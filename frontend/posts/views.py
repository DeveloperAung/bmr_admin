import base64
import json

from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect

from frontend.adminUsers.views import check_auth_request
from frontend.config.api_endpoints import APIEndpoints
from frontend.posts.utlis.validate_image import validate_cover_image, convert_image_to_base64

cover_image_size = 5 * 1024 * 1024


def post_category_list(request):
    try:
        page = request.GET.get("page", 1)
        search = request.GET.get("q", "")

        params = {"page": page}
        if search:
            params["search"] = search

        response = check_auth_request("GET", APIEndpoints.URL_POST_CATEGORY, request, params=params)
        if response.status_code == 401 or response.status_code == 400:
            messages.warning(request, "Your session has expired! Please login again.")
            return redirect("login")

        response_body = response.json()
        context = {
            'messages': response_body["message"],
            'data_header': response_body["data"],
            'data_results': response_body["data"]["results"],
            "request": request,
            "query": search,
        }
        return render(request, "posts/category_list.html", context)
    except Exception as e:
        print('error', e)
        return render(request, "posts/category_list.html", {"error": str(e), "request": request, })


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


def weekly_activities_list(request):
    try:
        page = request.GET.get("page", 1)
        search = request.GET.get("q", "")

        params = {"page": page}
        if search:
            params["search"] = search
        params["category_id"] = 1

        response = check_auth_request("GET", APIEndpoints.URL_POST, request, params=params)

        if response.status_code == 401 or response.status_code == 400:
            messages.warning(request, "Your session has expired! Please login again.")
            return redirect("login")

        response_body = response.json()
        context = {
            'messages': response_body["message"],
            'data_header': response_body["data"],
            'data_results': response_body["data"]["results"],
            "request": request,
            "query": search,
        }
        return render(request, "posts/weekly_activities/list.html", context)
    except Exception as e:
        print('error', e)
        return render(request, "posts/weekly_activities/list.html", {"error": str(e)})


def weekly_activity_create(request):
    try:
        if request.method == "POST":
            title = request.POST.get("title", "").strip()
            description = request.POST.get("description", "").strip()
            is_publish = request.POST.get("is_publish") == "on"  # Checkbox handling
            cover_image = request.FILES.get("cover_image")

            # Validation
            errors = []

            if not title:
                errors.append("Title is required.")

            # if len(title) > 200:
            #     errors.append("Title must be less than 200 characters.")

            if not description:
                errors.append("Description is required.")

            if cover_image:
                if cover_image.size > cover_image_size:
                    errors.append("Cover image must be less than 5MB.")

                # Check file type
                allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp']
                if cover_image.content_type not in allowed_types:
                    errors.append("Cover image must be a valid image file (JPEG, PNG, GIF, WebP).")

            # If there are validation errors, return to form with errors
            if errors:
                context = {
                    'error_message': "Please correct the following errors:",
                    'custom_alerts': [
                        {
                            'type': 'danger',
                            'message': error,
                            'icon': 'fa-solid fa-circle-exclamation'
                        } for error in errors
                    ]
                }
                return render(request, 'posts/weekly_activities/create.html', context)

            payload = {
                'title': title,
                'description': description,
                'is_published': is_publish,
                'post_category': 1,
            }
            if cover_image:
                payload['cover_image'] = convert_image_to_base64(cover_image)

            response = check_auth_request("POST", APIEndpoints.URL_POST, request, data=payload)
            if response.status_code == 401 or response.status_code == 400:
                messages.warning(request, "Your session has expired! Please login again.")
                return redirect("login")
            response_body = response.json()
            if response.status_code == 201:
                return redirect('weekly_activities_list')
            else:
                context = {
                    'errors': response_body['errors'],
                    'message': response_body['message']
                }
                return render(request, "posts/weekly_activities/create.html", context)
        else:
            context = {

            }
            return render(request, "posts/weekly_activities/create.html", context)
    except Exception as e:
        print('error', e)
        return render(request, "posts/weekly_activities/create.html", {"error": str(e)})


def weekly_activity_edit(request, uuid):
    try:
        if request.method == "POST":

            title = request.POST.get("title", "").strip()
            description = request.POST.get("description", "").strip()
            is_publish = request.POST.get("is_publish") == "on"  # Checkbox handling
            cover_image = request.FILES.get("cover_image")

            # Validation
            errors = []

            if not title:
                errors.append("Title is required.")

            # if len(title) > 200:
            #     errors.append("Title must be less than 200 characters.")

            if not description:
                errors.append("Description is required.")

            if cover_image:
                if cover_image.size > cover_image_size:
                    errors.append("Cover image must be less than 5MB.")

                # Check file type
                allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp']
                if cover_image.content_type not in allowed_types:
                    errors.append("Cover image must be a valid image file (JPEG, PNG, GIF, WebP).")

            # If there are validation errors, return to form with errors
            if errors:
                context = {
                    'error_message': "Please correct the following errors:",
                    'custom_alerts': [
                        {
                            'type': 'danger',
                            'message': error,
                            'icon': 'fa-solid fa-circle-exclamation'
                        } for error in errors
                    ]
                }
                return render(request, 'posts/weekly_activities/edit.html', context)

            payload = {
                'title': title,
                'description': description,
                'is_published': is_publish,
                'post_category': 1,
            }
            if cover_image:
                payload['cover_image'] = convert_image_to_base64(cover_image)

            response = check_auth_request("PUT", APIEndpoints.URL_POST_DETAILS(uuid), request, data=payload)
            if response.status_code == 401 or response.status_code == 400:
                messages.warning(request, "Your session has expired! Please login again.")
                return redirect("login")
            response_body = response.json()
            if response.status_code == 200:
                return redirect('weekly_activities_list')
            else:
                context = {
                    'errors': response_body['errors'],
                    'message': response_body['message']
                }
                return render(request, "posts/weekly_activities/edit.html", context)
        else:
            response = check_auth_request("GET", APIEndpoints.URL_POST_DETAILS(uuid), request)
            if response.status_code == 401 or response.status_code == 400:
                messages.warning(request, "Your session has expired! Please login again.")
                return redirect("login")
            response_body = response.json()
            context = {
                'data': response_body['data']
            }
            return render(request, "posts/weekly_activities/edit.html", context)
    except Exception as e:
        print('error', e)
        return render(request, "posts/weekly_activities/edit.html", {"error": str(e)})


def article_list(request):
    try:
        page = request.GET.get("page", 1)
        search = request.GET.get("q", "")

        params = {"page": page}
        if search:
            params["search"] = search
        params["category_id"] = 2

        response = check_auth_request("GET", APIEndpoints.URL_POST, request, params=params)
        print('response', response)
        if response.status_code == 401 or response.status_code == 400:
            messages.warning(request, "Your session has expired! Please login again.")
            return redirect("login")

        response_body = response.json()
        context = {
            'messages': response_body["message"],
            'data_header': response_body["data"],
            'data_results': response_body["data"]["results"],
            "request": request,
            "query": search,
        }
        return render(request, "posts/articles/list.html", context)
    except Exception as e:
        print('error', e)
        return render(request, "posts/articles/list.html", {"error": str(e)})


def article_create(request):
    try:
        if request.method == "POST":
            title = request.POST.get("title", "").strip()
            parent = request.POST.get("parent_article", "").strip()
            description = request.POST.get("description", "").strip()
            is_publish = request.POST.get("is_publish") == "on"  # Checkbox handling
            cover_image = request.FILES.get("cover_image")

            # Validation
            errors = []

            if not title:
                errors.append("Title is required.")

            # if len(title) > 200:
            #     errors.append("Title must be less than 200 characters.")

            if not description:
                errors.append("Description is required.")

            # Validate cover image if provided
            if cover_image:
                # Check file size (e.g., max 5MB)
                if cover_image.size > cover_image_size:
                    errors.append("Cover image must be less than 5MB.")

                # Check file type
                allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp']
                if cover_image.content_type not in allowed_types:
                    errors.append("Cover image must be a valid image file (JPEG, PNG, GIF, WebP).")

            # If there are validation errors, return to form with errors
            if errors:
                context = {
                    'error_message': "Please correct the following errors:",
                    'custom_alerts': [
                        {
                            'type': 'danger',
                            'message': error,
                            'icon': 'fa-solid fa-circle-exclamation'
                        } for error in errors
                    ]
                }
                return render(request, 'posts/articles/create.html', context)

            payload = {
                'title': title,
                'parent': parent,
                'description': description,
                'is_published': is_publish,
                'post_category': 2,
            }
            errors.append(validate_cover_image(cover_image))
            if cover_image:
                payload['cover_image'] = convert_image_to_base64(cover_image)

            response = check_auth_request("POST", APIEndpoints.URL_POST, request, data=payload)
            if response.status_code == 401 or response.status_code == 400:
                messages.warning(request, "Your session has expired! Please login again.")
                return redirect("login")
            response_body = response.json()
            if response.status_code == 201:
                return redirect('article_list')
            else:
                context = {
                    'errors': response_body['errors'],
                    'message': response_body['message']
                }
                return render(request, "posts/articles/create.html", context)
        else:
            params = {"category_id": 2}
            response = check_auth_request("GET", APIEndpoints.URL_POST, request, params=params)
            response_data = response.json()["data"]
            context = {
                'parent_posts': response_data["results"] if response_data else None
            }
            return render(request, "posts/articles/create.html", context)
    except Exception as e:
        print('error', e)
        return render(request, "posts/articles/create.html", {"error": str(e)})


def article_edit(request, uuid):
    try:
        if request.method == "POST":

            title = request.POST.get("title", "").strip()
            description = request.POST.get("description", "").strip()
            parent_article = request.POST["parent_article"]
            is_publish = request.POST.get("is_publish") == "on"  # Checkbox handling
            cover_image = request.FILES.get("cover_image")

            errors = []

            if not title:
                errors.append("Title is required.")

            # if len(title) > 200:
            #     errors.append("Title must be less than 200 characters.")

            if not description:
                errors.append("Description is required.")

            # Validate cover image if provided
            if cover_image:
                if cover_image.size > cover_image_size:
                    errors.append("Cover image must be less than 5MB.")

                # Check file type
                allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp']
                if cover_image.content_type not in allowed_types:
                    errors.append("Cover image must be a valid image file (JPEG, PNG, GIF, WebP).")

            # If there are validation errors, return to form with errors
            if errors:
                context = {
                    'error_message': "Please correct the following errors:",
                    'custom_alerts': [
                        {
                            'type': 'danger',
                            'message': error,
                            'icon': 'fa-solid fa-circle-exclamation'
                        } for error in errors
                    ]
                }
                return render(request, 'posts/articles/edit.html', context)

            payload = {
                'title': title,
                'description': description,
                'is_published': is_publish,
                'post_category': 2,
                'parent': parent_article,
            }
            if cover_image:
                payload['cover_image'] = convert_image_to_base64(cover_image)

            response = check_auth_request("PUT", APIEndpoints.URL_POST_DETAILS(uuid), request, data=payload)
            if response.status_code == 401 or response.status_code == 400:
                messages.warning(request, "Your session has expired! Please login again.")
                return redirect("login")
            response_body = response.json()
            if response.status_code == 200:
                return redirect('article_list')
            else:
                context = {
                    'errors': response_body['errors'],
                    'message': response_body['message']
                }
                return render(request, "posts/articles/edit.html", context)
        else:
            response = check_auth_request("GET", APIEndpoints.URL_POST_DETAILS(uuid), request)

            params = {"category_id": 2}
            parent_article_response = check_auth_request("GET", APIEndpoints.URL_POST, request, params=params)
            response_data = parent_article_response.json()["data"]
            if response.status_code == 401 or response.status_code == 400:
                messages.warning(request, "Your session has expired! Please login again.")
                return redirect("login")
            response_body = response.json()
            context = {
                'data': response_body['data'],
                'parent_posts': response_data["results"] if response_data else None
            }
            return render(request, "posts/articles/edit.html", context)
    except Exception as e:
        print('error', e)
        return render(request, "posts/articles/edit.html", {"error": str(e)})


def travel_post_list(request):
    try:
        page = request.GET.get("page", 1)
        search = request.GET.get("q", "")

        params = {"page": page}
        if search:
            params["search"] = search
        params["category_id"] = 4

        response = check_auth_request("GET", APIEndpoints.URL_POST, request, params=params)
        print('response', response)
        if response.status_code == 401 or response.status_code == 400:
            messages.warning(request, "Your session has expired! Please login again.")
            return redirect("login")

        response_body = response.json()
        context = {
            'messages': response_body["message"],
            'data_header': response_body["data"],
            'data_results': response_body["data"]["results"],
            "request": request,
            "query": search,
        }
        return render(request, "posts/travel_post/list.html", context)
    except Exception as e:
        print('error', e)
        return render(request, "posts/travel_post/list.html", {"error": str(e)})


def travel_post_create(request):
    try:
        if request.method == "POST":
            title = request.POST.get("title", "").strip()
            parent = request.POST.get("parent_article", "").strip()
            short_description = request.POST.get("short_description", "").strip()
            description = request.POST.get("description", "").strip()
            is_publish = request.POST.get("is_publish") == "on"  # Checkbox handling
            cover_image = request.FILES.get("cover_image")

            # Validation
            errors = []

            if not title:
                errors.append("Title is required.")

            # if len(title) > 200:
            #     errors.append("Title must be less than 200 characters.")

            if not description:
                errors.append("Description is required.")

            # Validate cover image if provided
            if cover_image:
                # Check file size (e.g., max 5MB)
                if cover_image.size > cover_image_size:
                    errors.append("Cover image must be less than 5MB.")

                # Check file type
                allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp']
                if cover_image.content_type not in allowed_types:
                    errors.append("Cover image must be a valid image file (JPEG, PNG, GIF, WebP).")

            # If there are validation errors, return to form with errors
            if errors:
                context = {
                    'error_message': "Please correct the following errors:",
                    'custom_alerts': [
                        {
                            'type': 'danger',
                            'message': error,
                            'icon': 'fa-solid fa-circle-exclamation'
                        } for error in errors
                    ]
                }
                return render(request, 'posts/travel_post/create.html', context)

            payload = {
                'title': title,
                'parent': parent,
                'short_description': short_description,
                'description': description,
                'is_published': is_publish,
                'post_category': 4,
            }
            if cover_image:
                payload['cover_image'] = convert_image_to_base64(cover_image)

            response = check_auth_request("POST", APIEndpoints.URL_POST, request, data=payload)
            if response.status_code == 401 or response.status_code == 400:
                messages.warning(request, "Your session has expired! Please login again.")
                return redirect("login")
            response_body = response.json()
            if response.status_code == 201:
                return redirect('travel_post_list')
            else:
                context = {
                    'errors': response_body['errors'],
                    'message': response_body['message']
                }
                return render(request, "posts/travel_post/create.html", context)
        else:
            params = {"category_id": 4}
            response = check_auth_request("GET", APIEndpoints.URL_POST, request, params=params)
            response_data = response.json()["data"]
            context = {
                'parent_posts': response_data["results"] if response_data else None
            }
            return render(request, "posts/travel_post/create.html", context)
    except Exception as e:
        print('error', e)
        return render(request, "posts/travel_post/create.html", {"error": str(e)})


def travel_post_edit(request, uuid):
    try:
        if request.method == "POST":

            title = request.POST.get("title", "").strip()
            short_description = request.POST.get("short_description", "").strip()
            description = request.POST.get("description", "").strip()
            parent_article = request.POST["parent_article"]
            is_publish = request.POST.get("is_publish") == "on"  # Checkbox handling
            cover_image = request.FILES.get("cover_image")

            errors = []

            if not title:
                errors.append("Title is required.")

            # if len(title) > 200:
            #     errors.append("Title must be less than 200 characters.")

            if not description:
                errors.append("Description is required.")

            # Validate cover image if provided
            if cover_image:
                if cover_image.size > cover_image_size:
                    errors.append("Cover image must be less than 5MB.")

                # Check file type
                allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp']
                if cover_image.content_type not in allowed_types:
                    errors.append("Cover image must be a valid image file (JPEG, PNG, GIF, WebP).")

            # If there are validation errors, return to form with errors
            if errors:
                context = {
                    'error_message': "Please correct the following errors:",
                    'custom_alerts': [
                        {
                            'type': 'danger',
                            'message': error,
                            'icon': 'fa-solid fa-circle-exclamation'
                        } for error in errors
                    ]
                }
                return render(request, 'posts/travel_post/edit.html', context)

            payload = {
                'title': title,
                'short_description': short_description,
                'description': description,
                'is_published': is_publish,
                'post_category': 4,
                'parent': parent_article,
            }
            if cover_image:
                payload['cover_image'] = convert_image_to_base64(cover_image)

            response = check_auth_request("PUT", APIEndpoints.URL_POST_DETAILS(uuid), request, data=payload)
            if response.status_code == 401 or response.status_code == 400:
                messages.warning(request, "Your session has expired! Please login again.")
                return redirect("login")
            response_body = response.json()
            if response.status_code == 200:
                return redirect('travel_post_list')
            else:
                context = {
                    'errors': response_body['errors'],
                    'message': response_body['message']
                }
                return render(request, "posts/travel_post/edit.html", context)
        else:
            response = check_auth_request("GET", APIEndpoints.URL_POST_DETAILS(uuid), request)

            params = {"category_id": 4}
            parent_article_response = check_auth_request("GET", APIEndpoints.URL_POST, request, params=params)
            response_data = parent_article_response.json()["data"]
            if response.status_code == 401 or response.status_code == 400:
                messages.warning(request, "Your session has expired! Please login again.")
                return redirect("login")
            response_body = response.json()
            context = {
                'data': response_body['data'],
                'parent_posts': response_data["results"] if response_data else None
            }
            return render(request, "posts/travel_post/edit.html", context)
    except Exception as e:
        print('error', e)
        return render(request, "posts/travel_post/edit.html", {"error": str(e)})


def friday_activities_list(request):
    try:
        page = request.GET.get("page", 1)
        search = request.GET.get("q", "")

        params = {"page": page}
        if search:
            params["search"] = search
        params["category_id"] = 5

        response = check_auth_request("GET", APIEndpoints.URL_POST, request, params=params)

        if response.status_code == 401 or response.status_code == 400:
            messages.warning(request, "Your session has expired! Please login again.")
            return redirect("login")

        response_body = response.json()
        context = {
            'messages': response_body["message"],
            'data_header': response_body["data"],
            'data_results': response_body["data"]["results"],
            "request": request,
            "query": search,
        }
        return render(request, "posts/friday_activities/list.html", context)
    except Exception as e:
        print('error', e)
        return render(request, "posts/friday_activities/list.html", {"error": str(e)})


def friday_activity_create(request):
    try:
        if request.method == "POST":
            title = request.POST.get("title", "").strip()
            description = request.POST.get("description", "").strip()
            is_publish = request.POST.get("is_publish") == "on"  # Checkbox handling
            cover_image = request.FILES.get("cover_image")

            # Validation
            errors = []

            if not title:
                errors.append("Title is required.")

            # if len(title) > 200:
            #     errors.append("Title must be less than 200 characters.")

            if not description:
                errors.append("Description is required.")

            if cover_image:
                if cover_image.size > cover_image_size:
                    errors.append("Cover image must be less than 5MB.")

                # Check file type
                allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp']
                if cover_image.content_type not in allowed_types:
                    errors.append("Cover image must be a valid image file (JPEG, PNG, GIF, WebP).")

            # If there are validation errors, return to form with errors
            if errors:
                context = {
                    'error_message': "Please correct the following errors:",
                    'custom_alerts': [
                        {
                            'type': 'danger',
                            'message': error,
                            'icon': 'fa-solid fa-circle-exclamation'
                        } for error in errors
                    ]
                }
                return render(request, 'posts/friday_activities/create.html', context)

            payload = {
                'title': title,
                'description': description,
                'is_published': is_publish,
                'post_category': 5,
            }
            if cover_image:
                payload['cover_image'] = convert_image_to_base64(cover_image)

            response = check_auth_request("POST", APIEndpoints.URL_POST, request, data=payload)
            if response.status_code == 401 or response.status_code == 400:
                messages.warning(request, "Your session has expired! Please login again.")
                return redirect("login")
            response_body = response.json()
            if response.status_code == 201:
                return redirect('friday_activities_list')
            else:
                context = {
                    'errors': response_body['errors'],
                    'message': response_body['message']
                }
                return render(request, "posts/friday_activities/create.html", context)
        else:
            context = {

            }
            return render(request, "posts/friday_activities/create.html", context)
    except Exception as e:
        print('error', e)
        return render(request, "posts/friday_activities/create.html", {"error": str(e)})


def friday_activity_edit(request, uuid):
    try:
        if request.method == "POST":

            title = request.POST.get("title", "").strip()
            description = request.POST.get("description", "").strip()
            is_publish = request.POST.get("is_publish") == "on"  # Checkbox handling
            cover_image = request.FILES.get("cover_image")

            # Validation
            errors = []

            if not title:
                errors.append("Title is required.")

            # if len(title) > 200:
            #     errors.append("Title must be less than 200 characters.")

            if not description:
                errors.append("Description is required.")

            if cover_image:
                if cover_image.size > cover_image_size:
                    errors.append("Cover image must be less than 5MB.")

                # Check file type
                allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp']
                if cover_image.content_type not in allowed_types:
                    errors.append("Cover image must be a valid image file (JPEG, PNG, GIF, WebP).")

            # If there are validation errors, return to form with errors
            if errors:
                context = {
                    'error_message': "Please correct the following errors:",
                    'custom_alerts': [
                        {
                            'type': 'danger',
                            'message': error,
                            'icon': 'fa-solid fa-circle-exclamation'
                        } for error in errors
                    ]
                }
                return render(request, 'posts/friday_activities/edit.html', context)

            payload = {
                'title': title,
                'description': description,
                'is_published': is_publish,
                'post_category': 5,
            }
            if cover_image:
                payload['cover_image'] = convert_image_to_base64(cover_image)

            response = check_auth_request("PUT", APIEndpoints.URL_POST_DETAILS(uuid), request, data=payload)
            if response.status_code == 401 or response.status_code == 400:
                messages.warning(request, "Your session has expired! Please login again.")
                return redirect("login")
            response_body = response.json()
            if response.status_code == 200:
                return redirect('friday_activities_list')
            else:
                context = {
                    'errors': response_body['errors'],
                    'message': response_body['message']
                }
                return render(request, "posts/friday_activities/edit.html", context)
        else:
            response = check_auth_request("GET", APIEndpoints.URL_POST_DETAILS(uuid), request)
            if response.status_code == 401 or response.status_code == 400:
                messages.warning(request, "Your session has expired! Please login again.")
                return redirect("login")
            response_body = response.json()
            context = {
                'data': response_body['data']
            }
            return render(request, "posts/friday_activities/edit.html", context)
    except Exception as e:
        print('error', e)
        return render(request, "posts/friday_activities/edit.html", {"error": str(e)})


def post_soft_delete(request, uuid):
    if request.method == "DELETE":
        response = check_auth_request("DELETE", APIEndpoints.URL_POST_DETAILS(uuid), request)
        if response.status_code == 401 or response.status_code == 400:
            messages.warning(request, "Your session has expired! Please login again.")
            return redirect("login")
        if response.status_code == 200:
            return JsonResponse({"success": True, "message": "Post deleted successfully."})
        else:
            return JsonResponse(
                {"success": False, "message": f"Failed to delete Post {response.status_code}."}, status=400
            )
    return JsonResponse({"success": False, "message": "Invalid request method."}, status=405)


def post_publish_toggle(request, uuid):
    if request.method == "PATCH":

        response = check_auth_request("PATCH", APIEndpoints.URL_POST_PUBLISH_TOGGLE(uuid), request)
        decoded_response = response.json()
        if response.status_code == 401 or response.status_code == 400:
            return redirect("login")

        if response.status_code == 200:
            return JsonResponse({"success": True, "message": decoded_response["message"]})
        else:
            return JsonResponse(
                {"success": False, "message": f"Failed to publish / un-publish {response.status_code}."}, status=400
            )
    return JsonResponse({"success": False, "message": "Invalid request method."}, status=405)


def books_post_list(request, category_title):
    try:
        response = check_auth_request("GET", APIEndpoints.URL_POST, request)
        if response.status_code == 401 or response.status_code == 400:
            messages.warning(request, "Your session has expired! Please login again.")
            return redirect("login")

        response_body = response.json()
        context = {
            'messages': response_body["message"],
            'data': response_body["data"]["results"],
        }
        return render(request, "posts/book/list.html", context)
    except Exception as e:
        print('error', e)
        return render(request, "posts/book/list.html", {"error": str(e)})


def achievements_post_list(request, category_title):
    try:
        response = check_auth_request("GET", APIEndpoints.URL_POST, request)
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
