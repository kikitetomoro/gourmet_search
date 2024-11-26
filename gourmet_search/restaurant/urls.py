from django.urls import path
from . import views

app_name = "restaurant"  

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search_results, name="search_results"),
    # path("shop/<str:shop_id>/", views.shop_detail, name="shop_detail"),
]