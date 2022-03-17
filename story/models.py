from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Tag(models.Model):
    name = models.CharField(max_length=30, blank=False, unique=True)

    def __str__(self):
        return self.name


class SecretQuestion(models.Model):
    question = models.CharField(max_length=100, blank=False)

    def __str__(self):
        return self.question


class SecretQuestionAnswer(models.Model):
    answer = models.CharField(max_length=50, blank=False)
    question = models. OneToOneField(SecretQuestion, on_delete=models.CASCADE, related_name="answer") 
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="answer")

    def __str__(self):
        return str(self.user) + " + " + str(self.question) + " - " + self.answer


class Story(models.Model):
    class Meta:
        verbose_name_plural = "Stories"

    PUBLIC = 0
    PRIVATE = 1
    VISIBILITY = [(PUBLIC, 'Public'), (PRIVATE, 'Private')]

    DELETED = 0
    PUBLISHED = 1
    STATUS = [(DELETED, 'Deleted'), (PUBLISHED, 'Published')]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="story")
    tags = models.ManyToManyField(Tag)
    title = models.CharField(max_length=60, blank=False)
    content = models.CharField(max_length=250, blank=True)
    visibility = models.IntegerField(choices=VISIBILITY, default=PRIVATE)
    published = models.IntegerField(choices=STATUS, default=PUBLISHED)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, auto_created=True)
    updated_at = models.DateTimeField(auto_now=True)
    title_length = models.IntegerField(blank=True)

    # created_at_month = models.CharField(max_length=15, blank=True)

    def get_title_length(self):
        return len(self.title)

    def get_created_month(self):
        return self.created_at.strftime('%b')

    def clean(self):
        if self.created_at > timezone.now():
            raise ValidationError("Invalid created_at time given")

    def save(self, *args, **kwargs):
        self.title_length = self.get_title_length()
        # self.created_at_month = self.get_created_month()
        super(Story, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
