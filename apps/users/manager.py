from django.contrib.auth.models import BaseUserManager


class CustomUser(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have admin=True.")
        if not password:
            raise TypeError("Superuser must have a password.")
        user = self.create_user(
            email=email,
            password=password,
            **extra_fields
        )
        user.save(using=self._db)
        return user
