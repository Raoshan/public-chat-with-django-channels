from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
import re
# Create your views here.

def chat(request):
    return render(request,'chat.html',{})

def Login(request):
    if request.user.is_authenticated:
        return redirect("index")
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            if username and password:
                user = authenticate(username=username,password=password)
                if user:
                    login(request,user)
                    return redirect("index")
        return render(request,'login.html',{})
    
def signup(request):
    if request.user.is_authenticated:
        return redirect("index")
    else:
        if request.method == 'POST':
            username = request.POST['username']
            email = request.POST['email']
            password1 = request.POST['password']
            confirm_password = request.POST['confirm_password']
            flag = 0
            if (len(password1)<7 or len(password1)>15):
                flag = 1
            elif not re.search('[a-z]', password1):
                flag = 1
            elif not re.search('[0-9]', password1):
                flag = 1
            elif not re.search('[A-Z]', password1):
                flag = 1
            elif not re.search('[@#$!]', password1):
                flag = 1  
            
            if (flag == 0):
                if password1==confirm_password:
                    if User.objects.filter(username=username).exists():
                        messages.info(request, 'Username Taken')
                        return redirect('signup')
                    elif User.objects.filter(email=email).exists():
                        messages.info(request, 'Email Taken')
                        return redirect('signup')
                    else:
                        user = User.objects.create_user(username=username,email=email,password=password1)
                        if user:
                            return redirect("login")
                else:
                    messages.info(request, 'Password does not match')
                    return redirect('signup')
            else:
                messages.info(request, 'Password is not valid')

        return render(request,'signup.html',{})

def Logout(request):
    logout(request)
    return redirect("index")