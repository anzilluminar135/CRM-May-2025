from django.shortcuts import render,redirect

# Create your views here.

from django.views import View

from .forms import LoginForm

from django.contrib.auth import authenticate,login,logout

from django.contrib import messages 

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



