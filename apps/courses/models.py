from django.db import models
from django.conf import settings
from cloudinary.models import CloudinaryField


class Category(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.title


class Course(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='courses', null=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    thumbnail = CloudinaryField('image', folder='edemdu/courses/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Enrollment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Confirmation'),
        ('confirmed', 'Confirmed'),
    ]

    # CHANGED: Added null=True and blank=True to allow Guest enrollments
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    # Receipt details

    full_name = models.CharField(max_length=20) # Updated to 20
    index_number = models.CharField(max_length=10) # Updated to 10
    whatsapp_number = models.CharField(max_length=10) # Updated to 10

    reference_id = models.CharField(max_length=50, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.course.title}"