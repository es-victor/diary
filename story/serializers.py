from datetime import timezone, datetime

from rest_framework import serializers, status
from rest_framework.generics import DestroyAPIView
from rest_framework.response import Response

from .models import Tag, Story, SecretQuestion, SecretQuestionAnswer
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name")
        read_only_fields = fields


class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'first_name', 'last_name')
        write_only_fields = ('password',)
        read_only_fields = ('id',)

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        user.set_password(validated_data['password'])
        user.save()
        return user


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("id", "name")


class SecretQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecretQuestion
        fields = ("question",)


class WriteStorySerializers(serializers.ModelSerializer):
    # use CurrentUserDefault to get user details
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    tags = TagSerializer(many=True, read_only=True).data

    # tags = serializers.SlugRelatedField(slug_field="id",queryset=Tag.objects)

    class Meta:
        model = Story
        fields = (
            "id", "user", "tags", "title", "content", "visibility", "published", "latitude", "longitude", "created_at",)

        # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     user = self.context["request"].user
    #     self.fields["category"].queryset = user.categories.all()


class ReadStorySerializers(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    tags = TagSerializer(read_only=True, many=True)

    class Meta:
        model = Story
        fields = (
            "id", "user", "tags", "title", "title_length", "content", "visibility", "published", "latitude",
            "longitude",
            "created_at",)
        read_only_fields = fields


class ReadSecretQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecretQuestion
        fields = ("question",)
        read_only_fields = fields


class WriteSecretQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecretQuestion
        fields = ("question",)


class ReadSecretQuestionAnswerSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    question = SecretQuestionSerializer(read_only=True)

    class Meta:
        model = SecretQuestionAnswer
        fields = ("question", "answer", "user")
        read_only_fields = fields


class WriteSecretQuestionAnswerSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    question = SecretQuestionSerializer(many=True, read_only=True).data

    class Meta:
        model = SecretQuestionAnswer
        fields = ("question", "answer", "user")