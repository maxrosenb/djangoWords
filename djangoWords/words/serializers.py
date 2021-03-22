from django.contrib.auth.models import User, Group
from rest_framework import serializers
from words.models import Game, Word, UserProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "password")

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User.objects.create_user(**validated_data)
        print("password: ", password)
        user.set_password(password)
        user.save()
        user_profile = UserProfile.objects.create(user=user)
        user_profile.save()
        return user


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ["url", "name"]


class GameSerializer(serializers.ModelSerializer):
    game_words = serializers.StringRelatedField(many=True)

    class Meta:
        model = Game
        fields = ["master", "game_words"]


class WordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = ["text"]
