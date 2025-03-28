from django.http import JsonResponse
from django.shortcuts import render, redirect

from frontend.adminUsers.views import check_auth_request
from frontend.config.api_endpoints import APIEndpoints


def subscriber_list(request):
    try:
        response = check_auth_request("GET", APIEndpoints.URL_SINGLE_PAGES, request)
        if response.status_code == 401:  # Unauthorized
            return redirect("login")
        response_body = response.json()
        context = {
            'messages': response_body["message"],
            'data': response_body["data"]["results"],
        }
        return render(request, "subscribers/list.html", context)
    except Exception as e:
        print('error', e)
        return render(request, "subscribers/list.html", {"error": str(e)})


def subscribers_bulk_create(request):
    try:
        if request.method == "POST":

            title = request.POST["title"]
            title_mm = request.POST["title_mm"]
            content_type = request.POST["content_type"]
            content = request.POST["content"]

            payload = {
                "title": title,
                "title_mm": title_mm,
                "content_type": content_type,
                "content": content
            }
            response = check_auth_request("POST", APIEndpoints.URL_SINGLE_PAGES, request, data=payload)
            if response.status_code == 401:
                return redirect("login")
            response_body = response.json()
            if response.status_code == 201:
                return redirect('single_page_list')
            else:
                context = {
                    'errors': response_body['errors'],
                    'message': response_body['message']
                }
                return render(request, "subscribers/create.html", context)
        else:
            context = {

            }
            return render(request, "subscribers/create.html", context)
    except Exception as e:
        print('error', e)
        return render(request, "subscribers/create.html", {"error": str(e)})


def single_page_soft_delete(request, uuid):
    if request.method == "DELETE":
        response = check_auth_request("DELETE", APIEndpoints.URL_SINGLE_PAGE_DETAILS(uuid), request)
        if response.status_code == 401:
            return redirect("login")

        if response.status_code == 200:
            return JsonResponse({"success": True, "message": "Subscriber deleted successfully."})
        else:
            return JsonResponse(
                {"success": False, "message": f"Failed to delete Subscriber {response.status_code}."}, status=400
            )
    return JsonResponse({"success": False, "message": "Invalid request method."}, status=405)


