import json
from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate
from django.contrib.auth.models import User
from words.models import Game, Word, UserProfile
import words.views as views


class GameTests(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(username="max", email="max@maxrosenb.com", password="top_secret")
        self.user_profile = UserProfile.objects.create(user=self.user)
        self.game = Game.objects.create(master=self.user)

    def test_create_game(self):
        view = views.create_game
        request = self.factory.post("create-game/")
        request.user = self.user
        force_authenticate(request, user=self.user)
        response = view(request)

        assert response.status_code == 201

    def test_submit_words(self):
        view = views.submit_words
        pk = 1
        request = self.factory.put(
            "games/" + str(pk) + "/submit-words", {"words": ["dog", "dolphin", "cat", "whale"]}, format="json"
        )
        request.user = self.user
        force_authenticate(request, user=self.user)
        response = view(request, pk)

        assert response.status_code == 201

    def test_anon_submit_words(self):
        view = views.submit_words
        pk = 1
        request = self.factory.put(
            "games/" + str(pk) + "/submit-words",
            {"words": ["dog", "dolphin", "cat", "whale"], "name": "anon steve"},
            format="json",
        )
        response = view(request, pk)

        assert response.status_code == 201

    def test_get_word_creators(self):
        view = views.list_word_creators
        pk = 1
        request = self.factory.get("games/" + str(pk) + "/list-word-creators")
        request.user = self.user
        force_authenticate(request, user=self.user)
        response = view(request, pk)

        assert response.status_code == 200

    def test_start(self):
        view = views.start_game
        pk = 1
        request = self.factory.put("games/" + str(pk) + "start/")
        request.user = self.user
        force_authenticate(request, user=self.user)
        response = view(request, pk)
        tested_game = Game.objects.get(pk=pk)

        assert response.status_code == 200
        assert tested_game.submissions_allowed == False
