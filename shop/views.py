from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template
from django.template import Context
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.csrf import csrf_exempt
from django.utils.text import slugify
from shop import models as shop_models
import uuid


def index(request):
    item_list = shop_models.Item.objects.all()
    context = {"items": item_list}
    return render(request, "index.html",context)

def productDetails(request,slug):
    # print(slug)
    item = shop_models.Item.objects.get(slug = slug)
    print(item)
    context = {"item": item}
    return render(request, "product-details.html",context)
    