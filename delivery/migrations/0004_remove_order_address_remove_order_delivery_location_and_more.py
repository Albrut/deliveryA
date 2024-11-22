# Generated by Django 5.1.3 on 2024-11-22 22:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0003_alter_order_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='address',
        ),
        migrations.RemoveField(
            model_name='order',
            name='delivery_location',
        ),
        migrations.AddField(
            model_name='user',
            name='car_type',
            field=models.CharField(blank=True, choices=[('light', 'Легковая'), ('middle', 'Минивэн'), ('hard', 'Грузовая')], default='light', max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='latitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='longitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='status',
            field=models.CharField(default='available', max_length=20),
        ),
    ]