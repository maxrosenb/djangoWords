# Generated by Django 3.1.7 on 2021-03-22 00:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('words', '0005_auto_20210322_0043'),
    ]

    operations = [
        migrations.AlterField(
            model_name='word',
            name='creator',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='word', to=settings.AUTH_USER_MODEL),
        ),
    ]
