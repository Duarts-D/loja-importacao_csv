# Generated by Django 4.1.7 on 2023-03-27 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loja', '0003_alter_produtos_manufacturer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produtos',
            name='carrier_plan_type',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='produtos',
            name='color',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='produtos',
            name='model',
            field=models.CharField(max_length=255),
        ),
    ]