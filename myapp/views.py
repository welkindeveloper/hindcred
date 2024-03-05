from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework import viewsets,response,status
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
import random
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from django.conf import settings


# class SendOtpViewSet(viewsets.ModelViewSet):
#     queryset = SendOtpModel.objects.all()
#     serializer_class = SendOtpSerializer

def responseReturn(status=None, message=None, result=None, data=None):
    default_status = 200
    default_message = "Fetch Successfully"
    default_result = "Success"

    response_map = {
        "status": status if status is not None else default_status,
        "message": f"${message}" if message is not None else default_message,
        "result": result if result is not None else default_result,
        "data": data
    }

    return Response(response_map)

@api_view(['POST'])
def SendOtpFunction(request):
    mobile_number = request.data.get("mobileNumber")
    existing_instance = SendOtpModel.objects.filter(mobileNumber=mobile_number).first()
    otp="".join(random.choices('0123456789', k=6))
    if existing_instance:        
        serializer = SendOtpSerializer(instance=existing_instance, data={"otp": otp}, partial=True)
    else:
        serializer = SendOtpSerializer(data={"mobileNumber": mobile_number, "otp": otp})

    if(serializer.is_valid()):
        serializer.save()
        return responseReturn(message="OTP send Successfully",data=otp)
    else:
        return responseReturn(status=400,result="failed",message=serializer.errors)

@api_view(['POST'])
def VerifyOtpFunction(request):
    mobile_number = request.data.get("mobileNumber")
    otp = request.data.get("otp")
    if not mobile_number or not otp:
        return responseReturn(status=400,result="Failed", message="Mobile number and OTP are required")

    querryData=SendOtpModel.objects.filter(mobileNumber=mobile_number)
    if querryData.exists():
        print(querryData.first().otp)
        if querryData.first().otp == otp:
            user,created = User.objects.get_or_create(username=mobile_number,defaults={'password': '1@12345'})
            token, created = Token.objects.get_or_create(user=user)

            return responseReturn(message='OTP verified successfully',data={"token":token.key})
        else:
            return responseReturn(status=400,result="Failed",message="Wrong OTP")

    return responseReturn(status=400,result="Failed",message="Mobile Number does Not Exists")


class ImageUploadView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ApplicationVerificationFunction(APIView):

    def post(self,request,*args,**kwargs):
        
        applicant = request.data.get('applicant')
        step = request.data.get('step')
        step=int(step)
        if not applicant:
            return responseReturn(status=400,result="failed",message="applicant Id is Null")
        
        instanceApplicants = Applicants.objects.get(applicant_id=applicant)
        if not instanceApplicants:
            return responseReturn(status=400,result="failed",message="applicant Id does not exists")
        

        if not step or step == 0:
            return responseReturn(status=400,result="failed",message="step is required")
        
        if step == 1:
            pan_number = request.data.get('pan_number')
            pan_front = request.data.get('pan_front')
            pan_back = request.data.get('pan_back')
            if not pan_number or not pan_front or not pan_back:
                return responseReturn(status=400,result="failed",message="pan_number, pan_front, and pan_back are required")
            if len(pan_number) != 10:
                return responseReturn(status=400,result="failed",message="Invalid Pan Number length")
       
        if step == 2:
            aadhar_number = request.data.get('aadhar_number')
            aadhar_front = request.data.get('aadhar_front')
            aadhar_back = request.data.get('aadhar_back')
            if not aadhar_number or not aadhar_front or not aadhar_back:
                return responseReturn(status=400,result="failed",message="aadhar_number, aadhar_front, and aadhar_back are required")
            if len(aadhar_number) != 12:
                return responseReturn(status=400,result="failed",message="Invalid Aadhar Number length")
        
        if step == 3:
            voter_id = request.data.get('voter_id')
            voter_front = request.data.get('voter_front')
            voter_back = request.data.get('aadhar_back')
            if not voter_id or not voter_front or not voter_back:
                return responseReturn(status=400,result="failed",message="voter_id, voter_front, and voter_back are required")
            if len(voter_id) != 10:
                return responseReturn(status=400,result="failed",message="Invalid Voter ID length")
        
        if step == 4:
            selfie = request.data.get('selfie')
            if not selfie:
                return responseReturn(status=400,result="failed",message="selfie required")
        
        if step == 5:
            business_type = request.data.get('business_type')
            business_name = request.data.get('business_name')
            business_address = request.data.get('business_address')
            business_pic = request.data.get('business_pic')
            if not business_type or not business_name or not business_address or not business_pic:
                return responseReturn(status=400,result="failed",message="business_type, business_name, business_address and business_pic are required")
            if len(business_name) < 3:
                return responseReturn(status=400,result="failed",message="business_name too short")
        
        if step == 6:
            two_wheeler = request.data.get('two_wheeler')
            four_wheeler = request.data.get('four_wheeler')
            own_residence = request.data.get('own_residence')
            rented = request.data.get('rented')
            life_insurance = request.data.get('life_insurance')
            credit_card = request.data.get('credit_card')
            any_loan = request.data.get('any_loan')
            dependent_member = request.data.get('dependent_member')
            children_academic = request.data.get('children_academic')
            if not two_wheeler or not four_wheeler or not own_residence or not rented or not life_insurance or not credit_card or not any_loan or not dependent_member or not children_academic:
                return responseReturn(status=400,result="failed",message="two_wheeler, four_wheeler, own_residence ,rented, life_insurance, credit_card, any_loan, dependent_member and children_academic are required")
            if (two_wheeler not in ('0', '1') or four_wheeler not in ('0', '1') or own_residence not in ('0', '1') or rented not in ('0', '1') or life_insurance not in ('0', '1') or credit_card not in ('0', '1') or any_loan not in ('0', '1') or dependent_member not in ('0', '1') or children_academic not in ('0', '1')):
                return responseReturn(status=400, result="failed", message="All fields must be either '0' or '1'")
        
        if step > 6:
            return responseReturn(status=400, result="failed", message="Invalid Step")

        instance = ApplicationVerification.objects.filter(applicant_id=applicant).first()
        if instance.step==6:
            return responseReturn(status=400, result="failed", message="Application already applied")
        if not instance:
            serializer= ApplicationVerificationSerializer(data=request.data,partial=True)
        else:
            serializer= ApplicationVerificationSerializer(instance,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return responseReturn(data=serializer.data,message="Application save succesfully")
        return responseReturn(status=400,result='failed',message=serializer.errors)
