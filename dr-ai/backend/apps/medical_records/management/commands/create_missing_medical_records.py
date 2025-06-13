from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.medical_records.models import MedicalRecord
from datetime import date

User = get_user_model()

class Command(BaseCommand):
    help = 'Create medical records for users that do not have one'

    def handle(self, *args, **kwargs):
        # Get users without medical records
        users_without_records = User.objects.filter(medicalrecord__isnull=True)
        count = users_without_records.count()
        
        if count == 0:
            self.stdout.write(
                self.style.SUCCESS('All users already have medical records')
            )
            return

        self.stdout.write(f'Found {count} users without medical records')
        
        for user in users_without_records:
            try:
                # Create basic medical record
                medical_record = MedicalRecord.objects.create(
                    user=user,
                    full_name=f"{user.first_name} {user.last_name}".strip() or user.username,
                    date_of_birth="2000-01-01",  # Default date
                    blood_type="Unknown"
                )
                
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Created medical record for {user.username} with NFC ID: {medical_record.nfc_id}'
                    )
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(
                        f'Error creating medical record for {user.username}: {str(e)}'
                    )
                )

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {count} medical records')
        )
