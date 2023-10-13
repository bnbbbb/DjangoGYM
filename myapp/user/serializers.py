from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import ValidationError
from .models import User

class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=80)
    password = serializers.CharField(min_length=8, write_only=True)
    class Meta:
        model = User
        fields = ('id', 'password','username', 'business', 'is_staff', 'is_superuser', 'is_active', 'last_login', 'date_joined')

    def create(self, validated_data):
        password = validated_data.pop("password")

        user = super().create(validated_data)
        user.set_password(password)
        user.save()

        Token.objects.create(user=user)

        return user