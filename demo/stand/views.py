from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import ClientEnrollment
from .serializers import ClientEnrollmentSerializer
from datetime import timedelta
from django.db.models import Q

class EnrollmentListCreate(APIView):
    def post(self, request):
        serializer = ClientEnrollmentSerializer(data=request.data)
        if serializer.is_valid():
            new_enrollment_time = serializer.validated_data['enrollment_time']
            if self.is_time_slot_busy(new_enrollment_time):
                return Response({'error': 'Time slot is already busy'}, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        enrollments = ClientEnrollment.objects.all()
        serializer = ClientEnrollmentSerializer(enrollments, many=True)
        return Response(serializer.data)

    def is_time_slot_busy(self, new_enrollment_time):
        existing_enrollments = ClientEnrollment.objects.filter(
            Q(enrollment_time__lte=new_enrollment_time + timedelta(minutes=30)) &
            Q(enrollment_time__gte=new_enrollment_time - timedelta(minutes=30))
        )
        return existing_enrollments.exists()

class EnrollmentDetail(APIView):
    def get(self, request, pk):
        enrollment = get_object_or_404(ClientEnrollment, pk=pk)
        serializer = ClientEnrollmentSerializer(enrollment)
        return Response(serializer.data)

    def put(self, request, pk):
        enrollment = get_object_or_404(ClientEnrollment, pk=pk)
        serializer = ClientEnrollmentSerializer(enrollment, data=request.data)
        if serializer.is_valid():
            # Add time validation before saving
            new_enrollment_time = serializer.validated_data['enrollment_time']
            if self.is_time_slot_busy(new_enrollment_time):
                return Response({'error': 'Time slot is already busy'}, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        enrollment = get_object_or_404(ClientEnrollment, pk=pk)
        enrollment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
