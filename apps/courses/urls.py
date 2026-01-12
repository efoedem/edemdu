from django.urls import path
from . import views

urlpatterns = [
    # 1. This is the "Welcome / Level Picker" page
    path('', views.course_list, name='course_list'),

    # 2. This is the specific page for a level (e.g., Level 100)
    path('level/<str:level>/', views.courses_by_level, name='level_view'),

    # 3. Standard course and enrollment paths
    path('course/<int:pk>/', views.course_detail, name='course_detail'),
    path('enroll/<int:pk>/', views.manual_payment, name='manual_payment'),
    path('receipt/<int:enrollment_id>/', views.download_receipt, name='download_receipt'),
]