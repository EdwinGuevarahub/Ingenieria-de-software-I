from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

@api_view(['GET', 'POST'])
def hello_world(request):
    if request.method == 'POST':
        return Response({"message": "Post method!"})
    return Response({"message": "Hello, world!"})

class ApiViewSet(ViewSet):
    def list(self, request):
        return Response({"message": "Base entry point. please specify in the path the resource you want to use."})

class DefaultViewSet(ViewSet):
    def list(self, request):
        return Response({"message": "Base entry point. Hello, world!"})