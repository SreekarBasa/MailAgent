# views.py
from django.shortcuts import render
from .models import Email

def inbox_view(request):
    # Single query to fetch all emails, ordered by date descending
    # This reduces database hits compared to separate queries per priority
    emails = Email.objects.all().order_by('-date')
    # Filter emails by priority in memory to avoid multiple queries
    high = emails.filter(priority='high')
    medium = emails.filter(priority='medium')
    low = emails.filter(priority='low')
    return render(request, 'mailapp/inbox.html', {
        'high': high,
        'medium': medium,
        'low': low
    })