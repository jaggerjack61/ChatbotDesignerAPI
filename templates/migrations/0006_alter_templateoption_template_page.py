# Generated by Django 5.0.3 on 2024-03-22 07:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('templates', '0005_alter_templatepage_body'),
    ]

    operations = [
        migrations.AlterField(
            model_name='templateoption',
            name='template_page',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='templates.templatepage'),
        ),
    ]
