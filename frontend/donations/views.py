import requests
from django.http import JsonResponse
from django.shortcuts import render, redirect

from frontend.adminUsers.views import check_auth_request, get_auth_headers
from frontend.config.api_endpoints import APIEndpoints


def donation_category_list(request):
    try:
        headers = get_auth_headers(request)
        response = requests.get(APIEndpoints.URL_DONATION_CATEGORY, headers=headers)

        if response.status_code == 401:
            return redirect("login")

        donation_response_body = response.json()
        context = {
            'messages': donation_response_body["message"],
            'data': donation_response_body["data"]["results"],
        }
        return render(request, "donations/category_list.html", context)
    except Exception as e:
        print('Donation Category List Error:', e)
        return render(request, "donations/category_list.html", {"error": str(e)})


def donation_category_create(request):
    try:
        if request.method == "POST":

            title = request.POST["title"]
            payload = {
                "title": title,
            }
            response = check_auth_request("POST", APIEndpoints.URL_DONATION_CATEGORY, request, data=payload)

            if response.status_code == 401:  # Unauthorized
                return redirect("login")

            response_body = response.json()
            if response.status_code == 201:
                return redirect('donation_category_list')
            else:
                context = {
                    'errors': response_body['errors'],
                    'message': response_body['message']
                }
                return render(request, "donations/category_create.html", context)
        else:
            context = {

            }
            return render(request, "donations/category_create.html", context)
    except Exception as e:
        print('Donation Category Create Error:', e)
        return render(request, "donations/category_create.html", {"error": str(e)})


def donation_category_edit(request, uuid):
    try:
        if request.method == "POST":

            title = request.POST["title"]
            payload = {
                "title": title,
            }
            response = check_auth_request("PUT", APIEndpoints.URL_DONATION_CATEGORY_DETAILS(uuid), request, data=payload)

            if response.status_code == 401:  # Unauthorized
                return redirect("login")

            response_body = response.json()
            if response.status_code == 200:
                return redirect('donation_category_list')
            else:
                context = {
                    'errors': response_body['errors'],
                    'message': response_body['message']
                }
                return render(request, "donations/category_edit.html", context)
        else:
            response = check_auth_request("GET", APIEndpoints.URL_DONATION_CATEGORY_DETAILS(uuid), request)
            response_body = response.json()
            context = {
                'data': response_body['data']
            }
            return render(request, "donations/category_edit.html", context)
    except Exception as e:
        print('Donation Category Edit Error:', e)
        return render(request, "donations/category_edit.html", {"error": str(e)})


def donation_category_soft_delete(request, uuid):
    if request.method == "DELETE":
        response = check_auth_request("DELETE", APIEndpoints.URL_DONATION_CATEGORY_DETAILS(uuid), request)
        if response.status_code == 401:  # Unauthorized
            return redirect("login")

        if response.status_code == 200:
            return JsonResponse({"success": True, "message": "Category deleted successfully."})
        else:
            return JsonResponse(
                {"success": False, "message": f"Failed to delete Category {response.status_code}."}, status=400
            )
    return JsonResponse({"success": False, "message": "Invalid request method."}, status=405)


def donation_sub_category_list(request):
    try:
        response = check_auth_request("GET", APIEndpoints.URL_DONATION_SUB_CATEGORY, request)
        if response.status_code == 401:  # Unauthorized
            return redirect("login")

        donation_response_body = response.json()
        context = {
            'messages': donation_response_body["message"],
            'data': donation_response_body["data"]["results"],
        }
        return render(request, "donations/sub_category_list.html", context)
    except Exception as e:
        print('Donation Sub Category List Error:', e)
        return render(request, "donations/sub_category_list.html", {"error": str(e)})


def donation_sub_category_create(request):
    try:
        if request.method == "POST":

            title = request.POST["title"]
            category = request.POST["category"]

            payload = {
                "title": title,
                "donation_category": category
            }
            response = check_auth_request("POST", APIEndpoints.URL_DONATION_SUB_CATEGORY, request, data=payload)
            if response.status_code == 401:  # Unauthorized
                return redirect("login")

            response_body = response.json()
            if response.status_code == 201:
                return redirect('donation_sub_category_list')
            else:
                context = {
                    'errors': response_body['errors'],
                    'message': response_body['message']
                }
                return render(request, "donations/sub_category_create.html", context)
        else:
            response_category = check_auth_request("GET", APIEndpoints.URL_DONATION_CATEGORY, request)
            response_category_body = response_category.json()
            context = {
                'errors': response_category_body['errors'],
                'message': response_category_body['message'],
                'categories': response_category_body['data']['results']
            }
            return render(request, "donations/sub_category_create.html", context)
    except Exception as e:
        print('Donation Sub Category Creation Error:', e)
        return render(request, "donations/sub_category_create.html", {"error": str(e)})


def donation_sub_category_edit(request, uuid):
    try:
        if request.method == "POST":

            title = request.POST["title"]
            category = request.POST["category"]

            payload = {
                "title": title,
                "donation_category": category
            }
            response = check_auth_request("PUT", APIEndpoints.URL_DONATION_SUB_CATEGORY_DETAILS(uuid), request, data=payload)
            if response.status_code == 401:  # Unauthorized
                return redirect("login")
            response_body = response.json()
            if response.status_code == 200:
                return redirect('donation_sub_category_list')
            else:
                context = {
                    'errors': response_body['errors'],
                    'message': response_body['message']
                }
                return render(request, "donations/sub_category_edit.html", context)
        else:
            response = check_auth_request("GET", APIEndpoints.URL_DONATION_SUB_CATEGORY_DETAILS(uuid), request)
            if response.status_code == 401:  # Unauthorized
                return redirect("login")
            response_body = response.json()
            response_category = check_auth_request("GET", APIEndpoints.URL_DONATION_CATEGORY, request)
            response_category_body = response_category.json()
            context = {
                'data': response_body['data'],
                'categories': response_category_body['data']['results']
            }
            return render(request, "donations/sub_category_edit.html", context)
    except Exception as e:
        print('error', e)
        return render(request, "donations/sub_category_edit.html", {"error": str(e)})


def donation_sub_category_soft_delete(request, uuid):
    if request.method == "DELETE":
        response = check_auth_request("DELETE", APIEndpoints.URL_DONATION_SUB_CATEGORY_DETAILS(uuid), request)
        if response.status_code == 200:
            return JsonResponse({"success": True, "message": "Sub Category deleted successfully."})
        else:
            return JsonResponse(
                {"success": False, "message": f"Failed to delete Sub Category {response.status_code}."}, status=400
            )
    return JsonResponse({"success": False, "message": "Invalid request method."}, status=405)


def donation_list(request):
    return render(request, 'donations/list.html')


def donation_edit(request):
    return render(request, 'donations/create.html')
