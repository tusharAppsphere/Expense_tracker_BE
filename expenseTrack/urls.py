from django.contrib import admin
from rest_framework.routers import DefaultRouter
from tracker.views import (
    ExpenseViewSet,
    CategoryViewSet,
    AddFundsViewSet,
    MonthlyExpenseViewSet,
    CustomTokenObtainPairViewSet,
    ExportExpensesCSVViewSet,
    UserDetailViewSet
)
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()

router.register(r'expenses', ExpenseViewSet, basename='expense')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'add-funds', AddFundsViewSet, basename='add-funds')
router.register(r'login',CustomTokenObtainPairViewSet,basename="login")
router.register(r'monthly-expenses', MonthlyExpenseViewSet, basename='monthly-expenses')
router.register(r'export-expenses', ExportExpensesCSVViewSet, basename='export-expenses')
router.register(r'user/details', UserDetailViewSet, basename="user-details")


urlpatterns = [
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls)
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
