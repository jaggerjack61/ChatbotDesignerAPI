from django.db import models

# Create your models here


class Number(models.Model):
    phone_number = models.CharField(max_length=20, unique=True)
    opt_in_status = models.BooleanField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)


class Batch(models.Model):
    template = models.CharField(max_length=100)
    language = models.CharField(max_length=20)
    status = models.CharField(max_length=20, default='ongoing')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)


class MessageLog(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    number = models.ForeignKey(Number, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
