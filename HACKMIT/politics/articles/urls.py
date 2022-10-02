from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path("account/", views.account, name='account'),
    path("login/", views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('search/', views.search, name='search'),

    # API Routes
    path('save/', views.save_post, name="save")
]