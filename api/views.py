from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from api.helpers.api import load_file, best_bundle_in_mango, best_bundle_in_hemle, set_logging
from .models import UserChoices
from .serializer import UserChoicesSerializer


@api_view(['GET', 'POST'])
def load_datas(request):
    load_file()
    return Response({"datas": {'status': "Datas Saved."}})


@api_view(["POST"])
def get_choice(request):
    serializer = UserChoicesSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    mango_bundles = best_bundle_in_mango(**serializer.data)
    hemle_bundles = best_bundle_in_hemle(**serializer.data)
    return Response({'Mango': mango_bundles, 'Hemle': hemle_bundles}, status=status.HTTP_201_CREATED)
