from django.urls import path
from . import views

urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('course/<int:pk>/', views.course_detail, name='course_detail'),
    path('enroll/<int:pk>/', views.manual_payment, name='manual_payment'),
    path('receipt/<int:enrollment_id>/', views.download_receipt, name='download_receipt'),
    # REMOVED: path('dashboard/', views.student_dashboard, name='student_dashboard'),
]