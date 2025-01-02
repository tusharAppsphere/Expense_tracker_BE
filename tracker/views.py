from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from django.db.models import Sum
from rest_framework.decorators import action
from .models import User, Expense, Category, SubCategory
from .serializers import (
    ExpenseSerializer,
    CategorySerializer,
    SubCategorySerializer,
    AddFundsSerializer,
    MonthlyExpenseSerializer,
    UserSerializer
)
from django.http import HttpResponse
import csv


# Custom permission for admin-only access
class IsAdminPermission(IsAuthenticated):
    def has_permission(self, request, view):
        # Allow access only for admin users
        return request.user.user_type == 'admin'


# ViewSet for Expense
class ExpenseViewSet(viewsets.ModelViewSet):
    serializer_class = ExpenseSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Get expenses for the authenticated user, or for all users if the user is an admin.
        """
        if self.request.user.user_type == 'admin':
            return Expense.objects.all()
        return Expense.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """
        Create a new expense entry with the authenticated user.
        """
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def getCategoryWiseExpense(self,request):
        month = request.GET.get('month')
        print(month,"monthhh")
        expenses = (
            Expense.objects.filter(expense_date__month=month)
            .values('category__category_name')
            .annotate(total_expense=Sum('total_amount'))
        )

        data = [
            {
                "category_name": expense['category__category_name'],
                "total_expense": expense['total_expense']
            }
            for expense in expenses
        ]

        return Response(data)


# ViewSet for Category (Admin only)
class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = []  # Admin only permission

    def get_queryset(self):
        """
        Return all categories only for admin users.
        """
        return Category.objects.all()

    def perform_create(self, serializer):
        """
        Create a new category, only accessible to admins.
        """
        serializer.save()


# ViewSet for AddFunds (Admin only)
class AddFundsViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminPermission]  # Admin only permission

    def create(self, request):
        """
        Add funds to a user account. Only accessible to admins.
        """
        serializer = AddFundsSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            funds = serializer.validated_data['funds']
            try:
                user = User.objects.get(email=email)
                user.funds += funds
                user.save()
                return Response({"detail": "Funds added successfully."}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ViewSet for Monthly Expenses
class MonthlyExpenseViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request):
        """
        Get the total expenses for the given month and year for the authenticated user.
        """
        serializer = MonthlyExpenseSerializer(data=request.data)
        if serializer.is_valid():
            month = serializer.validated_data['month']
            year = serializer.validated_data['year']
            expenses = Expense.objects.filter(
                expense_date__year=year,
                expense_date__month=month,
                user=request.user if request.user.user_type != 'admin' else None
            )
            total = expenses.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
            return Response({"total_monthly_expense": total}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ViewSet for exporting expenses to CSV (Admin only)
class ExportExpensesCSVViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminPermission]  # Admin only permission

    def list(self, request):
        """
        Export all expenses to a CSV file. Only accessible to admins.
        """
        expenses = Expense.objects.all()
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="expenses.csv"'

        writer = csv.writer(response)
        writer.writerow(['User', 'Description', 'Amount', 'Category', 'Subcategory', 'Date'])

        for expense in expenses:
            writer.writerow([
                expense.user.naam,
                expense.description,
                expense.total_amount,
                expense.category.category_name,
                expense.subcategory.subcategory_name,
                expense.expense_date
            ])

        return response


from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
class CustomTokenObtainPairViewSet(viewsets.ViewSet):
    """
    Custom ViewSet to return the JWT access and refresh tokens with the user_type.
    """

    permission_classes = [AllowAny]  # No authentication required for login

    def create(self, request):
        """
        Handle user login, return JWT tokens along with user_type.
        """
        # Get username and password from the request data
        email = request.data.get('email')
        password = request.data.get('password')
        
        # Authenticate the user
        user = authenticate(email=email, password=password)
        userdata = UserSerializer(user)  
        
        
        if user is not None:
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            
            return Response({
                'access': access_token,
                'refresh': refresh_token,
                'user':userdata.data
            })
        
        # If authentication fails, return error response
        return Response({'detail': 'Invalid credentials'}, status=400)
    
from rest_framework_api_key.permissions import HasAPIKey
    
class UserDetailViewSet(viewsets.ViewSet):
    """
    API endpoint to return user details based on the provided access token.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminPermission]

    def list(self, request):
        """
        Retrieve the user's details using the decoded token.
        """
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=200)
    @action(detail=False, methods=['get'])
    def getall(self,request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)  
        return Response(serializer.data, status=200)