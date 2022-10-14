from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path("account/", views.account, name='account'),
    path("login/", views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('search/', views.search, name='search'),
    path('category/<str:category>', views.category, name="category"),
    path('saved/', views.saved, name='saved'),

    # API Routes
    path('save/', views.save_post, name="save"),
    path('delete/', views.delete_post, name="delete")
]