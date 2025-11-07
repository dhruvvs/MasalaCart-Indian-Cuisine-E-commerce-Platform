from django.urls import path,include
from . import views

urlpatterns = [
    # path('', views.login, name='login'),
    path("signup.html", views.authView, name="authView"),
    # path('login.html', views.login, name='login'),
    path('', views.product, name='product'),
    path('cartDetails.html', views.cartDetails, name='cartDetails'),
    path('thankYou.html', views.thankYou, name='thankYou'),
    path('add-to-cart', views.add_to_cart, name='add_to_cart'),
    path('logout.html', views.logout_view, name='logmeout'),
    path('update_cart/', views.update_cart, name='update_cart'),
    path("accounts/", include("django.contrib.auth.urls")),
]
