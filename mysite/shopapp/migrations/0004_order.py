# Generated by Django 4.2.3 on 2023-09-11 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopapp', '0003_product_archieved'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('delivery_adress', models.TextField(blank=True)),
                ('promocode', models.CharField(blank=True, max_length=28)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
