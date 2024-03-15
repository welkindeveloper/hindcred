from django.db import models


class SendOtpModel(models.Model):
    mobileNumber = models.CharField(max_length=255)
    otp = models.CharField(max_length=255) 

    def __str__(self):
        return self.mobileNumber
    class Meta:
        db_table = 'sendotpmodel'


# class Image(models.Model):
    # image = models.ImageField(upload_to='images/')


class Applicants(models.Model):
    CHOICES = [
        ('PENDING', 'Pending'),
        ('ONGOING', 'Ongoing'),
        ('COMPLETED', 'Completed'),
    ]
    applicant_id=models.CharField(max_length=50,primary_key=True)
    first_name=models.CharField(max_length=50)
    middle_name=models.CharField(max_length=50,blank=True)
    last_name=models.CharField(max_length=50,blank=True)
    address=models.TextField()
    mobile_number=models.CharField(max_length=20)
    status=models.CharField(max_length=20, choices=CHOICES)

    def __str__(self):
        return f"{dict(self.CHOICES).get(self.status)} : {self.first_name}"
    
    class Meta:
        db_table = 'applicants'
    

class ApplicationVerification(models.Model):
    CHOICES = [
        ('1', 'Yes'),
        ('0', 'No')
    ]

    applicant=models.CharField(max_length=100)
    pan_number=models.CharField(max_length=10)
    pan_front = models.ImageField(upload_to='images/')
    pan_back = models.ImageField(upload_to='images/')
    aadhar_number=models.CharField(max_length=12)
    aadhar_front = models.ImageField(upload_to='images/')
    aadhar_back = models.ImageField(upload_to='images/')
    voter_id=models.CharField(max_length=10)
    voter_front = models.ImageField(upload_to='images/')
    voter_back = models.ImageField(upload_to='images/')
    selfie = models.ImageField(upload_to='images/')
    business_type=models.CharField(max_length=100)
    business_name=models.TextField()
    business_address=models.TextField()
    business_pic = models.ImageField(upload_to='images/')
    two_wheeler=models.CharField(max_length=5, choices=CHOICES)
    four_wheeler=models.CharField(max_length=5, choices=CHOICES)
    own_residence=models.CharField(max_length=5, choices=CHOICES)
    rented=models.CharField(max_length=5, choices=CHOICES)
    life_insurance=models.CharField(max_length=5, choices=CHOICES)
    credit_card=models.CharField(max_length=5, choices=CHOICES)
    any_loan=models.CharField(max_length=5, choices=CHOICES)
    dependent_member=models.CharField(max_length=5, choices=CHOICES)
    children_academic=models.CharField(max_length=5, choices=CHOICES)
    step=models.IntegerField(default=0)

    def __str__(self):
        return f"step {self.step} : {self.applicant.first_name}"
    
    class Meta:
        db_table = 'applicationVerification'

