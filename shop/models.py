from django.db import models
from django.conf import settings
from django_countries.fields import CountryField
from django.shortcuts import reverse
class Item(models.Model):
    length = 255
    productName = models.CharField(max_length=length)
    productDescription = models.CharField(max_length=length)
    unitPrice = models.IntegerField()
    discountPrice = models.FloatField(blank=True, null=True)
    unitsInStock = models.CharField(max_length=length)
    logo = models.ImageField(blank=True, null=True)
    stl = models.FileField(blank=True, null=True)
    slug = models.CharField(max_length=length, unique=True)

    def __str__(self):
        return self.productName

    def get_absolute_url(self):
        return reverse("shop:product", kwargs={"slug": self.slug})

    def get_add_to_cart_url(self):
        return reverse("shop:add-to-cart", kwargs={"slug": self.slug})

    def get_remove_from_cart_url(self):
        return reverse("shop:remove-from-cart", kwargs={"slug": self.slug})

    @property
    def image(self):
        return self.itemimage_set.all()

class ItemImage(models.Model):
    length = 255
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    image = models.ImageField()  # image

    def __str__(self):
        return self.item.productName

class Variation(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)  # material
    unitPrise = models.IntegerField(blank=True, null=True)

    class Meta:
        unique_together = ("item", "name")

    def __str__(self):
        return self.name


class ItemVariation(models.Model):
    variation = models.ForeignKey(Variation, on_delete=models.CASCADE)
    value = models.CharField(max_length=50)  # size
    attachment = models.CharField(blank=True, null=True, max_length=255)

    class Meta:
        unique_together = ("variation", "value")

    def __str__(self):
        return self.value


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    variation = models.ForeignKey(
        Variation, on_delete=models.CASCADE, blank=True, null=True
    )
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    item_variations = models.ManyToManyField(ItemVariation)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.productName}"

    def get_total_item_price(self):
        return self.quantity * self.item.unitPrice

    def get_total_discount_item_price(self):
        return self.quantity * self.item.discountPrice

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.item.discountPrice:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()


class Order(models.Model):
    length = 255
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ref_code = models.CharField(max_length=length, blank=True, null=True)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    shipping_address = models.ForeignKey(
        "Address",
        related_name="shipping_address",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    billing_address = models.ForeignKey(
        "Address",
        related_name="billing_address",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    payment = models.ForeignKey(
        "Payment",
        related_name="payment",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    coupon = models.ForeignKey(
        "Coupon",
        related_name="coupon",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    being_delivered = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)

    def __str__(self):
        return self.user.email
    
    def get_gst(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_total_item_price()
        return (float(total)*0.18)

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        if self.coupon:
            total -= self.coupon.amount
        return float(total) + self.get_gst()

    def get_total_amount(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_total_item_price()
        return float(total)
    def get_total_discount(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_amount_saved()
        return float(total)

class Address(models.Model):
    ADDRESS_CHOICES = (
        ("B", "Billing"),
        ("S", "Shipping"),
    )
    length = 255
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=length)
    apartment_address = models.CharField(max_length=length)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=length)
    address_type = models.CharField(max_length=length, choices=ADDRESS_CHOICES)
    default_addr = models.BooleanField(default=False)

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name_plural = "Addresses"


class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email


class Coupon(models.Model):
    code = models.CharField(max_length=15)
    amount = models.FloatField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.code
