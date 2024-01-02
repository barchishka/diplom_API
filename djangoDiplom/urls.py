"""
URL configuration for djangoDiplom project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from backend.views import *
# from backend.views import Home
from rest_framework import routers
from django_rest_passwordreset.views import reset_password_confirm, reset_password_request_token

router = routers.SimpleRouter()
router.register(r'user', UserViewSet)
router.register(r'product', ProductViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    path('', include(router.urls)),
    # path('', Home.as_view(), name='home'),

    path('user/register', RegisterAccount.as_view(), name='user-register'),
    path('user/register/confirm', Сonfirmation.as_view(), name='user-register-confirm'),
    path('user/login', LoginUser.as_view(), name='user-login'),
    path('user/contact', ContactView.as_view(), name='user-contacts'),
    path('user/contacts', ContactAPIList.as_view(), name='user-contacts'),
    path('user/details', DetailUser.as_view(), name='user-details'),
    path('user/password_reset', reset_password_request_token, name='password-reset'),
    path('user/password_reset/confirm', reset_password_confirm, name='password-reset-confirm'),

    path('shops', ShopView.as_view(), name='shops'),
    path('categories', CategoryView.as_view(), name='categories'),
    path('products', ProductView.as_view(), name='products'),

    path('partner/update', PartnerUpdate.as_view(), name='partner-update'),
    path('partner/state', PartnerState.as_view(), name='partner-state'),
    path('partner/orders', PartnerOrders.as_view(), name='partner-orders'),

    path('cart', CartView.as_view(), name='cart'),
    path('order', OrderView.as_view(), name='order'),
]
app_name = 'backend'
