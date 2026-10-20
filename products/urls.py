from django.urls import path

from . import views

urlpatterns = [
    # path("", views.product_list, name="product_list"),
    # path("<int:product_id>/", views.product_detail, name="product_detail"),
    path("search/", views.product_search, name="product_search"),
    path(
        "home/",
        views.StoreHomeView.as_view(),
        name="store_home",
    ),
    path(
        "",
        views.ProductListView.as_view(),
        name="product_list",
    ),
    path(
        "<int:product_id>/",
        views.ProductDetailView.as_view(),
        name="product_detail",
    ),
    path(
        "create/",
        views.product_create,
        name="product_create",
    ),
]
