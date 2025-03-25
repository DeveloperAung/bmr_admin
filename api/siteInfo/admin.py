from django.contrib import admin
from . models import SiteInfo, SocialMedia


admin.site.register(SiteInfo)


@admin.register(SocialMedia)
class SocialMediaAdmin(admin.ModelAdmin):
    list_display = ('title', 'short_title', 'social_media_link', 'preview_icon')
    search_fields = ('title', 'short_title')
    readonly_fields = ('preview_icon',)

    def preview_icon(self, obj):
        if obj.social_media_ico:
            return f'<img src="{obj.social_media_ico.url}" width="30" height="30" />'
        return "No Icon"
    preview_icon.short_description = 'Icon'
    preview_icon.allow_tags = True

    def formfield_for_dbfield(self, db_field, **kwargs):
        from django.utils.safestring import mark_safe
        formfield = super().formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'social_media_ico':
            if 'request' in kwargs:
                obj = kwargs['request'].resolver_match.kwargs.get('object_id')
                if obj:
                    formfield.help_text = mark_safe(f'<br><img src="{obj.social_media_ico.url}" width="100"/>')
        return formfield
