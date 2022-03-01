from django.contrib import admin

from .models import Story, Tag, SecretQuestion, SecretQuestionAnswer

admin.site.register(Story)
admin.site.register(Tag)
admin.site.register(SecretQuestion)
admin.site.register(SecretQuestionAnswer)
