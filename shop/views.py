from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template
from django.template import Context
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.csrf import csrf_exempt
from django.utils.text import slugify
from shop import models as shop_models
import uuid
from django.utils import timezone
from shop import forms as shop_forms

def is_valid_form(values):
    valid = True
    for field in values:
        if field == '':
            valid = False
    return valid

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


@login_required
def add_to_cart(request, slug):
    print(request)
    # variations = request.data.get("variations", [])
    item = get_object_or_404(shop_models.Item, slug=slug)
    # minimun_variations_count = shop_models.Variation.objects.filter(item=item).count()
    # if len(variations) < minimun_variations_count:
    #     messages.info(request, "Please specify the required variation types.")
    # order_item = shop_models.OrderItem.objects.filter(
    #     item=item,
    #     user=request.user,
    #     ordered=False
    # )
    # for v in variations:
    #     order_item_qs = order_item_qs.filter(Q(item_variations__exact=v))

    # if order_item_qs.exists():
    #     order_item = order_item_qs.first()
    #     order_item.quantity += 1
    #     order_item.save()
    # else:
    #     order_item = shop_models.OrderItem.objects.create(
    #         item=item, user=request.user, ordered=False, quantity=1
    #     )
    #     order_item.item_variations.add(*variations)
    #     order_item.save()

    # order_qs = shop_models.Order.objects.filter(user=request.user, ordered=False)
    order_item, created = shop_models.OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = shop_models.Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect("shop:order-summary")
        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect("shop:order-summary")
    else:
        ordered_date = timezone.now()
        order = shop_models.Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect("shop:order-summary")

def ordersummary(request):
    try:
        order = shop_models.Order.objects.get(ordered=False)
        context = {
            'items': order
        }
        return render(request, 'order-summary.html', context)
    except ObjectDoesNotExist:
        messages.warning(request, "You do not have an active order")
        return redirect("/")
    # return render(request, "order-summary.html")

def checkout(request):
    if request.method == "GET":
        form = shop_forms.CheckoutForm()
        order = shop_models.Order.objects.get(user=request.user, ordered=False)
        
        context = {
                "order":order,
                'form': form
                }
        return render(request, 'check-out.html',context)
    else:
        form = shop_forms.CheckoutForm(request.POST or None)
        try:
            order = shop_models.Order.objects.get(user=request.user, ordered=False)
            if form.is_valid():
                print("User is entering a new shipping address")
                shipping_address1 = form.cleaned_data.get(
                    'shipping_address')
                shipping_address2 = form.cleaned_data.get(
                    'shipping_address2')
                shipping_zip = form.cleaned_data.get('shipping_zip')

                if is_valid_form([shipping_address1, shipping_zip]):
                    shipping_address = shop_models.Address(
                        user=request.user,
                        street_address=shipping_address1,
                        apartment_address=shipping_address2,
                        country="india",
                        zip=shipping_zip,
                        address_type='S'
                    )
                    shipping_address.save()

                    order.shipping_address = shipping_address
                    order.save()

                else:
                    messages.info(
                        request, "Please fill in the required shipping address fields")


                payment_option = form.cleaned_data.get('payment_option')

                if payment_option == 'S':
                    return redirect('shop:payment', payment_option='stripe')
                elif payment_option == 'P':
                    return redirect('shop:payment', payment_option='paypal')
                else:
                    messages.warning(
                        request, "Invalid payment option selected")
                    return redirect('shop:checkout')
            else:
                return redirect('shop:checkout')
        except ObjectDoesNotExist:
            messages.warning(request, "You do not have an active order")
            return redirect("shop:order-summary")

def payment(request,payment_option):
    if request.method == "GET":
        form = shop_forms.PaymentForm()
        context = {
                'form': form
                }
        return render(request, 'payment.html',context)
    else:
        order = shop_models.Order.objects.get(ordered=False)
        obj = shop_models.Payment.objects.create(
            stripe_charge_id = uuid.uuid1(),
            user = request.user,
            amount = order.get_total()
        )
        order.payment = obj
        order.ordered = True
        order.save()
        return redirect("/")

def admin(request):
    order = shop_models.Order.objects.filter(ordered=True)
    context = {
                'orders': order
            }
    return render(request, 'admin-order.html',context)

        