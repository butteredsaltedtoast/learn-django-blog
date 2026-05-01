from celery import shared_task
from django.utils import timezone
from .models import Post

@shared_task
def update_post_dates():
    Post.objects.all().update(date=timezone.now().date())