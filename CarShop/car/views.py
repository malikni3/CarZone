from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse_lazy
from .models import Car, Brand, Category, Order
from .forms import OrderForm, LoginForm, BrandForm, CategoryForm, CarForm

class CarListView(ListView):
    model = Car
    template_name = 'car/car_list.html'
    context_object_name = 'cars'

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get('q')
        brand_id = self.request.GET.get('brand')
        category_id = self.request.GET.get('category')

        if q:
            queryset = queryset.filter(title__icontains=q)
        if brand_id:
            queryset = queryset.filter(brand__id=brand_id)
        if category_id:
            queryset = queryset.filter(category__id=category_id)

        return queryset.filter(is_available=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['brands'] = Brand.objects.all()
        context['categories'] = Category.objects.all()
        return context


class CarDetailView(DetailView):
    model = Car
    template_name = 'car/car_detail.html'
    context_object_name = 'car'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order_form'] = OrderForm()
        return context


class CreateOrderView(LoginRequiredMixin, CreateView):
    model = Order
    form_class = OrderForm

    def form_valid(self, form):
        car = get_object_or_404(Car, pk=self.kwargs['car_id'])
        if not car.is_available:
            messages.error(self.request, "Sorry, this car is no longer available.")
            return redirect('car_detail', pk=car.id)

        order = form.save(commit=False)
        order.car = car
        order.buyer = self.request.user
        order.save()

        messages.success(self.request, "Order request sent! The seller will contact you.")
        return redirect('home')

class CustomLoginView(View):
    template_name = 'login.html'
    form_class = LoginForm

    def get(self, request):
        return render(request, self.template_name, {'form': self.form_class()})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, 'Invalid username or password')
        return render(request, self.template_name, {'form': form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')

class DashboardView(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = 'car/dashboard.html'
    login_url = 'login'

    def test_func(self):
        return self.request.user.is_staff

    def get(self, request):
        context = {
            'car_form': CarForm(),
            'brand_form': BrandForm(),
            'category_form': CategoryForm(),
            'cars': Car.objects.all().order_by('-id'),
            'brands': Brand.objects.all().order_by('name'),
            'categories': Category.objects.all().order_by('name'),
        }
        return render(request, self.template_name, context)

    def post(self, request):
        if 'btn_add_car' in request.POST:
            form = CarForm(request.POST, request.FILES)
            if form.is_valid():
                car = form.save(commit=False)
                car.seller = request.user
                car.save()
                messages.success(request, "Car added successfully!")
                return redirect('dashboard')
            else:
                messages.error(request, "Error adding car. Please check the form.")

        elif 'btn_add_brand' in request.POST:
            form = BrandForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, "Brand added successfully!")
                return redirect('dashboard')
            else:
                messages.error(request, "Error adding brand.")

        elif 'btn_add_category' in request.POST:
            form = CategoryForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Category added successfully!")
                return redirect('dashboard')
            else:
                messages.error(request, "Error adding category.")

        return self.get(request)

class CarUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Car
    form_class = CarForm
    template_name = 'car/edit_form.html'
    success_url = reverse_lazy('dashboard')

    def test_func(self): return self.request.user.is_staff


class CarDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Car
    template_name = 'car/delete_confirm.html'
    success_url = reverse_lazy('dashboard')

    def test_func(self): return self.request.user.is_staff


class BrandUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Brand
    form_class = BrandForm
    template_name = 'car/edit_form.html'
    success_url = reverse_lazy('dashboard')

    def test_func(self): return self.request.user.is_staff


class BrandDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Brand
    template_name = 'car/delete_confirm.html'
    success_url = reverse_lazy('dashboard')

    def test_func(self): return self.request.user.is_staff


class CategoryUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'car/edit_form.html'
    success_url = reverse_lazy('dashboard')

    def test_func(self): return self.request.user.is_staff


class CategoryDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Category
    template_name = 'car/delete_confirm.html'
    success_url = reverse_lazy('dashboard')

    def test_func(self): return self.request.user.is_staff