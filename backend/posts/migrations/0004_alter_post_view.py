# Generated by Django 4.2.11 on 2024-05-11 04:20

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0003_alter_post_upvote'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='view',
            field=models.ManyToManyField(blank=True, related_name='viewed_posts', to=settings.AUTH_USER_MODEL),
        ),
    ]