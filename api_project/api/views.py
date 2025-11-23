from api.models import Book
from .serializers import BookSerializer
from rest_framework.generics import ListAPIView

# the following is a Generic Class-Based View
# its logic implementation: Automatic. You only need to set attributes (queryset and serializer_class), 
# and the parent class handles the rest.

class BookList(ListAPIView):
    # The queryset attribute tells the view what data to retrieve.
    queryset = Book.objects.all()
    # The serializer_class attribute tells the view how to format the data.
    serializer_class = BookSerializer
