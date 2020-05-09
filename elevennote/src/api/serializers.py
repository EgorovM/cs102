from rest_framework import serializers
from accounts.models import User
from notes.models import Note


class NoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Note
        fields = ('id', 'title', 'body', 'tags', 'pub_date', 'owner', 'shared')



class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'is_active', 'is_staff', 'is_verified', 'code')
