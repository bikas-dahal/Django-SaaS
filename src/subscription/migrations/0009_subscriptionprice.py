# Generated by Django 5.0.6 on 2024-06-18 03:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscription', '0008_subscription_stripe_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubscriptionPrice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('interval', models.CharField(choices=[('month', 'Monthly'), ('year', 'Annually')], default='month', max_length=120)),
                ('price', models.DecimalField(decimal_places=2, default=99.99, max_digits=10)),
                ('stripe_id', models.CharField(blank=True, max_length=50, null=True)),
                ('subscription', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='subscription.subscription')),
            ],
        ),
    ]
