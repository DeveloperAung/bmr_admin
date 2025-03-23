from django.http import JsonResponse
from django.shortcuts import render, redirect

from frontend.adminUsers.views import check_auth_request
from frontend.config.api_endpoints import APIEndpoints


def notice_list(request):
    try:
        response = check_auth_request("GET", APIEndpoints.URL_NOTICES, request)
        if response.status_code == 401:  # Unauthorized
            return redirect("login")
        response_body = response.json()
        context = {
            'messages': response_body["message"],
            'data': response_body["data"]["results"],
        }
        return render(request, "notices/notice_list.html", context)
    except Exception as e:
        print('error', e)
        return render(request, "notices/category_list.html", {"error": str(e)})


def notice_create(request):
    try:
        if request.method == "POST":

            title = request.POST["title"]
            description = request.POST["description"]
            from_date = request.POST["from_date"]
            to_date = request.POST["to_date"]
            payload = {
                "title": title,
                "description": description,
                "from_date": from_date,
                "to_date": to_date
            }
            response = check_auth_request("POST", APIEndpoints.URL_NOTICES, request, data=payload)
            if response.status_code == 401:
                return redirect("login")
            response_body = response.json()
            if response.status_code == 201:
                return redirect('notice_list')
            else:
                print('errors', response_body['errors'])
                context = {
                    'errors': response_body['errors'],
                    'message': response_body['message']
                }
                return render(request, "notices/notice_create.html", context)
        else:
            context = {

            }
            return render(request, "notices/notice_create.html", context)
    except Exception as e:
        print('error', e)
        return render(request, "notices/notice_create.html", {"error": str(e)})


def notice_edit(request, uuid):
    try:
        if request.method == "POST":

            title = request.POST["title"]
            description = request.POST["description"]
            from_date = request.POST["from_date"]
            to_date = request.POST["to_date"]
            payload = {
                "title": title,
                "description": description,
                "from_date": from_date,
                "to_date": to_date
            }
            response = check_auth_request("PUT", APIEndpoints.URL_NOICE_DETAILS(uuid), request, data=payload)
            if response.status_code == 401:
                return redirect("login")
            response_body = response.json()
            print('response_body', response_body)
            if response.status_code == 200:
                return redirect('notice_list')
            else:
                context = {
                    'errors': response_body['errors'],
                    'message': response_body['message']
                }
                return render(request, "notices/notice_edit.html", context)
        else:
            response = check_auth_request("GET", APIEndpoints.URL_NOICE_DETAILS(uuid), request)
            response_body = response.json()
            context = {
                'data': response_body['data']
            }
            return render(request, "notices/notice_edit.html", context)
    except Exception as e:
        print('error', e)
        return render(request, "notices/notice_edit.html", {"error": str(e)})


def notice_soft_delete(request, uuid):
    if request.method == "DELETE":
        response = check_auth_request("DELETE", APIEndpoints.URL_NOICE_DETAILS(uuid), request)
        if response.status_code == 401:
            return redirect("login")

        if response.status_code == 200:
            return JsonResponse({"success": True, "message": "Notice deleted successfully."})
        else:
            return JsonResponse(
                {"success": False, "message": f"Failed to delete Notice {response.status_code}."}, status=400
            )
    return JsonResponse({"success": False, "message": "Invalid request method."}, status=405)


def notice_publish_toggle(request, uuid):
    if request.method == "PATCH":

        response = check_auth_request("PATCH", APIEndpoints.URL_NOICE_PUBLISH_TOGGLE(uuid), request)
        decoded_response = response.json()
        if response.status_code == 401:
            return redirect("login")

        if response.status_code == 200:
            return JsonResponse({"success": True, "message": decoded_response["message"]})
        else:
            return JsonResponse(
                {"success": False, "message": f"Failed to delete Notice {response.status_code}."}, status=400
            )
    return JsonResponse({"success": False, "message": "Invalid request method."}, status=405)
