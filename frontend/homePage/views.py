from django.shortcuts import render


def home_setting_video_listing(request):
    return render(request, 'homePage/home_settings.html')


def home_setting_video_edit(request):
    return render(request, 'homePage/home_setting_video_edit.html')


def home_page_banner_list(request):
    return render(request, 'homePage/home_banner_order.html')
