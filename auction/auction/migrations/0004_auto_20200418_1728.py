# Generated by Django 3.0.5 on 2020-04-18 17:28

from decimal import Decimal
from django.db import migrations
import djmoney.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('auction', '0003_auto_20200418_1703'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionitem',
            name='base_price',
            field=djmoney.models.fields.MoneyField(decimal_places=2, default=Decimal('0.00'), help_text='Starting price for the auction.', max_digits=19),
        ),
    ]
