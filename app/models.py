from django.contrib.auth.models import User
from django.db import models


class Item(models.Model):
    image = models.ImageField(upload_to="items")
    name = models.CharField(max_length=100, blank=False, null=False, unique=True)
    rate = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False)
    discount_percentage = models.IntegerField()
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    unit = models.CharField(max_length=30, default="SQM")
    height = models.IntegerField(blank=False, null=False)
    width = models.IntegerField(blank=False, null=False)
    sq_mt = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    sq_ft = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.rate <= 1000:
            self.discount_percentage = 5
        else:
            self.discount_percentage = 10
        self.discount_price = (int(self.discount_percentage) / 100) * float(self.rate)
        self.price = float(self.rate) - float(self.discount_price)
        self.sq_mt = (int(self.height) / 100) * (int(self.width) / 100)
        self.sq_ft = float(self.sq_mt) * 10.76391042
        super(Item, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "items"


class Feature(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    feature = models.CharField(max_length=255, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.feature

    class Meta:
        db_table = "features"


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total_rate = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.total_price = float(self.item.price) * int(self.quantity)
        self.total_rate = float(self.item.rate) * int(self.quantity)
        self.total_discount = float(self.total_rate) - float(self.total_price)
        super(Cart, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.username

    class Meta:
        db_table = "carts"


class Notification(models.Model):
    title = models.CharField(max_length=255, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "notifications"