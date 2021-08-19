from django.conf import settings
from django.db import models
from django.utils import timezone


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

class Product_detail(models.Model):
    name = models.CharField(max_length=100)
    img = models.ImageField(null=True)
    details = models.TextField(max_length=100,null=True)
    quantity = models.CharField(max_length=20,null=True)
    price = models.IntegerField()

class checkout_detail(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    address = models.TextField()
    pincode = models.IntegerField(max_length=6)
    contact = models.IntegerField()
    time = models.DateTimeField(blank=True,null=True)
    order = models.TextField(null=True)
    total = models.IntegerField(null=True)

    def publish(self):
        self.time = timezone.now()
        self.save()





