from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('app_auth.urls')),  # Додаємо аутентифікацію
    path('', include('quotes.urls')),  # Додаємо цитати
]