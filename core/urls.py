from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # ADD THIS LINE to fix the 404 error
    path('accounts/', include('django.contrib.auth.urls')),

    # Your existing course app urls
    path('', include('apps.courses.urls')),
]