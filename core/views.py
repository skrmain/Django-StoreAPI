from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from core.serializers import UserSerializer


class UserDetailView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = UserSerializer(request.user)
        return Response(user.data)

    def patch(self, request):
        user = UserSerializer(request.user, request.data)
        if user.is_valid():
            user.save()
            return Response({'data': 'Updated'})
        return Response({'data': 'Invalid'}, status=400)
