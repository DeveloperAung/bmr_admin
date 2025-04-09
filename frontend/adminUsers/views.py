import requests
from django.http import JsonResponse
from django.shortcuts import render, redirect
from frontend.config.api_endpoints import APIEndpoints


def admin_user_list(request):
    try:
        headers = get_auth_headers(request)
        response = requests.get(APIEndpoints.URL_ADMIN_USERS, headers=headers)
        if response.status_code == 401:
            return redirect("login")
        response_body = response.json()
        context = {
            'messages': response_body["message"],
            'data': response_body["data"]["results"]
        }
        return render(request, "adminUsers/list.html", context)
    except Exception as e:
        print('error', e)
        return render(request, "adminUsers/list.html", {"error": str(e)})


def admin_user_register(request):
    try:
        role_response = check_auth_request("GET", APIEndpoints.URL_ADMIN_USER_ROLES, request)
        roles_data = role_response.json().get("data", [])
        roles = roles_data["results"]

        if request.method == "POST":

            name = request.POST["name"]
            username = request.POST["username"]
            email = request.POST["email"]
            contact = request.POST["contact"]
            secondary_contact = request.POST["secondary_contact"]
            admin_user_role = request.POST["admin_user_role"]

            payload = {
                "name": name,
                "username": username,
                "email": email,
                "contact": contact,
                "secondary_contact": secondary_contact,
                "admin_user_role": admin_user_role
            }
            response = check_auth_request("POST", APIEndpoints.URL_ADMIN_USERS, request, data=payload)

            if response.status_code == 401:  # Unauthorized
                return redirect("login")

            response_body = response.json()
            if response.status_code == 201:
                return redirect('admin_user_list')
            else:
                context = {
                    'errors': response_body['errors'],
                    'message': response_body['message'],
                    "roles": roles
                }
                return render(request, "adminUsers/create.html", context)
        else:
            context = {
                "roles": roles
            }
            return render(request, "adminUsers/create.html", context)
    except Exception as e:
        print('Admin User Create Error:', e)
        return render(request, "adminUsers/create.html", {"error": str(e)})


def admin_user_edit(request, uuid):
    try:
        role_response = check_auth_request("GET", APIEndpoints.URL_ADMIN_USER_ROLES, request)
        roles_data = role_response.json().get("data", [])
        roles = roles_data["results"]

        if request.method == "POST":

            name = request.POST["name"]
            username = request.POST["username"]
            email = request.POST["email"]
            contact = request.POST["contact"]
            secondary_contact = request.POST["secondary_contact"]
            admin_user_role = request.POST.get("admin_user_role")

            payload = {
                "name": name,
                "username": username,
                "email": email,
                "contact": contact,
                "secondary_contact": secondary_contact,
                "admin_user_role": admin_user_role
            }
            response = check_auth_request("PUT", APIEndpoints.URL_ADMIN_USER_DETAILS(uuid), request, data=payload)

            if response.status_code == 401:  # Unauthorized
                return redirect("login")

            response_body = response.json()
            if response.status_code == 200:
                return redirect('admin_user_list')
            else:
                context = {
                    'errors': response_body['errors'],
                    'message': response_body['message'],
                    'roles': roles
                }
                return render(request, "adminUsers/edit.html", context)
        else:
            response = check_auth_request("GET", APIEndpoints.URL_ADMIN_USER_DETAILS(uuid), request)
            response_body = response.json()
            context = {
                'data': response_body['data'],
                'roles': roles
            }
            return render(request, "adminUsers/edit.html", context)
    except Exception as e:
        print('Admin User Edit Error:', e)
        return render(request, "adminUsers/edit.html", {"error": str(e)})


def admin_user_soft_delete(request, uuid):
    if request.method == "DELETE":
        response = check_auth_request("DELETE", APIEndpoints.URL_ADMIN_USER_DETAILS(uuid), request)
        if response.status_code == 401:  # Unauthorized
            return redirect("login")

        if response.status_code == 200:
            return JsonResponse({"success": True, "message": "Admin User deleted successfully."})
        else:
            return JsonResponse(
                {"success": False, "message": f"Failed to delete Admin User {response.status_code}."}, status=400
            )
    return JsonResponse({"success": False, "message": "Invalid request method."}, status=405)


def reset_password(request):
    return render(request, 'adminUsers/reset_password.html')


def d_reset_password(request):
    return render(request, 'adminUsers/d_reset_password.html')


def forgot_password(request):
    return render(request, 'adminUsers/forgot_password.html')


def logout(request):
    return render(request, 'adminUsers/login.html')


def refresh_access_token(request):
    """Automatically refresh JWT token if expired"""
    refresh_token = request.session.get("refresh_token")

    if refresh_token:
        response = requests.post(APIEndpoints.URL_REFRESH, json={"refresh": refresh_token})

        if response.status_code == 200:
            tokens = response.json()
            request.session["access_token"] = tokens["access"]  # ✅ Store new access token
            return tokens["access"]

        request.session.flush()

    return None


def get_auth_headers(request):
    """Retrieve JWT token from session and attach to headers"""
    token = request.session.get("access_token")
    if token:
        return {"Authorization": f"Bearer {token}"}

    new_token = refresh_access_token(request)

    if new_token:
        return {"Authorization": f"Bearer {new_token}"}
    return {}


def check_auth_request(method, url, request, data=None, params=None):
    try:
        headers = get_auth_headers(request)
        response = requests.request(method, url, headers=headers, json=data, params=params)
        print('response', response)
        return response

    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        return None


def login(request):
    """Handles user login"""
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        response = requests.post(APIEndpoints.URL_LOGIN, json={"username": username, "password": password})

        if response.status_code == 200:
            tokens = response.json()
            request.session["access_token"] = tokens["data"]["access"]
            request.session["refresh_token"] = tokens["data"]["refresh"]
            return redirect("dashboard")
        else:
            return render(request, "adminUsers/login.html", {"error": "Invalid credentials"})

    return render(request, "adminUsers/login.html")


def logout(request):
    lg_response = requests.post(APIEndpoints.URL_LOGOUT, json={"refresh_token": request.session.get("refresh_token")}, allow_redirects=False)
    request.session.flush()
    return redirect("login")
