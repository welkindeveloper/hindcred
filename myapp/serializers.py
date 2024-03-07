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

class ApplicantsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Applicants
        fields = '__all__'


class ApplicationVerificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = ApplicationVerification
        fields = '__all__'

    def get_image_url(self, obj, field_name):
        request = self.context.get('request')
        if obj and getattr(obj, field_name):
            return request.build_absolute_uri(getattr(obj, field_name).url)
        return None

    def get_pan_front(self, obj):
        return self.get_image_url(obj, 'pan_front')

    def get_pan_back(self, obj):
        return self.get_image_url(obj, 'pan_back')

    def get_aadhar_front(self, obj):
        return self.get_image_url(obj, 'aadhar_front')

    def get_aadhar_back(self, obj):
        return self.get_image_url(obj, 'aadhar_back')

    def get_voter_front(self, obj):
        return self.get_image_url(obj, 'voter_front')

    def get_voter_back(self, obj):
        return self.get_image_url(obj, 'voter_back')

    def get_selfie(self, obj):
        return self.get_image_url(obj, 'selfie')

    def get_business_pic(self, obj):
        return self.get_image_url(obj, 'business_pic')