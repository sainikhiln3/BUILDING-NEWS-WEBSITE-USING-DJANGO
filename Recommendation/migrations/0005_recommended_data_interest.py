# Generated by Django 3.2 on 2021-05-21 05:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Recommendation', '0004_auto_20210521_1110'),
    ]

    operations = [
        migrations.AddField(
            model_name='recommended_data',
            name='interest',
            field=models.TextField(null=True),
        ),
    ]
