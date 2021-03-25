from rest_framework.generics import ListAPIView, GenericAPIView
from project.feed.models.admin_ad import AdminAd
from project.api.admin_ad.serializer import AdminAdSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from project.feed.models import admin_ad


class ListAdView(ListAPIView):
    serializer_class = AdminAdSerializer
    queryset = AdminAd.objects.all()


class AddAdImage(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminAdSerializer

    def post(self, request):
        admin_ad.image = request.data.get('image')
        admin_ad.save()
        return Response(self.serializer_class(admin_ad).data, status.HTTP_200_OK)

    def get_queryset(self):
        return self.queryset.filter(is_active=True)