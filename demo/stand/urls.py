from django.urls import path
from . import views  # Import your views

urlpatterns = [
    # Enrollment Creation and Listing
    path('enrollments/', views.EnrollmentListCreate.as_view(), name='enrollment-list-create'),

    # Enrollment Details (retrieve, update, delete)
    path('enrollments/<int:pk>/', views.EnrollmentDetail.as_view(), name='enrollment-detail'),
]
