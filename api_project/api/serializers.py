from api.models import Book 
from rest_framework import serializers
class BookSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    class Meta: 
        model = Book
        fields = '__all__'