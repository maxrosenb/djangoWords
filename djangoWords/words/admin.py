from django.contrib import admin
from words.models import Word, Game, UserProfile

# Register your models here.
admin.site.register(Game)
admin.site.register(Word)
admin.site.register(UserProfile)