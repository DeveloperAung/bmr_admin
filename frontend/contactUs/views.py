import requests
from django.http import JsonResponse
from django.shortcuts import render, redirect

from frontend.adminUsers.views import get_auth_headers
from frontend.config.api_endpoints import APIEndpoints


def contact_us_list(request):
    try:
        headers = get_auth_headers(request)
        response = requests.get(APIEndpoints.URL_CONTACT_US_LIST, headers=headers)
        if response.status_code == 401 or response.status_code == 400:
            return redirect("login")
        response_body = response.json()
        context = {
            'messages': response_body["message"],
            'data': response_body["data"]["results"]
        }
        return render(request, "contactUs/list.html", context)
    except Exception as e:
        print('error', e)
        return render(request, "contactUs/list.html", {"error": str(e)})


def contact_us_edit(request, uuid):
    headers = get_auth_headers(request)
    if request.method == "POST":
        try:
            reply_message = request.POST.get("reply_message")

            payload = {
                "reply_message": reply_message
            }
            # Send PUT request to update the contact message
            response = requests.put(APIEndpoints.URL_CONTACT_US_DETAIL(uuid), json=payload, headers=headers)

            response_body = response.json()
            if response.status_code == 401 or response.status_code == 400:
                return redirect("login")
            if response.status_code == 200:
                return redirect("contact_us_list")
            else:
                return render(request, "contactUs/edit.html", {"error": response_body["message"]})

        except Exception as e:
            print("contact_us_edit_error", e)
            return render(request, "contactUs/edit.html", {"error": str(e)})
    try:
        response = requests.get(APIEndpoints.URL_CONTACT_US_DETAIL(uuid), headers=headers)
        response_body = response.json()
        context = {
            'messages': response_body["message"],
            'data': response_body["data"]
        }
        return render(request, "contactUs/edit.html", context)
    except Exception as e:
        print('contact_us_error', e)
        return render(request, "contactUs/edit.html", {"error": str(e)})


def soft_delete_contact(request, uuid):
    """Soft delete a contact message via AJAX"""
    if request.method == "DELETE":
        headers = get_auth_headers(request)
        response = requests.delete(APIEndpoints.URL_CONTACT_US_DETAIL(uuid), headers=headers)
        if response.status_code == 401 or response.status_code == 400:
            return redirect("login")
        if response.status_code == 200:
            return JsonResponse({"success": True, "message": "Message deleted successfully."})
        else:
            return JsonResponse({"success": False, "message": f"Failed to delete message {response.status_code}."}, status=400)

    return JsonResponse({"success": False, "message": "Invalid request method."}, status=405)

