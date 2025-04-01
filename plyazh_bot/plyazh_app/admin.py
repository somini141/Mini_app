from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Country


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'image_preview')
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:  # Для ImageField
            return mark_safe(f'<img src="{obj.image.url}" width="150" />')
        elif obj.image_url:  # Для URLField
            return mark_safe(f'<img src="{obj.image_url}" width="150" />')
        return "Нет изображения"

    image_preview.short_description = "Превью"