import re
from typing import Dict, Any
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from ..utils.logger import setup_logger

logger = setup_logger('ollama_client')

class OllamaClient:
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.ollama = Ollama(
            base_url=base_url,
            model="medllama2",
            temperature=0.05,
            num_ctx=4096,
            top_k=40,
            top_p=0.9,
            repeat_penalty=1.2,
            num_predict=1024,
            system="""You are a chief medical specialist with 20+ years of experience. 
Provide authoritative diagnoses and evidence-based treatment plans. 
Structure responses EXACTLY as:

DIAGNOSIS:
[detailed analysis]

TREATMENT PLAN:
[step-by-step protocol]

CRITICAL FORMATTING RULES:
1. DIAGNOSIS and TREATMENT PLAN must be standalone section headers in ALL CAPS
2. NEVER combine diagnosis and treatment in the same section
3. ALWAYS start DIAGNOSIS section on a new line
4. ALWAYS start TREATMENT PLAN section on a new line after diagnosis
5. Use ONLY these exact headers: "DIAGNOSIS:" and "TREATMENT PLAN:"
6. NEVER include these headers within sentences
7. Treatment plan MUST include numbered steps
8. NEVER include placeholders like [Your signature]
9. NEVER include your name or credentials
10. Provide ONLY clinical content"""
        )
        logger.info(f"Initialized enhanced medical specialist client with model: medllama2")
        
        self.prompt_template = PromptTemplate(
            template="""**Medical Analysis Request**
Patient: {full_name} | DOB: {date_of_birth} | Blood: {blood_type}
**Critical Alerts**: 
- Allergies: {allergies}
- Chronic Conditions: {chronic_conditions}
- Current Medications: {medications}

**Clinical History**:
{medical_history}

**Consultation Query**: {question}

**Required Output Format**:
DIAGNOSIS:
[Your clinical assessment including: 
- Pathophysiology mechanism 
- Diagnostic criteria met 
- Differential diagnosis 
- ICD-11 code]

TREATMENT PLAN:
[Your prescribed actions:
1. Primary pharmacotherapy (drug class, dose, frequency)
2. Adjuvant therapies 
3. Lifestyle modifications
4. Monitoring parameters 
5. Red flags requiring immediate attention]

**STRICT FORMAT REQUIREMENTS**:
- Start DIAGNOSIS section on new line
- Start TREATMENT PLAN section on new line after diagnosis
- Use EXACT section headers: "DIAGNOSIS:" and "TREATMENT PLAN:" in ALL CAPS
- Never include section headers in middle of sentences
- Do NOT include placeholders like [Your signature]
- Do NOT include your name or credentials
- Provide ONLY clinical content""",
            input_variables=["full_name", "date_of_birth", "blood_type", "allergies", 
                           "chronic_conditions", "medications", "medical_history", "question"]
        )

    def generate_medical_response(self, medical_record: Dict[str, Any], question: str) -> Dict[str, str]:
        try:
            logger.info(f"Consultation for {medical_record['full_name']} | DOB: {medical_record['date_of_birth']}")
            logger.info(f"Clinical Query: '{question}'")
            logger.debug(f"Medical Context:\nAllergies: {medical_record['allergies']}\nMedications: {medical_record['medications']}")
            
            prompt = self.prompt_template.format(
                full_name=medical_record['full_name'],
                date_of_birth=medical_record['date_of_birth'],
                blood_type=medical_record['blood_type'],
                allergies=medical_record['allergies'],
                chronic_conditions=medical_record['chronic_conditions'],
                medications=medical_record['medications'],
                medical_history=medical_record['medical_history'],
                question=question
            )
            
            logger.debug(f"Generated clinical prompt:\n{prompt}")
            
            response = self.ollama.invoke(prompt)
            logger.debug(f"Raw Specialist Response:\n{response}")
            
            parsed_response = self._parse_medical_response(response)
            logger.info("Successfully generated specialist-level response")
            
            return parsed_response
            
        except Exception as e:
            logger.error(f"Consultation error: {str(e)}", exc_info=True)
            raise

    def _parse_medical_response(self, response: str) -> Dict[str, str]:
        try:
            # Clean unwanted patterns before parsing
            response = re.sub(
                r'\[Your\s*(signature|name|credentials?)\]\s*', 
                '', 
                response, 
                flags=re.IGNORECASE
            )
            
            # Remove trailing condition names like "GERD" at the end
            response = re.sub(
                r'[\n\s]+[A-Z]+\s*$', 
                '', 
                response
            )
            
            # Normalize section headers
            normalized_response = re.sub(
                r'(?i)(\bdifferential\s*)?diagnosis\s*[:]?', 
                'DIAGNOSIS:', 
                response
            )
            normalized_response = re.sub(
                r'(?i)treatment\s*plan\s*[:]?', 
                'TREATMENT PLAN:', 
                normalized_response
            )
            
            # Split into sections using standardized headers
            sections = re.split(
                r'(?i)(DIAGNOSIS:|TREATMENT PLAN:)', 
                normalized_response
            )
            
            # Find positions of section headers
            diagnosis_pos = None
            treatment_pos = None
            
            for idx, section in enumerate(sections):
                if section.upper() == "DIAGNOSIS:":
                    diagnosis_pos = idx
                elif section.upper() == "TREATMENT PLAN:":
                    treatment_pos = idx
            
            # Validate section positions
            if diagnosis_pos is None:
                raise ValueError("DIAGNOSIS section header not found")
            if treatment_pos is None:
                raise ValueError("TREATMENT PLAN section header not found")
            if treatment_pos <= diagnosis_pos:
                raise ValueError("TREATMENT PLAN appears before DIAGNOSIS")
            
            # Extract diagnosis content
            diagnosis_content = ''.join(sections[diagnosis_pos+1:treatment_pos]).strip()
            
            # Extract treatment content
            treatment_content = ''.join(sections[treatment_pos+1:]).strip()
            
            # Extract ICD code if present
            icd_match = re.search(r"ICD-11:\s*([A-Z0-9\.]+)", response, re.IGNORECASE)
            icd_code = icd_match.group(1).strip() if icd_match else None
            
            # Additional cleaning of diagnosis content
            diagnosis_content = re.sub(
                r'Thank you for providing the patient\'s details\.?\s*', 
                '', 
                diagnosis_content, 
                flags=re.IGNORECASE
            )
            
            # Build result
            result = {
                "diagnosis": diagnosis_content,
                "treatment_plan": treatment_content
            }
            
            if icd_code:
                result["icd_code"] = icd_code
                
            return result
            
        except Exception as e:
            logger.error(f"Enhanced parsing failed: {str(e)}")
            
            # Fallback 1: Try to extract treatment content using different patterns
            treatment_patterns = [
                r'TREATMENT PLAN:\s*(.*?)(?=\n\s*[A-Z]+:|\Z)',
                r'MANAGEMENT:\s*(.*?)(?=\n\s*[A-Z]+:|\Z)',
                r'RECOMMENDATIONS:\s*(.*?)(?=\n\s*[A-Z]+:|\Z)',
                r'PLAN:\s*(.*?)(?=\n\s*[A-Z]+:|\Z)'
            ]
            
            for pattern in treatment_patterns:
                treatment_match = re.search(pattern, response, re.IGNORECASE | re.DOTALL)
                if treatment_match:
                    treatment_content = treatment_match.group(1).strip()
                    diagnosis_content = response.replace(treatment_match.group(0), '').strip()
                    return {
                        "diagnosis": diagnosis_content,
                        "treatment_plan": treatment_content
                    }
            
            # Fallback 2: If all else fails, return entire response as diagnosis
            return {
                "diagnosis": response.strip(),
                "treatment_plan": "See diagnosis section for complete clinical assessment"
            }