from django.contrib import admin
from django.utils.html import mark_safe
from django.utils.text import slugify
from .models import Subscriber, ServiceCategory, ServiceItem


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ['email', 'created_at']
    search_fields = ['email']
    readonly_fields = ['created_at']


class ServiceItemInline(admin.StackedInline):
    model = ServiceItem
    extra = 0
    fields = [
        ('name', 'icon_class'),
        'short_description',
        ('url', 'order', 'is_active'),
    ]
    ordering = ['order']
    classes = ['collapse']


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = [
        'order', 'icon_preview', 'name', 'slug',
        'is_active', 'coming_soon', 'item_count',
    ]
    list_display_links = ['name']
    list_editable = ['order', 'is_active', 'coming_soon']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ServiceItemInline]

    fieldsets = (
        ('Əsas Məlumatlar', {
            'fields': (
                ('name', 'slug'),
                ('icon_class', 'order'),
                ('is_active', 'coming_soon'),
            )
        }),
        ('Təsvirlər', {
            'fields': ('short_description', 'description'),
        }),
        ('Şəkillər', {
            'fields': (('image', 'image_preview'), ('banner_image', 'banner_preview')),
        }),
    )
    readonly_fields = ['image_preview', 'banner_preview']

    def icon_preview(self, obj):
        if obj.icon_class:
            return mark_safe(f'<i class="{obj.icon_class}" style="font-size:18px;color:#f5b754;"></i>')
        return '-'
    icon_preview.short_description = 'İkon'

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" style="max-height:120px;border-radius:8px;"/>')
        return 'Şəkil yüklənməyib'
    image_preview.short_description = 'Şəkil önizləmə'

    def banner_preview(self, obj):
        if obj.banner_image:
            return mark_safe(f'<img src="{obj.banner_image.url}" style="max-height:120px;border-radius:8px;"/>')
        return 'Şəkil yüklənməyib'
    banner_preview.short_description = 'Banner önizləmə'

    def item_count(self, obj):
        return obj.items.count()
    item_count.short_description = 'Xidmət sayı'

    class Media:
        css = {'all': ('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css',)}


@admin.register(ServiceItem)
class ServiceItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'icon_preview', 'name', 'category', 'short_desc', 'is_active']
    list_display_links = ['name']
    list_editable = ['order', 'is_active']
    list_filter = ['category', 'is_active']
    search_fields = ['name', 'category__name']
    fields = [
        ('category', 'order', 'is_active'),
        ('name', 'icon_class'),
        'short_description',
        'url',
    ]

    def icon_preview(self, obj):
        if obj.icon_class:
            return mark_safe(f'<i class="{obj.icon_class}" style="font-size:16px;color:#f5b754;"></i>')
        return '-'
    icon_preview.short_description = 'İkon'

    def short_desc(self, obj):
        if obj.short_description:
            return obj.short_description[:60] + ('...' if len(obj.short_description) > 60 else '')
        return '-'
    short_desc.short_description = 'Qısa təsvir'

    class Media:
        css = {'all': ('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css',)}
