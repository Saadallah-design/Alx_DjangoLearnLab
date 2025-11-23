from api.models import Book
from .serializers import BookSerializer
from rest_framework import generics 
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import permissions 
from rest_framework import status

# the following is a Generic Class-Based View
# its logic implementation: Automatic. You only need to set attributes (queryset and serializer_class), 
# and the parent class handles the rest.

class BookList(generics.ListAPIView):
    # The queryset attribute tells the view what data to retrieve.
    queryset = Book.objects.all()
    # The serializer_class attribute tells the view how to format the data.
    serializer_class = BookSerializer


# Creating a viewset
class BookViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for viewing and editing book instances.
    This single class handles: LIST, CREATE, RETRIEVE, UPDATE, 
    PARTIAL_UPDATE, and DESTROY actions.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    # Allows GET, HEAD, OPTIONS requests for unauthenticated users,
    # but requires authentication for POST, PUT, PATCH, and DELETE.
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


# Setting token-based authentication in DRF

class BookListView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Only authenticated users can access this view
        queryset = Book.objects.all()
        BookSerializer = BookSerializer(queryset, many=True)
        return Response(BookSerializer.data)
        # return Response({'message': 'Hello, authenticated user!'})

# class BookListCreateView(APIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAdminUser]

#     def post(self, request):
#         # Only admin users can create new model instances
#         serializer = BookSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)