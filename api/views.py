from rest_framework import generics, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.helpers.api import load_file
from api.serializer import UserChoicesSerializer


@api_view(['GET', 'POST'])
def load_datas(request):
    load_file()
    return Response({"datas": {'status': "Datas Saved."}})


class UserChoiseAPI(generics.GenericAPIView):
    serializer_class = UserChoicesSerializer
    authentication_classes = [permissions.AllowAny, ]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_choice = serializer.save()
        return Response({
            "datas": {
                user_choice
            }
        })
