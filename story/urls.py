from django.urls import path
# from .views import TransactionModelViewSet, CategoryModelViewSet, CurrencyModelViewSet, TransactionReportAPIView, \
#     RegisterUserView
from .serializers import LogoutView
from .views import StoryModelViewSet, TagModelViewSet, RegisterUserView
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'tags', TagModelViewSet, basename="tag")
router.register(r'stories', StoryModelViewSet, basename="story")

urlpatterns = [
                  path("register/", RegisterUserView.as_view(), name="register"),
                  path("logout/", LogoutView.as_view(), name="logout")
              ] + router.urls
