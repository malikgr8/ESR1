from rest_framework.generics import ListAPIView
from project.feed.models.admin_ad import AdminAd
from project.api.admin_ad.serializer import AdminAdSerializer


class ListAdView(ListAPIView):
    serializer_class = AdminAdSerializer
    queryset = AdminAd.objects.all()

    def get_queryset(self):
        return self.queryset.filter(is_active=True)