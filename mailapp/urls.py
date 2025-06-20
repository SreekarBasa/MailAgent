from django.urls import path
from .views import inbox_view

urlpatterns = [
    path('', inbox_view, name='inbox'),
    # path('classified/', classified_view, name='classified'),
    # path('mark-read/<int:email_id>/', mark_email_read, name='mark_email_read'),
]