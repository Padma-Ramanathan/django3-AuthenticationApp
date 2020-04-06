from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login,logout,authenticate


def homepage(request):
    return render(request,"authenticationApp/homepage.html")

def signupuser(request):
    if request.method=="GET":
        return render(request,"authenticationApp/signupuser.html",{'forms':UserCreationForm})
    else:
        if request.POST['password1']==request.POST['password2']:
            try:
                user= User.objects.create_user(request.POST['username'],password=request.POST['password1'])
                user.save()
                login(request,user)
                return redirect("currentpage")
            except IntegrityError:
                return render(request, "authenticationApp/signupuser.html", {'forms': UserCreationForm,"error":"Username is already taken. Use other username"})
        else:
            return render(request, "authenticationApp/signupuser.html", {'forms': UserCreationForm,"error":"Password didn't match"})


def logoutuser(request):
    if request.method=="POST":
        logout(request)
        return redirect("homepage")

def loginuser(request):
    if request.method == "GET":
        return render(request, "authenticationApp/loginuser.html", {'forms': AuthenticationForm})
    else:
        user = authenticate(request,username=request.POST['username'],password=request.POST['password'])
        if user is None:
            return render(request, "authenticationApp/loginuser.html", {'forms': AuthenticationForm,"error":"Username doesn't exist"})
        else:
            login(request,user)
            return redirect("currentpage")



def currentpage(request):
    return render(request,"authenticationApp/currentpage.html")
