from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework import viewsets,response,status,generics
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
import random
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from django.conf import settings
from django.db import connection

                
# class SendOtpViewSet(viewsets.ModelViewSet):
#     queryset = SendOtpModel.objects.all()
#     serializer_class = SendOtpSerializer

def responseReturn(status=None, message=None, result=None, data=None):
    default_status = 200
    default_message = "Fetch Successfully"
    default_result = "Success"

    response_map = {
        "status": status if status is not None else default_status,
        "message": f"{message}" if message is not None else default_message,
        "result": result if result is not None else default_result,
        "data": data
    }

    return Response(response_map)


def requestDatabase(raw_query):
    try:
        with connection.cursor() as cursor:
            cursor.execute(raw_query)

            columns = [col[0] for col in cursor.description]
            results = cursor.fetchall()
            data=None
            list=[]
            for row in results:
                data = {col: val for col, val in zip(columns, row)}
                list.append(data)
            return responseReturn(data=list)
    except:
        return responseReturn(status=400,result="failed",message="Something went wrong")

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

class ApplicantsListView(APIView):
    def get(self,request):
        raw_query="SELECT * FROM customers where status=2"
        with connection.cursor() as cursor:
            cursor.execute(raw_query)
        results = cursor.fetchall()
        list=[]
        with connection.cursor() as cursor:
            cursor.execute(raw_query)
            columns = [col[0] for col in cursor.description]
            results = cursor.fetchall()
            print(columns)
            print(results)
            for row in results:
                data = {col: val for col, val in zip(columns, row)}
                list.append(data)
            return responseReturn(data=list)
    


class ApplicationVerificationFunction(APIView):
    def get(self,request):
        applicant_id = request.GET.get('applicant_id')
        print(applicant_id)
        instance = ApplicationVerification.objects.filter(applicant_id=applicant_id).first()
        return responseReturn(data=ApplicationVerificationSerializer(instance,context={'request': request}).data)



    def post(self,request,*args,**kwargs):
        
        applicant_id = request.data.get('applicant_id')
        step = request.data.get('step')
        step=int(step)

    
        instance = ApplicationVerification.objects.filter(applicant_id=applicant_id).first()
        if instance is not None and instance.step==6:
            return responseReturn(status=400, result="failed", message="Application already applied")
        
        if not applicant_id:
            return responseReturn(status=400,result="failed",message="applicant Id is Null")

        if not step or step == 0:
            return responseReturn(status=400,result="failed",message="step is required")
        
        if step == 1:
            pan_number = request.data.get('pan_number')
            pan_front = request.data.get('pan_front')
            pan_back = request.data.get('pan_back')
            if not pan_number:
                return responseReturn(status=400,result="failed",message="pan_number required")
            if len(pan_number) != 10:
                return responseReturn(status=400,result="failed",message="Invalid Pan Number length")
            if not instance and not pan_front or instance and not instance.pan_front and not pan_front:
                return responseReturn(status=400,result="failed",message=" pan_front is required")
            if not instance and not pan_back or instance and not instance.pan_back and not pan_back:
                return responseReturn(status=400,result="failed",message=" pan_back is required")
       
        if step == 2:
            aadhar_number = request.data.get('aadhar_number')
            aadhar_front = request.data.get('aadhar_front')
            aadhar_back = request.data.get('aadhar_back')
            if not aadhar_number:
                return responseReturn(status=400,result="failed",message="aadhar_number required")
            if len(aadhar_number) != 12:
                return responseReturn(status=400,result="failed",message="Invalid Aadhaar Number length")
            
            if not instance and not aadhar_front or instance and not instance.aadhar_front and not aadhar_front:
                return responseReturn(status=400,result="failed",message=" aadhar_front is required")
            if not instance and not aadhar_back or instance and not instance.aadhar_back and not aadhar_back:
                return responseReturn(status=400,result="failed",message=" aadhar_back is required")
        
        if step == 3:
            voter_id = request.data.get('voter_id')
            voter_front = request.data.get('voter_front')
            voter_back = request.data.get('voter_back')
            if not voter_id:
                return responseReturn(status=400,result="failed",message="voter_id required")
            if len(voter_id) != 10:
                return responseReturn(status=400,result="failed",message="Invalid Voter ID length")
            
            if not instance and not voter_front or instance and not instance.voter_front and not voter_front:
                return responseReturn(status=400,result="failed",message=" voter_front is required")
            if not instance and not voter_back or instance and not instance.voter_back and not voter_back:
                return responseReturn(status=400,result="failed",message=" voter_back is required")
        
        if step == 4:
            selfie = request.data.get('selfie')
            if not instance and not selfie or instance and not instance.selfie and not selfie:
                return responseReturn(status=400,result="failed",message=" selfie is required")
        
        if step == 5:
            business_type = request.data.get('business_type')
            business_name = request.data.get('business_name')
            business_address = request.data.get('business_address')
            business_pic = request.data.get('business_pic')
            if not business_type or not business_name or not business_address:
                return responseReturn(status=400,result="failed",message="business_type, business_name and business_address are required")
            if not instance and not business_pic or instance and not instance.business_pic and not business_pic:
                return responseReturn(status=400,result="failed",message=" business_pic is required")
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

        
        if not instance:
            serializer= ApplicationVerificationSerializer(data=request.data,partial=True,context={'request': request})
        else:
            serializer= ApplicationVerificationSerializer(instance,data=request.data,partial=True,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return responseReturn(data=serializer.data,message="Application save succesfully")
        return responseReturn(status=400,result='failed',message=serializer.errors)

    

class dashboardFunction(APIView):
    def get(self,request):
        raw_query = """ SELECT  (
                SELECT COUNT(*)
                FROM   customers where status=2
                ) AS under_approval,

                (
                SELECT COUNT(*)
                FROM   customers where agent_id=11 and status =5
                ) AS done_application,

                (
                SELECT COUNT(*)
                FROM  assign_emi_pendings WHERE emp_id=2
                ) AS no_of_customer ,

                (
                SELECT COUNT(*)
                FROM  collection_transactions WHERE collected_by=0
                ) AS total_collection ,  

                (
                SELECT SUM(collect_amount)
                FROM  collection_transactions WHERE collected_by=0
                ) AS collected_amount ,

                (
                select count(*) from disbursements where no_emi_pending <=3 
                ) as zero_three, 

                (
                select count(*) from disbursements where no_emi_pending >=4 and no_emi_pending <=7 
                ) as four_seven,

                (
                select count(*) from disbursements where no_emi_pending >=8 and no_emi_pending <=14
                ) as eight_fourteen,

                (
                select count(*) from disbursements where no_emi_pending >=15 and no_emi_pending <=29
                ) as fifteen_twentynine,

                (
                select count(*) from disbursements where no_emi_pending >=30 and no_emi_pending <=59
                ) as thirty_fiftynine,

                (
                select count(*) from disbursements where no_emi_pending >=60 and no_emi_pending <=90
                ) as sixty_ninety,

                (
                select count(*) from disbursements where no_emi_pending >90 
                ) as ninety_plus

                FROM  DUAL;
                """
        with connection.cursor() as cursor:
            cursor.execute(raw_query)

            columns = [col[0] for col in cursor.description]
            results = cursor.fetchall()
            for row in results:
                data = {col: val for col, val in zip(columns, row)}
                return responseReturn(data=data)
        return responseReturn(status=400,result="failed",message="Something went wrong")
    


class NoOfCustomers(APIView):
    def get(self,request):
        # raw_query="SELECT * FROM  assign_emi_pendings WHERE emp_id=2"
        raw_query="SELECT assign_emi_pendings.*, apply_loans.application_code,customers.id as customer_id,CONCAT(COALESCE(customers.fname,''),' ',COALESCE(customers.lname,'')) as customer_name,customers.cust_mobile FROM `assign_emi_pendings` INNER JOIN disbursements ON assign_emi_pendings.disburse_id=disbursements.id INNER JOIN apply_loans ON disbursements.application_id = apply_loans.id INNER JOIN customers ON apply_loans.customer_id = customers.id WHERE 1=1 AND assign_emi_pendings.emp_id='2';"
        raw_query="INSERT INTO assign_emi_pendings (disburse_id, emp_id, follow_up_date, follow_type, follow_up_content, status) VALUES (5, 11, '2024-03-22', 1, 'going to receive', 0);"
        # return requestDatabase(raw_query=raw_query)
        with connection.cursor() as cursor:
            cursor.execute(raw_query)

            columns = [col[0] for col in cursor.description]
            results = cursor.fetchall()
            data=None
            list=[]
            for row in results:
                data = {col: val for col, val in zip(columns, row)}
                list.append(data)
            return responseReturn(data=list)

class TotalCollection(APIView):
    def get(self,request):
        raw_query=""" SELECT collection_transactions.*, apply_loans.application_code,customers.id as customer_id,CONCAT(COALESCE(customers.fname,''),' ',COALESCE(customers.lname,'')) as customer_name,customers.cust_mobile FROM `collection_transactions` INNER JOIN disbursements ON collection_transactions.disburse_id=disbursements.id INNER JOIN apply_loans ON disbursements.application_id = apply_loans.id INNER JOIN customers ON apply_loans.customer_id = customers.id WHERE 1=1 AND collection_transactions.collected_by='0'; """
        return requestDatabase(raw_query=raw_query)