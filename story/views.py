from os import name
import re
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import CreateAPIView, DestroyAPIView, UpdateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet,ViewSet
from rest_framework.permissions import IsAuthenticated
from .serializers import  ChangePasswordSecretQuestionsSerializer, ChangePasswordSerializer, TagSerializer, WriteStorySerializers, ReadStorySerializers, RegisterUserSerializer, \
    ReadSecretQuestionSerializer, WriteSecretQuestionSerializer, WriteSecretQuestionAnswerSerializer, \
    ReadSecretQuestionAnswerSerializer
from .models import Tag, Story, SecretQuestion, SecretQuestionAnswer
from django.contrib.auth.models import User

from story import serializers

class TagModelViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    paginator = None
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class StoryModelViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    # queryset = Transaction.objects.select_related("currency", "category", "user")
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields = ["content", "title"]
    ordering_fields = ["created_at"]
    ordering = ['-created_at']
    filterset_fields = ["user__username",]

    def get_queryset(self):
        # return Story.objects.select_related("user").filter(user=self.request.user)
        return Story.objects.filter(visibility=0)

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return ReadStorySerializers
        return WriteStorySerializers

    #  Replaced by CurrentUserDefault on WriteTransactionSerializers
    # def perform_create(self, serializer):
    #     # add user id on create a transaction
    #     serializer.save(user=self.request.user)


class MyStoryModelViewSet(ModelViewSet):
    permissipoon_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Story.objects.select_related("user").filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return ReadStorySerializers
        return WriteStorySerializers


class RegisterUserView(CreateAPIView):
    def post(self, request, *args, **kwargs):
        serializer = RegisterUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(DestroyAPIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def get(request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


class SecretQuestionViewSet(ModelViewSet):
    # permission_classes = (IsAuthenticated,)
    paginator = None
    def get_queryset(self):
        return SecretQuestion.objects.all()

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return ReadSecretQuestionSerializer
        return WriteSecretQuestionSerializer


class SecretQuestionAnswerViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    paginator = None
    def get_queryset(self):
        return SecretQuestionAnswer.objects.select_related("user").filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return ReadSecretQuestionAnswerSerializer
        return WriteSecretQuestionAnswerSerializer


class ChangePasswordView(UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User

    # def get_object(self, queryset=None):
    #     obj = self.request.user
    #     return obj

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            try:
                user = User.objects.get(username=serializer.data.get("username"))
                # set_password also hashes the password that the user will get
                user.set_password(serializer.data.get("new_password"))
                # delete user token
                try:
                    user.auth_token.delete()
                except:
                    pass    
                user.save()
                response = {
                    # 'status': 'success',
                    # 'code': status.HTTP_200_OK,
                    'message': 'Password updated successfully',
                    # 'data': []
                }

                return Response(response)

            except:
                return Response({"Username not found"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ChangePasswordSecretQuestionsView(ViewSet):
    def list(self, request):
        try:
            serializer = ReadSecretQuestionSerializer(SecretQuestionAnswer.objects.filter(user__username = self.request.data["username"]), many=True)
            return Response(serializer.data)
        except:
            return Response({"Bad request"}, status=status.HTTP_400_BAD_REQUEST)

# class ChangePasswordSecretQuestionsAnswerView():
    
