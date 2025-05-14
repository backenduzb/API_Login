from django.db import models
from django.core.validators import RegexValidator
import uuid


phone_validator = RegexValidator(
    regex=r'^\+?998\d{9}$',
    message='Iltimos, telefon raqamini +998901234567 formatida kiriting.'
)

class User(models.Model):
    full_name = models.CharField(max_length=150, unique=True)
    phone_number = models.CharField(validators=[phone_validator], max_length=13, unique=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.full_name

class CustomToken(models.Model):
    key = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tokens')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Token for {self.user.full_name} — {self.key}"
