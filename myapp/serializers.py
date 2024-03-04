from rest_framework import serializers
from .models import *

class SendOtpSerializer(serializers.ModelSerializer):
    class Meta:
        model = SendOtpModel
        fields = '__all__'

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'

class ApplicationVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationVerification
        fields = '__all__'
