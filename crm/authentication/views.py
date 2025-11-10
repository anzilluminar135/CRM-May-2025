from django.shortcuts import render,redirect

# Create your views here.

from django.views import View

from .forms import LoginForm,OTPForm,ChangePasswordForm

from django.contrib.auth import authenticate,login,logout

from django.contrib import messages 

from crm.utils import generate_otps,sent_email,send_otp_sms,masking_email_and_phone

from django.utils.decorators import method_decorator

from authentication.permissions import permitted_users

import threading

from django.utils import timezone

from django.contrib.auth import update_session_auth_hash


# from django.contrib.auth.models import User

class LoginView(View):

    form_class = LoginForm

    def get(self,request,*args,**kwargs):

        form = self.form_class()

        data = {'form':form}

        return render(request,'authentication/login.html',context=data)
    
    def post(self,request,*args,**kwargs):

        form = self.form_class(request.POST)

        error = None

        if form.is_valid():

            email = form.cleaned_data.get('email')  #{'email':'abc@mail.com','password':'hjddvh'}

            password = form.cleaned_data.get('password') 

            user = authenticate(username=email,password=password)

            if user :

                login(request,user)

                messages.success(request,'successfully logined')

                return redirect('dashboard')
            
            error = 'invalid email or password'

        data = {'form':form,'error':error}

        return render(request,'authentication/login.html',context=data)
    
class LogoutView(View):

    def get(self,request,*args,**kwargs):

        logout(request)

        return redirect('login')


@method_decorator(permitted_users(['Student']),name='dispatch')
class OTPView(View):

    form_class = OTPForm

    def get(self,request,*args,**kwargs):

        form = self.form_class()

        email_otp,phone_otp = generate_otps()

        otp = request.user.otp

        otp.email_otp = email_otp

        otp.phone_otp = phone_otp

        otp.save()

        recepient = request.user.students.email

        template = 'email/otp-email.html'

        context = {'otp':email_otp,'name':f'{request.user.students.first_name} {request.user.students.last_name}'}

        title = 'Request To Change Password' 

        thread = threading.Thread(target=sent_email,args=(recepient,template,title,context))

        thread.start()

        send_otp_sms(phone_otp)

        masked_email,masked_phone = masking_email_and_phone(request.user.students.email,request.user.students.contact_num)

        request.session['otp_time'] = timezone.now().timestamp()

        remaining_time = 300

        data = {'form':form,'masked_email':masked_email,'masked_phone':masked_phone,'remaining_time':remaining_time}

        return render(request,'authentication/otp.html',context=data)
    
    def post(self,request,*args,**kwargs):

        form = self.form_class(request.POST)

        error = None

        if form.is_valid():

            form_email_otp = form.cleaned_data.get('email_otp')

            form_phone_otp = form.cleaned_data.get('phone_otp')

            otp = request.user.otp

            db_email_otp = otp.email_otp

            db_phone_otp = otp.phone_otp

            otp_time = request.session.get('otp_time')  

            current_time = timezone.now().timestamp()

            if otp_time :

                elapsed = current_time - otp_time

                remaining_time = max(0, 300 - int(elapsed))

                if elapsed > 300 :

                    error = 'OTP expired Request a Newone'

                elif form_email_otp == db_email_otp and form_phone_otp == db_phone_otp :
                    
                    messages.success(request,'OTPs Verified')

                    request.session.pop('otp_time')

                    otp.otp_verified = True

                    otp.save()

                    return redirect('change-password')
                
                else :


                    error = 'Invalid OTP'

        data = {'form':form,'error':error,'remaining_time':remaining_time}

        return render(request,'authentication/otp.html',context=data)   

@method_decorator(permitted_users(['Student']),name='dispatch')
class ChangePasswordView(View):

    form_class = ChangePasswordForm

    def get(self,request,*args,**kwargs):

        if request.user.otp.otp_verified :
            
            form = self.form_class()

            data = {'form':form}

            return render(request,'authentication/password.html',context=data)
        
        else :

            return redirect('otp')
    
    def post(self,request,*args,**kwargs):

        form = self.form_class(request.POST)

        if form.is_valid():

            password = form.cleaned_data.get('password')

            user = request.user

            user.set_password(password)

            user.save()

            otp = user.otp

            otp.otp_verified = False

            otp.save()

            update_session_auth_hash(request, user)

            messages.success(request,'Password Updated Successfully')

            return redirect('dashboard')
        
        data = {'form':form}

        return render(request,'authentication/password.html',context=data)




