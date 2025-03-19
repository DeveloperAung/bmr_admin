from django.shortcuts import render, redirect
import requests
from frontend.adminUsers.views import get_auth_headers
from frontend.config.api_endpoints import APIEndpoints
from frontend.events.forms import EventForm


def event_category_list(request):
    try:
        headers = get_auth_headers(request)

        event_response = requests.get(APIEndpoints.URL_EVENT_CATEGORY_LIST, headers=headers)

        if event_response.status_code == 401:
            return redirect("login")
        event_response_body = event_response.json()
        context = {
            'messages': event_response_body["message"],
            'data': event_response_body["data"]["results"],
        }
        return render(request, "events/category_list.html", context)
    except Exception as e:
        print('error', e)
        return render(request, "events/category_list.html", {"error": str(e)})


def event_sub_category_list(request):
    try:
        headers = get_auth_headers(request)

        event_response = requests.get(APIEndpoints.URL_EVENT_SUB_CATEGORY_LIST, headers=headers)

        if event_response.status_code == 401:
            return redirect("login")
        event_response_body = event_response.json()
        print('event_sub_response', event_response_body)
        context = {
            'messages': event_response_body["message"],
            'data': event_response_body["data"]["results"],
        }
        return render(request, "events/sub_category_list.html", context)
    except Exception as e:
        print('error', e)
        return render(request, "events/sub_category_list.html", {"error": str(e)})


def post_category(request):
    return render(request, '')


def dhamma_class_list(request):  # event
    try:
        headers = get_auth_headers(request)

        event_response = requests.get(APIEndpoints.URL_EVENT_LIST, headers=headers)

        if event_response.status_code == 401:
            return redirect("login")
        event_response_body = event_response.json()
        context = {
            'messages': event_response_body["message"],
            'data': event_response_body["data"]["results"],
        }
        return render(request, "events/list.html", context)
    except Exception as e:
        print('error', e)
        return render(request, "events/list.html", {"error": str(e)})
    return render(request, 'events/list.html')


def dhamma_class_create(request):   # event create
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user
            event.save()
            return redirect("dhamma_class_list")
    else:
        form = EventForm()

    return render(request, 'events/create.html', {"form": form})


def dhamma_class_details(request, event_uuid):
    headers = get_auth_headers(request)
    try:
        response = requests.get(APIEndpoints.URL_EVENT_DETAILS(event_uuid), headers=headers)
        # response_category = request.get(APIEndpoints.URL_EVENT_CATEGORY_LIST, headers=headers)
        # print('response_category', response_category)
        if response.status_code == 401:
            return redirect("login")

        response_body = response.json()
        # response_category_body = response_category.json()

        context = {
            'messages': response_body["message"],
            # 'categories': response_category_body["data"],
            'data': response_body["data"]
        }
        return render(request, "events/edit.html", context)
    except Exception as e:
        print('event details error', e)
        return render(request, "events/edit.html", {"error": str(e)})
    # """View to show event details"""
    # event = get_object_or_404(Event, id=event_id, is_active=True)
    # event_dates = EventDate.objects.filter(event=event)
    # return render(request, "events/event_detail.html", {"event": event, "event_dates": event_dates})
