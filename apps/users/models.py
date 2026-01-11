from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    # Add professional fields here
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    is_student = models.BooleanField(default=True)
    is_teacher = models.BooleanField(default=False)

    # This makes it easier to identify users in the admin panel
    def __str__(self):
        return f"{self.username} ({'Student' if self.is_student else 'Admin'})"