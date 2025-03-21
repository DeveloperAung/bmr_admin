from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect

from frontend.adminUsers.views import check_auth_request
from frontend.config.api_endpoints import APIEndpoints


def home_setting_video_listing(request):
    return render(request, 'homePage/home_settings.html')


def home_setting_video_edit(request):
    return render(request, 'homePage/home_setting_video_edit.html')


def home_page_banner_order(request):
    try:
        response = check_auth_request("GET", APIEndpoints.URL_HOME_BANNER_LIST, request)
        if response.status_code == 401:
            return redirect("login")
        response_body = response.json()
        context = {
            'messages': response_body["message"],
            'data': response_body["data"]["results"],
        }
        return render(request, "homePage/home_banner_order.html", context)
    except Exception as e:
        print('error', e)
        return render(request, "homePage/home_banner_order.html", {"error": str(e)})


def home_page_banner_reorder(request):
    try:
        import json
        payload = json.loads(request.body)
        response = check_auth_request("POST", APIEndpoints.URL_HOME_BANNER_REORDER, request, data=payload)
        if response.status_code == 401:
            return redirect("login")
        if response.status_code == 200:
            return JsonResponse(response.json())
    except Exception as e:
        print('error', e)
        return JsonResponse(e)
