from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime


@api_view(['GET'])
def server_status(request):
    date = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
    message = 'Server is live, current time is: '
    return Response(data=message + date, status=status.HTTP_200_OK)
