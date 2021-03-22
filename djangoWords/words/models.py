from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    games_submitted_to = models.ManyToManyField("Game")


class Game(models.Model):
    master = models.ForeignKey(User, related_name="game", on_delete=models.DO_NOTHING)
    submissions_allowed = models.BooleanField(default=True)


class Word(models.Model):
    text = models.CharField(max_length=30)
    game = models.ForeignKey(Game, related_name="word", on_delete=models.DO_NOTHING)
    creator = models.ForeignKey(User, related_name="word", null=True, on_delete=models.DO_NOTHING)
    creator_name = models.CharField(max_length=30)