import requests
from django.shortcuts import render, redirect
from frontend.config.api_endpoints import APIEndpoints


def admin_user_list(request):
    return render(request, 'adminUsers/list.html')


def register_admin_user(request):
    return render(request, 'adminUsers/register_admin_user.html')


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
            return tokens["access"]  # ✅ Return new access token

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
        if response.status_code == 401:  # Unauthorized
            return redirect("login")
        print('default response', response)
        return response  # Return the response object for further handling

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
    print('logout')
    """Handles user logout"""
    lg_response = requests.post(APIEndpoints.URL_LOGOUT, json={"refresh_token": request.session.get("refresh_token")}, allow_redirects=False)
    print('logout response', lg_response)
    request.session.flush()
    return redirect("login")
