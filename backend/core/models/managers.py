from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, full_name, **extra_fields):
        email=self.normalize_email(email)

        user_object = self.model(
            email=email,
            full_name=full_name,
            **extra_fields
        )

        user_object.set_password(password)

        user_object.save(using=self.db)
        return user_object

    def create_user(self, email, password, full_name, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, full_name, **extra_fields)

    def create_superuser(self, email, password, full_name, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, full_name, **extra_fields)
