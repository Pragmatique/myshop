# Generated by Django 2.2 on 2019-05-03 22:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_auto_20190504_0016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='userid',
            field=models.IntegerField(default=None, null=True),
        ),
    ]
