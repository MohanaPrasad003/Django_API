from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile
from rest_framework.validators import UniqueValidator

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = UserProfile
        fields = ['user', 'first_name', 'last_name', 'email']

    def create(self, validated_data):
        user_data = validated_data.pop('user')

        email = user_data.get('email')
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email is already in use.")
        
        user = User.objects.create(**user_data)
        profile = UserProfile.objects.create(user=user, **validated_data)
        return profile

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        user = instance.user
        user.username = user_data.get('username', user.username)
        user.email = user_data.get('email', user.email)
        user.save()

        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.save()

        return instance

    def validate(self, data):
        if 'first_name' not in data or not data['first_name']:
            raise serializers.ValidationError("First name is required.")
        if 'last_name' not in data or not data['last_name']:
            raise serializers.ValidationError("Last name is required.")
        return data
