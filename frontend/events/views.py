from django.http import JsonResponse
from django.shortcuts import render, redirect
import requests
from frontend.adminUsers.views import get_auth_headers, check_auth_request
from frontend.config.api_endpoints import APIEndpoints
from frontend.events.forms import EventForm


def event_category_list(request):
    try:
        event_response = check_auth_request("GET", APIEndpoints.URL_EVENT_CATEGORY, request)
        if event_response.status_code == 401:  # Unauthorized
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


def event_category_create(request):
    try:
        if request.method == "POST":

            title = request.POST["title"]
            payload = {
                "title": title,
            }
            response = check_auth_request("POST", APIEndpoints.URL_EVENT_CATEGORY, request, data=payload)
            if response.status_code == 401:  # Unauthorized
                return redirect("login")
            response_body = response.json()
            if response.status_code == 201:
                return redirect('event_category_list')
            else:
                context = {
                    'errors': response_body['errors'],
                    'message': response_body['message']
                }
                return render(request, "events/category_create.html", context)
        else:
            context = {

            }
            return render(request, "events/category_create.html", context)
    except Exception as e:
        print('error', e)
        return render(request, "events/category_create.html", {"error": str(e)})


def event_category_edit(request, uuid):
    try:
        if request.method == "POST":

            title = request.POST["title"]
            payload = {
                "title": title,
            }
            response = check_auth_request("PUT", APIEndpoints.URL_EVENT_CATEGORY_DETAILS(uuid), request, data=payload)
            if response.status_code == 401:
                return redirect("login")
            response_body = response.json()
            if response.status_code == 200:
                return redirect('event_category_list')
            else:
                context = {
                    'errors': response_body['errors'],
                    'message': response_body['message']
                }
                return render(request, "events/category_edit.html", context)
        else:
            response = check_auth_request("GET", APIEndpoints.URL_EVENT_CATEGORY_DETAILS(uuid), request)
            response_body = response.json()
            context = {
                'data': response_body['data']
            }
            return render(request, "events/category_edit.html", context)
    except Exception as e:
        print('error', e)
        return render(request, "events/category_edit.html", {"error": str(e)})


def event_category_soft_delete(request, uuid):
    if request.method == "DELETE":
        response = check_auth_request("DELETE", APIEndpoints.URL_EVENT_CATEGORY_DETAILS(uuid), request)
        if response.status_code == 401:
            return redirect("login")

        if response.status_code == 200:
            return JsonResponse({"success": True, "message": "Category deleted successfully."})
        else:
            return JsonResponse(
                {"success": False, "message": f"Failed to delete Category {response.status_code}."}, status=400
            )
    return JsonResponse({"success": False, "message": "Invalid request method."}, status=405)


def event_sub_category_list(request):
    try:
        response = check_auth_request("GET", APIEndpoints.URL_EVENT_SUB_CATEGORY, request)
        if response.status_code == 401:
            return redirect("login")

        event_response_body = response.json()
        context = {
            'messages': event_response_body["message"],
            'data': event_response_body["data"]["results"],
        }
        return render(request, "events/sub_category_list.html", context)
    except Exception as e:
        print('error', e)
        return render(request, "events/sub_category_list.html", {"error": str(e)})


def event_sub_category_create(request):
    try:
        if request.method == "POST":

            title = request.POST["title"]
            category = request.POST["category"]

            payload = {
                "title": title,
                "event_category": category
            }
            response = check_auth_request("POST", APIEndpoints.URL_EVENT_SUB_CATEGORY, request, data=payload)
            if response.status_code == 401:
                return redirect("login")
            response_body = response.json()
            if response.status_code == 201:
                return redirect('event_sub_category_list')
            else:
                context = {
                    'errors': response_body['errors'],
                    'message': response_body['message']
                }
                return render(request, "events/sub_category_create.html", context)
        else:
            response_category = check_auth_request("GET", APIEndpoints.URL_EVENT_CATEGORY, request)
            response_category_body = response_category.json()
            context = {
                'errors': response_category_body['errors'],
                'message': response_category_body['message'],
                'categories': response_category_body['data']['results']
            }
            return render(request, "events/sub_category_create.html", context)
    except Exception as e:
        print('error', e)
        return render(request, "events/sub_category_create.html", {"error": str(e)})


def event_sub_category_edit(request, uuid):
    try:
        if request.method == "POST":

            title = request.POST["title"]
            category = request.POST["category"]

            payload = {
                "title": title,
                "event_category": category
            }
            response = check_auth_request("PUT", APIEndpoints.URL_EVENT_SUB_CATEGORY_DETAILS(uuid), request, data=payload)
            if response.status_code == 401:
                return redirect("login")
            response_body = response.json()
            if response.status_code == 200:
                return redirect('event_sub_category_list')
            else:
                context = {
                    'errors': response_body['errors'],
                    'message': response_body['message']
                }
                return render(request, "events/sub_category_edit.html", context)
        else:
            response = check_auth_request("GET", APIEndpoints.URL_EVENT_SUB_CATEGORY_DETAILS(uuid), request)
            response_body = response.json()
            response_category = check_auth_request("GET", APIEndpoints.URL_EVENT_CATEGORY, request)
            response_category_body = response_category.json()
            context = {
                'data': response_body['data'],
                'categories': response_category_body['data']['results']
            }
            return render(request, "events/sub_category_edit.html", context)
    except Exception as e:
        print('error', e)
        return render(request, "events/sub_category_edit.html", {"error": str(e)})


def event_sub_category_soft_delete(request, uuid):
    if request.method == "DELETE":
        response = check_auth_request("DELETE", APIEndpoints.URL_EVENT_SUB_CATEGORY_DETAILS(uuid), request)
        if response.status_code == 401:
            return redirect("login")
        if response.status_code == 200:
            return JsonResponse({"success": True, "message": "Sub Category deleted successfully."})
        else:
            return JsonResponse(
                {"success": False, "message": f"Failed to delete Sub Category {response.status_code}."}, status=400
            )
    return JsonResponse({"success": False, "message": "Invalid request method."}, status=405)


def dhamma_class_list(request):  # event
    try:
        headers = get_auth_headers(request)

        response = requests.get(APIEndpoints.URL_EVENTS, headers=headers)

        if response.status_code == 401:
            return redirect("login")

        event_response_body = response.json()
        print('response', event_response_body)
        context = {
            'messages': event_response_body["message"],
            'data': event_response_body["data"]["results"],
        }
        return render(request, "events/list.html", context)
    except Exception as e:
        print('error', e)
        return render(request, "events/list.html", {"error": str(e)})
    # return render(request, 'events/list.html')


def dhamma_class_create(request):   # event create
    # try:
    #     if request.method == "POST":
    #
    #         title = request.POST["title"]
    #         title_mm = request.POST["title_mm"]
    #         content_type = request.POST["content_type"]
    #         content = request.POST["content"]
    #
    #         payload = {
    #             "title": title,
    #             "title_mm": title_mm,
    #             "content_type": content_type,
    #             "content": content
    #         }
    #         response = check_auth_request("POST", APIEndpoints.URL_SINGLE_PAGES, request, data=payload)
    #         if response.status_code == 401:
    #             return redirect("login")
    #         response_body = response.json()
    #         if response.status_code == 201:
    #             return redirect('single_page_list')
    #         else:
    #             context = {
    #                 'errors': response_body['errors'],
    #                 'message': response_body['message']
    #             }
    #             return render(request, "events/create.html", context)
    #     else:
    #         context = {
    #
    #         }
    #         return render(request, "events/create.html", context)
    # except Exception as e:
    #     print('error', e)
    #     return render(request, "events/create.html", {"error": str(e)})
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
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
