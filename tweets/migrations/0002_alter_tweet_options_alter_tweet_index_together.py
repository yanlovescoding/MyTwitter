# Generated by Django 5.0.4 on 2024-05-20 13:41

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tweets', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tweet',
            options={'ordering': ('user', 'created_at')},
        ),
        migrations.AlterIndexTogether(
            name='tweet',
            index_together={('user', 'created_at')},
        ),
    ]