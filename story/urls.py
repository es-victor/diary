from django.urls import path
# from .views import TransactionModelViewSet, CategoryModelViewSet, CurrencyModelViewSet, TransactionReportAPIView, \
#     RegisterUserView
from .views import StoryModelViewSet, TagModelViewSet, RegisterUserView, MyStoryModelViewSet, LogoutView, \
    SecretQuestionViewSet, SecretQuestionAnswerViewSet
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'tags', TagModelViewSet, basename="tag")
router.register(r'stories', StoryModelViewSet, basename="story")
router.register(r'my_stories', MyStoryModelViewSet, basename="myStory")
router.register(r'secret_question', SecretQuestionViewSet, basename="secret-question")
router.register(r'secret_question_answer', SecretQuestionAnswerViewSet, basename="secret-question-answer")

urlpatterns = [
                  path("register/", RegisterUserView.as_view(), name="register"),
                  path("logout/", LogoutView.as_view(), name="logout"),
                  ] + router.urls
