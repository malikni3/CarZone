from django.urls import path
from .views import (
    CarListView, CarDetailView, CreateOrderView,
    CustomLoginView, LogoutView, DashboardView,
    CarUpdateView, CarDeleteView,
    BrandUpdateView, BrandDeleteView,
    CategoryUpdateView, CategoryDeleteView
)

urlpatterns = [
    # Home
    path('', CarListView.as_view(), name='home'),

    # Car Details (The new page)
    path('car/<int:pk>/', CarDetailView.as_view(), name='car_detail'),

    # Buy Action
    path('car/<int:car_id>/order/', CreateOrderView.as_view(), name='create_order'),

    # Auth (Keep these from your previous library code)
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('dashboard/', DashboardView.as_view(), name='dashboard'),

    path('car/edit/<int:pk>/', CarUpdateView.as_view(), name='update_car'),
    path('car/delete/<int:pk>/', CarDeleteView.as_view(), name='delete_car'),

    path('brand/edit/<int:pk>/', BrandUpdateView.as_view(), name='update_brand'),
    path('brand/delete/<int:pk>/', BrandDeleteView.as_view(), name='delete_brand'),

    path('category/edit/<int:pk>/', CategoryUpdateView.as_view(), name='update_category'),
    path('category/delete/<int:pk>/', CategoryDeleteView.as_view(), name='delete_category'),
]