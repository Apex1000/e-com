from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template
from django.template import Context
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import *
from authentication import models as auth_models
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.csrf import csrf_exempt
from django.utils.text import slugify
import uuid


def Login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect("admin_index")
        else:
            messages.info(request, "Username Or Password Incorrect")
    context = {}
    if request.user.is_authenticated:
        return redirect("admin_index")
    return render(request, "login.html", context)


@login_required(login_url="admin_login")
def LogoutUser(request):
    logout(request)
    return redirect("admin_login")


def newusers(request):
    if request.method == "POST":
        form = SignUpForm(request.POST, request.FILES) or None
        if form.is_valid():
            form.save()
            return redirect("admin_index")
    else:
        form = SignUpForm()
    context = {"workers": True, "form": form, "title": "New User"}
    return render(request, "signup.html", context)

def index(request):
    return render(request, "index.html")