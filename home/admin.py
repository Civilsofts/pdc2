from django.contrib import admin
from .models import Subscriber

# Register your models here.

@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ['email', 'created_at']
    search_fields = ['email']
    readonly_fields = ['created_at']
