from django.urls import include, path
from django.contrib import admin

from rest_framework import routers
from words import views
from django.views.decorators.csrf import csrf_exempt

router = routers.DefaultRouter()

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path("", include(router.urls)),
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("register/", views.register, name="register_user"),
    path("games/<int:pk>/get-word-creators/", views.list_word_creators, name="game_words"),
    path("games/<int:pk>/submit-words/", views.submit_words, name="game_words"),
    path("games/<int:pk>/start/", views.start_game, name="start_game"),
    path("create-game/", views.create_game, name="create_game"),
]
