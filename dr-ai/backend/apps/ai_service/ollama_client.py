import requests
import json
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
            temperature=0.1,
            num_ctx=2048,  # Increase context window
            repeat_penalty=1.1,  # Prevent repetition
            num_predict=512,  # Limit response length
            system="You are a medical AI assistant. Always respond with DIAGNOSIS: followed by diagnosis and TREATMENT PLAN: followed by treatment. No other text."
        )
        logger.info(f"Initialized Ollama client with model: medllama2")
        
        self.prompt_template = PromptTemplate(
            template="""Analyze this medical record and question. Respond ONLY using this exact format with these exact headings:

Medical Record:
- Patient: {full_name}
- DOB: {date_of_birth}
- Blood Type: {blood_type}
- Allergies: {allergies}
- Chronic Conditions: {chronic_conditions}
- Current Medications: {medications}
- Medical History: {medical_history}

Question: {question}

DIAGNOSIS:
<provide detailed diagnosis based on medical history and current symptoms>

TREATMENT PLAN:
<provide comprehensive treatment plan including medications, lifestyle changes, and follow-up recommendations>

Do not include any other text or sections. Start directly with DIAGNOSIS:""",
            input_variables=["full_name", "date_of_birth", "blood_type", "allergies", 
                           "chronic_conditions", "medications", "medical_history", "question"]
        )

    def generate_medical_response(self, medical_record: Dict[str, Any], question: str) -> Dict[str, str]:
        try:
            logger.info(f"Generating response for patient: {medical_record['full_name']}")
            logger.info(f"Question: {question}")
            
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
            
            logger.debug(f"Generated prompt:\n{prompt}")
            
            response = self.ollama.invoke(prompt)
            logger.debug(f"Raw AI Response:\n{response}")
            
            parsed_response = self._parse_medical_response(response)
            logger.info("Successfully generated and parsed AI response")
            
            return parsed_response
            
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}", exc_info=True)
            raise

    def _parse_medical_response(self, response: str) -> Dict[str, str]:
        try:
            # Remove any parenthetical text
            response = response.replace("(DIAGNOSIS)", "").replace("(TREATMENT PLAN)", "")
            
            # Split on exact headings
            parts = response.split("TREATMENT PLAN:")
            if len(parts) != 2:
                raise ValueError("Missing TREATMENT PLAN section")
            
            diagnosis_parts = parts[0].split("DIAGNOSIS:")
            if len(diagnosis_parts) != 2:
                raise ValueError("Missing DIAGNOSIS section")
            
            return {
                "diagnosis": diagnosis_parts[1].strip(),
                "treatment_plan": parts[1].strip()
            }
            
        except Exception as e:
            logger.error(f"Parse error: {str(e)}")
            logger.debug(f"Raw response:\n{response}")
            # Return the entire response as diagnosis if parsing fails
            return {
                "diagnosis": response.strip(),
                "treatment_plan": "See diagnosis section for complete response."
            }