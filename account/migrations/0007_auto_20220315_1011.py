# Generated by Django 3.2.8 on 2022-03-15 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_user'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User',
        ),
        migrations.AddField(
            model_name='profile',
            name='name',
            field=models.CharField(default='', max_length=64),
            preserve_default=False,
        ),
    ]
