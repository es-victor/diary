from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import CreateAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .serializers import TagSerializer, WriteStorySerializers, ReadStorySerializers, RegisterUserSerializer, \
    ReadSecretQuestionSerializer, WriteSecretQuestionSerializer, WriteSecretQuestionAnswerSerializer, \
    ReadSecretQuestionAnswerSerializer
from .models import Tag, Story, SecretQuestion, SecretQuestionAnswer


class TagModelViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
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
    permission_classes = (IsAuthenticated,)

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
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return SecretQuestion.objects.all()

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return ReadSecretQuestionSerializer
        return WriteSecretQuestionSerializer


class SecretQuestionAnswerViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return SecretQuestionAnswer.objects.select_related("user").filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return ReadSecretQuestionAnswerSerializer
        return WriteSecretQuestionAnswerSerializer
