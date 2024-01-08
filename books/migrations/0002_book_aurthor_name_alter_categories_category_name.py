# Generated by Django 4.2.7 on 2024-01-07 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='aurthor_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='categories',
            name='category_name',
            field=models.CharField(max_length=100),
        ),
    ]
