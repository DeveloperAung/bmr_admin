from django.contrib import admin
from django.template.response import TemplateResponse
from django.urls import path
from .models import HomeBanner, Category


class HomeBannerAdmin(admin.ModelAdmin):
    list_display = ['title', 'order_index', 'category']

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('reorder/', self.admin_site.admin_view(self.reorder_view), name='homebanner_reorder'),
        ]
        return custom_urls + urls

    def reorder_view(self, request):
        banners = HomeBanner.objects.order_by('order_index')
        context = dict(
            self.admin_site.each_context(request),
            banners=banners
        )
        return TemplateResponse(request, "admin/homebanner_reorder.html", context)


admin.site.register(HomeBanner, HomeBannerAdmin)
admin.site.register(Category)
