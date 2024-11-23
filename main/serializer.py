from rest_framework import serializers
from .models import User, Project, Task
from django.contrib.auth import authenticate

class UserSerializeer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


class Registration(serializers.ModelSerializer):
    password = serializers.CharField(min_length=12)
    class Meta:
        model = User
        fields = ('email', 'username', 'password')

    def save_in_database(self, **kwargs):
        user = User()
        user.email = self.validated_data['email']
        user.username = self.validated_data['username']
        user.set_password(self.validated_data['password'])
        user.save()
        return user

class Login(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField()
    class Meta:
        model = User
        fields = ('username', 'password')
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        if username and password:
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)
        attrs['user'] = user
        return attrs
    