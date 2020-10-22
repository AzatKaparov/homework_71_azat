from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.views.generic.base import View
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.response import Response

from API.permissions import PermissionOrder
from webapp.models import Product, Order
from API.serializers import ProductSerializer, OrderSerializer, UserSerializer
from django.views.decorators.csrf import ensure_csrf_cookie
import json
from django.http import HttpResponse, HttpResponseNotAllowed, JsonResponse


class ProductViewSet(ViewSet):
    queryset = Product.objects.all()
    permission_classes = [PermissionOrder]

    def list(self, request):
        objects = Product.objects.all()
        slr = ProductSerializer(objects, many=True, context={'request': request})
        return Response(slr.data)

    def create(self, request):
        slr = ProductSerializer(data=request.data, context={'request': request})
        if slr.is_valid():
            prouct = slr.save()
            return Response(slr.data)
        else:
            return Response(slr.errors, status=400)

    def retrieve(self, request, pk=None):
        article = get_object_or_404(Product, pk=pk)
        slr = ProductSerializer(article, context={'request': request})
        return Response(slr.data)

    def update(self, request, pk=None):
        article = get_object_or_404(Product, pk=pk)
        slr = ProductSerializer(data=request.data, instance=article, context={'request': request})
        if slr.is_valid():
            product = slr.save()
            return Response(slr.data)
        else:
            return Response(slr.errors, status=400)

    def destroy(self, request, pk=None):
        article = get_object_or_404(Product, pk=pk)
        article.delete()
        return Response({'pk': pk})


class OrderViewSet(ViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:  # self.request.method == "GET"
            return [IsAdminUser()]
        else:
            return [AllowAny()]

    def retrieve(self, request, pk=None):
        article = get_object_or_404(Order, pk=pk)
        slr = OrderSerializer(article, context={'request': request})
        return Response(slr.data)

    def create(self, request):
        slr = OrderSerializer(data=request.data, context={'request': request})
        if slr.is_valid():
            order = slr.save()
            return Response(slr.data)
        else:
            return Response(slr.errors, status=400)


class UserViewSet(ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


@ensure_csrf_cookie
def get_token_view(request, *args, **kwargs):
    if request.method == 'GET':
        return HttpResponse()
    return HttpResponseNotAllowed('Only GET request are allowed')


class ProductCreateView(View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        slr = ProductSerializer(data=data)
        if slr.is_valid():
            article = slr.save()
            return JsonResponse(slr.data, safe=False)
        else:
            response = JsonResponse(slr.errors, safe=False)
            response.status_code = 400
            return response


