"""
URL configuration for FieldOfficerBackend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from rest_framework import routers
from myapp.views import *
from django.conf.urls.static import static


router = routers.DefaultRouter(trailing_slash=False)
# router.register(r'send_otp', SendOtpFunction)



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('send_otp',SendOtpFunction),
    path('verify_otp',VerifyOtpFunction),
    path('application',ApplicationVerificationFunction.as_view()),
    path('applicants', ApplicantsListView.as_view(), name='applicants-list'),
    path('dashboard', dashboardFunction.as_view()),
    path('no_of_customers', NoOfCustomers.as_view()),
    path('total_collection', TotalCollection.as_view()),
    path('collection_ageing', CollectionAgeing.as_view()),
    # path('upload', ImageUploadView.as_view(), name='image-upload'),

    # path('api-auth/', include('rest_framework.urls')),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
