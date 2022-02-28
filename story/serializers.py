from datetime import timezone, datetime

from rest_framework import serializers
from .models import Tag, Story
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
        fields = ("id", "name",)


class WriteStorySerializers(serializers.ModelSerializer):
    # use CurrentUserDefault to get user details
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    tag = serializers.SlugRelatedField(slug_field="id", queryset=Tag.objects.all())

    class Meta:
        model = Story
        fields = ("id", "user", "tags", "title", "content", "visibility", "published", "latitude", "longitude", "created_at",)

        # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     user = self.context["request"].user
    #     self.fields["category"].queryset = user.categories.all()


class ReadStorySerializers(serializers.ModelSerializer):
    # queryset = Transaction.objects.select_related("currency","category","user")
    user = UserSerializer(read_only=True)
    tags = TagSerializer(read_only=True, many=True)

    class Meta:
        model = Story
        fields = ("id", "user", "tags", "title", "title_length", "created_at_month", "content", "visibility", "published", "latitude", "longitude", "created_at",)
        read_only_fields = fields
