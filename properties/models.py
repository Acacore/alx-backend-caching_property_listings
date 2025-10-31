from django.contrib.auth.models import AbstractUser
from django.db import models

class Profile(AbstractUser):
    # Example of extra fields
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    is_agent = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'  # Use email to log in
    REQUIRED_FIELDS = ['username']  # Still require username for admin

    def __str__(self):
        return self.email


class Property(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)  # 👈 Correct spelling

    def __str__(self):
        return self.title