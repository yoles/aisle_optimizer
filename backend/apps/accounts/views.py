from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.http import JsonResponse
from rest_framework.views import APIView

from apps.accounts.serializers import UserSerializer


class Register(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return JsonResponse(
                {"detail": "Email and password are required."}, status=403
            )

        validate_password(password)
        user = get_user_model().objects.create(email=email)
        user.set_password(password)
        user.save()

        user_serializer = UserSerializer(user)
        return JsonResponse(user_serializer.data, status=200)
