from rest_framework.routers import DefaultRouter
from .views import ProductViewSet
from django.urls import path

from . import views

router = DefaultRouter()
router.register("products", ProductViewSet, basename="product")

urlpatterns = router.urls

urlpatterns = [
    path("demo/", views.ProductAPIView.as_view()),
    path(
        "products-generic/",
        views.ProductListGenericView.as_view(),
        name="product-list-generic",
    ),
    path(
        "products-create-generic/",
        views.ProductCreateGenericView.as_view(),
        name="product-create-generic",
    ),
    path(
        "products-generic/<int:pk>/",
        views.ProductRetrieveGenericView.as_view(),
        name="product-retrieve-generic",
    ),
    path(
        "products-update/<int:pk>/",
        views.ProductUpdateGenericView.as_view(),
        name="product-update-generic",
    ),
    path(
        "products-delete/<int:pk>/",
        views.ProductDeleteGenericView.as_view(),
        name="product-delete-generic",
    ),
] + router.urls
