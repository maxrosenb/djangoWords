from django.contrib.auth.models import User, Group
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from words.serializers import UserSerializer, GroupSerializer, GameSerializer, WordSerializer
from words.models import Game, Word, UserProfile
import random


@api_view(["POST"])
@permission_classes([AllowAny])
def create_auth(request):
    user_serializer = UserSerializer(data=request.data)
    if user_serializer.is_valid():
        user = User.objects.create_user(
            username=user_serializer.data["username"], password=user_serializer.data["password"]
        )
        user.save()
        user_profile = UserProfile.objects.create(user=user)
        user_profile.save()
        return Response(user_serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(user_serializer._errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def get_word_creators(request, pk):
    """Returns a list of users that have submitted words for a given game"""

    game = get_object_or_404(Game, pk=pk)
    # Only the game master can see the list of word creators
    if game.master.id == request.user.id:
        requested_words = Word.objects.filter(game__pk=pk)
        word_creators = set([word.creator_name for word in requested_words])
        return Response({"creators": word_creators})
    return Response({"message": "Only the game master can view word creators."}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(["POST"])
def create_game(request):
    """Creates a game"""
    game = Game.objects.create(master=request.user)
    game.save()
    return Response({"message": "Game created", "id": game.id}, status=status.HTTP_201_CREATED)


@api_view(["POST"])
@permission_classes([AllowAny])
def submit_words(request, pk):
    """Submit words for a given game"""
    print("SUBMIT_WORDS CALLED")
    game = get_object_or_404(Game, pk=pk)
    if not game.submissions_allowed:
        return Response(
            {"message": "This game has started and new submissions are not allowed."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    for game_word in request.data["words"]:
        if not game_word:
            return Response({"message": "Please make sure no words are blank."}, status=status.HTTP_400_BAD_REQUEST)

    if len(request.data["words"]) != 4:
        return Response({"message": "Exactly 4 words must be submitted."}, status=status.HTTP_400_BAD_REQUEST)

    # If not anonymous user
    if request.user.id != None:
        user_profile = UserProfile.objects.get(user=request.user)
        if user_profile.games_submitted_to.filter(id=game.id).exists():
            return Response(
                {"message": "You have already submitted words for this game!"}, status=status.HTTP_400_BAD_REQUEST
            )
        for game_word in request.data["words"]:
            Word.objects.create(text=game_word, game=game, creator=request.user, creator_name=request.user.username)
            user_profile.games_submitted_to.add(game)
        return Response({"message": "Words submitted"}, status=status.HTTP_201_CREATED)

    # If anonymous user
    else:
        print("ANON USER FOUND")
        if "name" not in request.data:
            return Response(
                {"message": "A name must be provided by anonymous users."}, status=status.HTTP_400_BAD_REQUEST
            )
        for game_word in request.data["words"]:
            Word.objects.create(text=game_word, game=game, creator_name=request.data["name"])
        return Response({"message": "Words submitted"}, status=status.HTTP_201_CREATED)


@api_view(["POST"])
@permission_classes([AllowAny])
def submit_words_without_account(request, pk):
    """Submit words for a given game without an account"""
    game = get_object_or_404(Game, pk=pk)
    if not game.submissions_allowed:
        return Response(
            {"message": "This game has started and new submissions are not allowed."},
            status=status.HTTP_400_BAD_REQUEST,
        )


@api_view(["PUT"])
def start_game(request, pk):
    """Starts the game given by the PK"""
    game = get_object_or_404(Game, pk=pk)
    # Only the game master can start a game
    if request.user.id != game.master.id:
        return Response({"message": "Only the game master can start the game"}, status=status.HTTP_400_BAD_REQUEST)
    # Cannot start a game that has already started
    if not game.submissions_allowed:
        return Response({"message": "This game has already started"}, status=status.HTTP_400_BAD_REQUEST)

    game.submissions_allowed = False
    game_words = [game_word.text for game_word in Word.objects.filter(game__pk=pk)]
    random.shuffle(game_words)
    game.save()
    return Response(game_words, status=status.HTTP_200_OK)