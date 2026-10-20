from .models import Product
from .forms import ProductForm
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import TemplateView, ListView, DetailView


class StoreHomeView(TemplateView):
    template_name = "products/home.html"


class ProductListView(ListView):
    model = Product
    template_name = "products/product_list.html"
    context_object_name = "products"


class ProductDetailView(DetailView):
    model = Product
    template_name = "products/product_detail.html"
    context_object_name = "product"
    pk_url_kwarg = "product_id"


def product_create(request):

    if request.method == "POST":
        form = ProductForm(request.POST)

        if form.is_valid():
            product = form.save()
            return redirect("product_detail", product_id=product.id)

    else:
        form = ProductForm()

    return render(
        request,
        "products/product_form.html",
        {"form": form},
    )


def product_list(request):
    products = Product.objects.all()

    return render(
        request,
        "products/product_list.html",
        {"products": products},
    )
    # return HttpResponse("Welcome to our products page!")


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    return render(
        request,
        "products/product_detail.html",
        {"product": product},
    )
    # return HttpResponse(
    #     f"Product: {product.name}, Price: {product.price}, Stock: {product.stock}"
    # )


def product_search(request):
    search = request.GET.get("search", "")
    category = request.GET.get("category", "")

    return HttpResponse(f"Search: {search}, Category: {category}")
