from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from django.db import transaction
from django import forms
from .models import User
from apps.medical_records.models import MedicalRecord

class CustomUserCreationForm(UserCreationForm):
    # Additional medical record fields
    date_of_birth = forms.DateField(required=True, help_text='Required. Format: YYYY-MM-DD')
    blood_type = forms.ChoiceField(choices=[
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('O+', 'O+'), ('O-', 'O-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
    ], required=True)
    allergies = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)
    chronic_conditions = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)
    medications = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)
    medical_history = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'get_nfc_id')
    list_filter = ('is_active', 'is_staff', 'groups')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('-date_joined',)

    def get_nfc_id(self, obj):
        try:
            return obj.medicalrecord.nfc_id
        except MedicalRecord.DoesNotExist:
            return '-'
    get_nfc_id.short_description = 'NFC ID'

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
        (_('Personal Information'), {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name'),
        }),
        (_('Medical Information'), {
            'classes': ('wide',),
            'fields': ('date_of_birth', 'blood_type', 'allergies', 'chronic_conditions', 'medications', 'medical_history'),
        }),
    )
    
    def save_model(self, request, obj, form, change):
        try:
            with transaction.atomic():
                is_new = obj.pk is None
                super().save_model(request, obj, form, change)
                
                if is_new and isinstance(form, CustomUserCreationForm):
                    # Generate a short NFC ID for medical record
                    medical_data = {
                        'user': obj,
                        'full_name': f"{form.cleaned_data.get('first_name', '')} {form.cleaned_data.get('last_name', '')}".strip() or obj.username,
                        'date_of_birth': form.cleaned_data.get('date_of_birth'),
                        'blood_type': form.cleaned_data.get('blood_type'),
                        'allergies': form.cleaned_data.get('allergies', ''),
                        'chronic_conditions': form.cleaned_data.get('chronic_conditions', ''),
                        'medications': form.cleaned_data.get('medications', ''),
                        'medical_history': form.cleaned_data.get('medical_history', '')
                    }
                    
                    medical_record = MedicalRecord.objects.create(**medical_data)
                    self.message_user(request, f'Medical record created successfully with NFC ID: {medical_record.nfc_id}')
        except Exception as e:
            self.message_user(request, f'Error creating medical record: {str(e)}', level='error')
            raise

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        
        if not is_superuser:
            form.base_fields['is_superuser'].disabled = True
            form.base_fields['user_permissions'].disabled = True
            form.base_fields['groups'].disabled = True
        
        return form