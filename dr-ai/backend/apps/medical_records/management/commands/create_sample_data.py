# from django.core.management.base import BaseCommand
# from django.contrib.auth import get_user_model
# from apps.medical_records.models import MedicalRecord
# import uuid

# User = get_user_model()

# SAMPLE_DATA = [
#     {
#         "username": "patient1",
#         "password": "patient123",
#         "email": "patient1@example.com",
#         "medical_record": {
#             "full_name": "Ahmed Mohamed",
#             "date_of_birth": "1985-03-15",
#             "blood_type": "A+",
#             "allergies": "Penicillin, Dust",
#             "chronic_conditions": "Type 2 Diabetes, Hypertension",
#             "medications": """- Metformin 500mg twice daily
# - Lisinopril 10mg once daily
# - Aspirin 81mg once daily""",
#             "medical_history": """2020: Diagnosed with Type 2 Diabetes
# 2018: Hypertension diagnosis
# 2015: Appendectomy
# 2010: Fractured right ankle
# Regular checkups show stable blood pressure and improving blood sugar levels."""
#         }
#     },
#     {
#         "username": "patient2",
#         "password": "patient123",
#         "email": "patient2@example.com",
#         "medical_record": {
#             "full_name": "Sara Ahmed",
#             "date_of_birth": "1990-07-22",
#             "blood_type": "O-",
#             "allergies": "Shellfish, Latex",
#             "chronic_conditions": "Asthma, Migraine",
#             "medications": """- Albuterol inhaler as needed
# - Sumatriptan 50mg for migraines
# - Montelukast 10mg daily""",
#             "medical_history": """2023: Severe asthma exacerbation requiring hospitalization
# 2021: Started migraine prophylaxis
# 2019: Diagnosed with moderate persistent asthma
# 2017: Tonsillectomy
# Regular pulmonary function tests show good asthma control."""
#         }
#     },
#     {
#         "username": "patient3",
#         "password": "patient123",
#         "email": "patient3@example.com",
#         "medical_record": {
#             "full_name": "Omar Khaled",
#             "date_of_birth": "1975-11-30",
#             "blood_type": "B+",
#             "allergies": "None",
#             "chronic_conditions": "Rheumatoid Arthritis, Osteoporosis",
#             "medications": """- Methotrexate 15mg weekly
# - Folic acid 1mg daily
# - Prednisone 5mg daily
# - Alendronate 70mg weekly
# - Calcium + Vitamin D supplement daily""",
#             "medical_history": """2022: Started osteoporosis treatment
# 2019: Rheumatoid arthritis diagnosis
# 2018: Total knee replacement (right)
# 2016: Carpal tunnel surgery
# Regular rheumatology follow-ups show disease under control."""
#         }
#     },
#     {
#         "username": "patient4",
#         "password": "patient123",
#         "email": "patient4@example.com",
#         "medical_record": {
#             "full_name": "Emma Wilson",
#             "date_of_birth": "1992-05-15",
#             "blood_type": "O+",
#             "allergies": "Penicillin, Pollen",
#             "chronic_conditions": "Asthma, Hypertension",
#             "medications": """- Ventolin inhaler as needed
# - Amlodipine 5mg once daily
# - Singulair 10mg daily""",
#             "medical_history": """2023: Severe asthma attack
# 2022: Started hypertension treatment
# 2020: Diagnosed with asthma
# 2018: Tonsillectomy
# Regular follow-ups show improved asthma control"""
#         }
#     },
#     {
#         "username": "patient5",
#         "password": "patient123",
#         "email": "patient5@example.com",
#         "medical_record": {
#             "full_name": "James Cooper",
#             "date_of_birth": "1988-11-20",
#             "blood_type": "A-",
#             "allergies": "Seafood",
#             "chronic_conditions": "Type 2 Diabetes, Depression",
#             "medications": """- Metformin 850mg twice daily
# - Glimepiride 2mg once daily
# - Sertraline 50mg daily
# - Aspirin 81mg daily""",
#             "medical_history": """2021: Diagnosed with Type 2 Diabetes
# 2020: Started depression treatment
# 2019: Elevated HbA1c levels
# 2017: Cholecystectomy
# Regular monitoring shows improving blood sugar levels"""
#         }
#     }
# ]

# class Command(BaseCommand):
#     help = 'Creates sample users with medical records'

#     def handle(self, *args, **kwargs):
#         for data in SAMPLE_DATA:
#             try:
#                 # Check if user exists
#                 if not User.objects.filter(username=data['username']).exists():
#                     # Create user
#                     user = User.objects.create_user(
#                         username=data['username'],
#                         email=data['email'],
#                         password=data['password']
#                     )
                    
#                     # Create medical record
#                     medical_data = data['medical_record']
#                     medical_data['user'] = user
#                     medical_data['nfc_id'] = str(uuid.uuid4())
                    
#                     medical_record = MedicalRecord.objects.create(**medical_data)
                    
#                     # Success message with details
#                     self.stdout.write(
#                         self.style.SUCCESS(
#                             f"\nCreated new medical record:"
#                             f"\nPatient: {medical_record.full_name}"
#                             f"\nUsername: {user.username}"
#                             f"\nPassword: {data['password']}"
#                             f"\nNFC ID: {medical_record.nfc_id}"
#                             f"\nAccess URL: http://localhost:5174/record/{medical_record.nfc_id}"
#                         )
#                     )
#                 else:
#                     self.stdout.write(
#                         self.style.WARNING(f"User {data['username']} already exists")
#                     )
                    
#             except Exception as e:
#                 self.stdout.write(
#                     self.style.ERROR(f"Error creating record for {data['username']}: {str(e)}")
#                 )
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.medical_records.models import MedicalRecord

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates one sample user with a specific NFC ID (ADE4987D)'

    def handle(self, *args, **kwargs):
        username = "patientx"
        password = "patient123"
        email = "patientx@example.com"
        nfc_id = "ADE4987D"

        medical_data = {
            "full_name": "Ahmed Mohamed",
            "date_of_birth": "1985-03-15",
            "blood_type": "A+",
            "allergies": "Penicillin, Dust",
            "chronic_conditions": "Type 2 Diabetes, Hypertension",
            "medications": """- Metformin 500mg twice daily
- Lisinopril 10mg once daily
- Aspirin 81mg once daily""",
            "medical_history": """2020: Diagnosed with Type 2 Diabetes
2018: Hypertension diagnosis
2015: Appendectomy
2010: Fractured right ankle
Regular checkups show stable blood pressure and improving blood sugar levels."""
        }

        try:
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password
                )

                medical_data['user'] = user
                medical_data['nfc_id'] = nfc_id

                medical_record = MedicalRecord.objects.create(**medical_data)

                self.stdout.write(
                    self.style.SUCCESS(
                        f"\n✅ Created new medical record:"
                        f"\n👤 Patient: {medical_record.full_name}"
                        f"\n🔐 Username: {user.username}"
                        f"\n🧬 NFC ID: {medical_record.nfc_id}"
                        f"\n🔗 Access URL: http://localhost:5174/record/{medical_record.nfc_id}\n"
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f"⚠️ User '{username}' already exists. Skipping creation.")
                )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"❌ Error creating user or medical record: {str(e)}")
            )
