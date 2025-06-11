from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect

from frontend.adminUsers.views import check_auth_request
from frontend.config.api_endpoints import APIEndpoints


def post_category_list(request):
    try:
        response = check_auth_request("GET", APIEndpoints.URL_POST_CATEGORY, request)
        if response.status_code == 401 or response.status_code == 400:
            messages.warning(request, "Your session has expired! Please login again.")
            return redirect("login")

        response_body = response.json()
        context = {
            'messages': response_body["message"],
            'data': response_body["data"]["results"],
        }
        return render(request, "posts/category_list.html", context)
    except Exception as e:
        print('error', e)
        return render(request, "posts/category_list.html", {"error": str(e)})


def post_category_create(request):
    try:
        if request.method == "POST":

            title = request.POST["title"]
            payload = {
                "title": title,
            }
            response = check_auth_request("POST", APIEndpoints.URL_POST_CATEGORY, request, data=payload)
            if response.status_code == 401 or response.status_code == 400:
                messages.warning(request, "Your session has expired! Please login again.")
                return redirect("login")
            response_body = response.json()
            if response.status_code == 201:
                return redirect('post_category_list')
            else:
                context = {
                    'errors': response_body['errors'],
                    'message': response_body['message']
                }
                return render(request, "posts/category_create.html", context)
        else:
            context = {

            }
            return render(request, "posts/category_create.html", context)
    except Exception as e:
        print('error', e)
        return render(request, "posts/category_create.html", {"error": str(e)})


def post_category_edit(request, uuid):
    try:
        if request.method == "POST":

            title = request.POST["title"]
            payload = {
                "title": title,
            }
            response = check_auth_request("PUT", APIEndpoints.URL_POST_CATEGORY_DETAILS(uuid), request, data=payload)
            if response.status_code == 401 or response.status_code == 400:
                messages.warning(request, "Your session has expired! Please login again.")
                return redirect("login")
            response_body = response.json()
            if response.status_code == 200:
                return redirect('post_category_list')
            else:
                context = {
                    'errors': response_body['errors'],
                    'message': response_body['message']
                }
                return render(request, "posts/category_edit.html", context)
        else:
            response = check_auth_request("GET", APIEndpoints.URL_POST_CATEGORY_DETAILS(uuid), request)
            if response.status_code == 401 or response.status_code == 400:
                messages.warning(request, "Your session has expired! Please login again.")
                return redirect("login")
            response_body = response.json()
            context = {
                'data': response_body['data']
            }
            return render(request, "posts/category_edit.html", context)
    except Exception as e:
        print('error', e)
        return render(request, "posts/category_edit.html", {"error": str(e)})


def post_category_soft_delete(request, uuid):
    if request.method == "DELETE":
        response = check_auth_request("DELETE", APIEndpoints.URL_POST_CATEGORY_DETAILS(uuid), request)
        if response.status_code == 401 or response.status_code == 400:
            messages.warning(request, "Your session has expired! Please login again.")
            return redirect("login")
        if response.status_code == 200:
            return JsonResponse({"success": True, "message": "Category deleted successfully."})
        else:
            return JsonResponse(
                {"success": False, "message": f"Failed to delete Category {response.status_code}."}, status=400
            )
    return JsonResponse({"success": False, "message": "Invalid request method."}, status=405)


def weekly_activities_post_list(request, category_title):
    try:
        response = check_auth_request("GET", APIEndpoints.URL_POST_BY_CATEGORY(category_title), request)
        if response.status_code == 401 or response.status_code == 400:
            messages.warning(request, "Your session has expired! Please login again.")
            return redirect("login")

        response_body = response.json()
        context = {
            'messages': response_body["message"],
            'data': response_body["data"]["results"],
        }
        return render(request, "posts/weekly_activities_post_list.html", context)
    except Exception as e:
        print('error', e)
        return render(request, "posts/weekly_activities_post_list.html", {"error": str(e)})


def article_post_list(request, category_title):
    try:
        response = check_auth_request("GET", APIEndpoints.URL_POST_BY_CATEGORY(category_title), request)
        if response.status_code == 401 or response.status_code == 400:
            messages.warning(request, "Your session has expired! Please login again.")
            return redirect("login")

        response_body = response.json()
        context = {
            'messages': response_body["message"],
            'data': response_body["data"]["results"],
        }
        return render(request, "posts/weekly_activities_post_list.html", context)
    except Exception as e:
        print('error', e)
        return render(request, "posts/weekly_activities_post_list.html", {"error": str(e)})


def books_post_list(request, category_title):
    try:
        response = check_auth_request("GET", APIEndpoints.URL_POST_BY_CATEGORY(category_title), request)
        if response.status_code == 401 or response.status_code == 400:
            messages.warning(request, "Your session has expired! Please login again.")
            return redirect("login")

        response_body = response.json()
        context = {
            'messages': response_body["message"],
            'data': response_body["data"]["results"],
        }
        return render(request, "posts/weekly_activities_post_list.html", context)
    except Exception as e:
        print('error', e)
        return render(request, "posts/weekly_activities_post_list.html", {"error": str(e)})


def travel_post_list(request, category_title):
    try:
        response = check_auth_request("GET", APIEndpoints.URL_POST_BY_CATEGORY(category_title), request)
        if response.status_code == 401 or response.status_code == 400:
            messages.warning(request, "Your session has expired! Please login again.")
            return redirect("login")

        response_body = response.json()
        context = {
            'messages': response_body["message"],
            'data': response_body["data"]["results"],
        }
        return render(request, "posts/weekly_activities_post_list.html", context)
    except Exception as e:
        print('error', e)
        return render(request, "posts/weekly_activities_post_list.html", {"error": str(e)})


def friday_activities_post_list(request, category_title):
    try:
        response = check_auth_request("GET", APIEndpoints.URL_POST_BY_CATEGORY(category_title), request)
        if response.status_code == 401 or response.status_code == 400:
            messages.warning(request, "Your session has expired! Please login again.")
            return redirect("login")

        response_body = response.json()
        context = {
            'messages': response_body["message"],
            'data': response_body["data"]["results"],
        }
        return render(request, "posts/weekly_activities_post_list.html", context)
    except Exception as e:
        print('error', e)
        return render(request, "posts/weekly_activities_post_list.html", {"error": str(e)})


def achievements_post_list(request, category_title):
    try:
        response = check_auth_request("GET", APIEndpoints.URL_POST_BY_CATEGORY(category_title), request)
        if response.status_code == 401 or response.status_code == 400:
            messages.warning(request, "Your session has expired! Please login again.")
            return redirect("login")

        response_body = response.json()
        context = {
            'messages': response_body["message"],
            'data': response_body["data"]["results"],
        }
        return render(request, "posts/weekly_activities_post_list.html", context)
    except Exception as e:
        print('error', e)
        return render(request, "posts/weekly_activities_post_list.html", {"error": str(e)})
