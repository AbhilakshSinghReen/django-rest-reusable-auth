from django.contrib.auth.admin import UserAdmin
from django import forms

from core.models.models import CustomUser


class CustomUserCreationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'full_name')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'full_name', 'is_active', 'is_staff', 'is_superuser')


class CustomUserAdmin(UserAdmin):
    model = CustomUser

    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    
    list_display = ('email', 'full_name', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active', 'groups')
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'full_name',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',)}),
        ('Important dates', {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'full_name', 'password', 'is_active', 'is_staff', 'is_superuser'),
        }),
    )

    search_fields = ('email', 'full_name')

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['email', 'full_name', 'is_staff', 'is_superuser', 'last_login']
        return ['invite_sent_at']
