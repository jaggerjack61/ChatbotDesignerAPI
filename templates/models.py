from django.db import models


# Create your models here.

class Template(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class TemplatePage(models.Model):
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=10)
    header = models.CharField(max_length=100, null=True)
    body = models.CharField(max_length=500)
    footer = models.CharField(max_length=100, null=True)
    menu_title = models.CharField(max_length=10, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    template = models.ForeignKey(Template, on_delete=models.CASCADE, null=True)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return self.name+" "+self.type+" type template"


class TemplateOption(models.Model):
    template_page = models.ForeignKey(TemplatePage, on_delete=models.CASCADE, null=True)
    type = models.CharField(max_length=10)
    text = models.CharField(max_length=20)
    value = models.CharField(max_length=20)
    description = models.CharField(max_length=40, null=True)

    def __str__(self):
        return self.type+" "+self.value


class Setting(models.Model):
    message_limit = models.IntegerField(default=250)


class Number(models.Model):
    phone_number = models.CharField(max_length=15)
    state = models.CharField(max_length=200, default="initial")
    opt_in = models.BooleanField(null=True)



