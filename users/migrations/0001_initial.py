# Generated by Django 3.2.4 on 2021-06-07 18:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('items', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_method', models.CharField(blank=True, max_length=100, null=True)),
                ('tax_price', models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True)),
                ('shipping_price', models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True)),
                ('total_price', models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True)),
                ('is_paid', models.BooleanField(blank=True, default=False, null=True)),
                ('paid_at', models.DateTimeField(blank=True, null=True)),
                ('is_delivered', models.BooleanField(blank=True, default=False, null=True)),
                ('delivered_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.CharField(blank=True, max_length=2000, null=True)),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('quantity', models.IntegerField(default=0, null=True)),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True)),
                ('cart', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.cart')),
                ('item', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='items.itemdetailpage')),
            ],
        ),
        migrations.CreateModel(
            name='ShippingAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(blank=True, max_length=200, null=True)),
                ('city', models.CharField(blank=True, max_length=100, null=True)),
                ('postal_code', models.CharField(blank=True, max_length=10, null=True)),
                ('country', models.CharField(blank=True, max_length=100, null=True)),
                ('shipping_price', models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True)),
                ('order', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.order')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('rating', models.IntegerField(default=0, null=True)),
                ('comment', models.TextField(blank=True, max_length=2000, null=True)),
                ('item', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='items.itemdetailpage')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
