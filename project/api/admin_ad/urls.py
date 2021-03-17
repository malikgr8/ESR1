from django.urls import path
from project.api.admin_ad.views import ListAdView


urlpatterns = [
    path('all', ListAdView.as_view())
]