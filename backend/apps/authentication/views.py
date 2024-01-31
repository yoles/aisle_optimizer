from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.utils.translation import gettext_lazy as _
from rest_framework.views import APIView


def get_csrf_view(request):
    response = JsonResponse({"detail": "CSRF cookie set"})
    response["X-CSRFToken"] = get_token(request)
    return response


class Login(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return JsonResponse(
                {"detail": _("Email and password is required.")}, status=403
            )

        user = authenticate(username=email, password=password)

        if user is None:
            return JsonResponse(
                {"detail": _("Invalid credentials.")}, status=403
            )

        login(request, user)
        return JsonResponse({"detail": "Successfully logged in."})
