# serializers.py
from rest_framework import serializers
from .models import ClientEnrollment

class ClientEnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientEnrollment
        fields = '__all__'
