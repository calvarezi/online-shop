from django.urls import path
from productos.views import SearchResultsView, ProductoDetailView, SignupView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('home/', views.lista_productos, name='lista-productos' ),
    path('buscar/', SearchResultsView.as_view(), name='buscar'),
    path('producto/<slug:slug>/', ProductoDetailView.as_view(), name='detalle-producto'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('signup/', SignupView.as_view(), name='signup'),


]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
