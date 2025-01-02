# from rest_framework.routers import DefaultRouter
# from .views import (
#     ExpenseViewSet,
#     CategoryViewSet,
#     AddFundsViewSet,
#     MonthlyExpenseViewSet,
#     CustomTokenObtainPairViewSet,
#     ExportExpensesCSVViewSet
# )
# from django.urls import path, include
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
# from django.contrib import admin

# router = DefaultRouter()

# router.register(r'expenses', ExpenseViewSet, basename='expense')
# router.register(r'categories', CategoryViewSet, basename='category')
# router.register(r'add-funds', AddFundsViewSet, basename='add-funds')
# router.register(r'monthly-expenses', MonthlyExpenseViewSet, basename='monthly-expenses')
# router.register(r'export-expenses', ExportExpensesCSVViewSet, basename='export-expenses')
# router.register('api/login',CustomTokenObtainPairViewSet,basename="login")

# urlpatterns = [
#     # path('api/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),  # Login view
#     path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Token refresh view

#     # Include the router-generated URLs for viewsets
#     path('api/', include(router.urls)),
#     path('admin/', admin.site.urls)
# ]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

