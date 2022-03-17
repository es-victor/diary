from django.urls import path
# from .views import TransactionModelViewSet, CategoryModelViewSet, CurrencyModelViewSet, TransactionReportAPIView, \
#     RegisterUserView
from .views import ChangePasswordSecretQuestionsView, ChangePasswordView, StoryModelViewSet, TagModelViewSet, RegisterUserView, MyStoryModelViewSet, LogoutView, \
    SecretQuestionViewSet, SecretQuestionAnswerViewSet
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'tags', TagModelViewSet, basename="tag")
router.register(r'stories', StoryModelViewSet, basename="story")
router.register(r'my_stories', MyStoryModelViewSet, basename="myStory")
router.register(r'secret-questions', SecretQuestionViewSet, basename="secret-question")
router.register(r'secret-question-answer', SecretQuestionAnswerViewSet, basename="secret-question-answer")
router.register(r'change-password-secret-questions', ChangePasswordSecretQuestionsView, basename="change-password-secret-questionsr")

urlpatterns = [
                  path("register/", RegisterUserView.as_view(), name="register"),
                  path("logout/", LogoutView.as_view(), name="logout"),
                  path("change-password/", ChangePasswordView.as_view(), name="change-password")
                  # path("change-password-secret-questions/", ChangePasswordSecretQuestionsView.as_view(), name="change-password-secret-questions")
                ] + router.urls
