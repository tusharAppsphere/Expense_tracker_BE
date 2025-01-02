from rest_framework import serializers
from .models import User, Expense, Category, SubCategory,CustomUserManager

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email','naam','user_type','funds'] 

# Category Serializer
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

# SubCategory Serializer
class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = '__all__'

# Add Funds Serializer
class AddFundsSerializer(serializers.Serializer):
    email = serializers.CharField()
    funds = serializers.FloatField()

# Total Monthly Expense Serializer
class MonthlyExpenseSerializer(serializers.Serializer):
    month = serializers.IntegerField()
    year = serializers.IntegerField()

from rest_framework import serializers
from .models import Expense, Category, SubCategory, User
from .serializers import CategorySerializer, SubCategorySerializer, UserSerializer

class ExpenseSerializer(serializers.ModelSerializer):
    # Use nested serializers for Category, SubCategory, and User for read operations
    category = CategorySerializer(read_only=True)
    subcategory = SubCategorySerializer(read_only=True)
    user = UserSerializer(read_only=True)

    # Use PrimaryKeyRelatedField for write operations to expect only ids
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), source='category', write_only=True, required=False)
    subcategory_id = serializers.PrimaryKeyRelatedField(queryset=SubCategory.objects.all(), source='subcategory', write_only=True, required=False)

    # Custom fields to return relative image paths instead of full URLs
    transaction_image = serializers.SerializerMethodField()
    bill_image = serializers.SerializerMethodField()

    class Meta:
        model = Expense
        fields = '__all__'
        read_only_fields = ('user', 'total_amount')  # total_amount is calculated

    def get_transaction_image(self, obj):
        # Return the relative path without the leading '../'
        if obj.transaction_image:
            # Strip off leading '../' and return the correct relative path
            return obj.transaction_image.name.lstrip('../')
        return None

    def get_bill_image(self, obj):
        if obj.bill_image:
            # Strip off leading '../' and return the correct relative path
            return obj.bill_image.name.lstrip('../')
        return None

    def update(self, instance, validated_data):
        # Extract category and subcategory from validated_data
        category = validated_data.pop('category', None)
        subcategory = validated_data.pop('subcategory', None)

        # Update the Expense instance with the validated data
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # If category_id and subcategory_id are provided, update the instance
        if 'category' in validated_data:
            instance.category = validated_data['category']
        if 'subcategory' in validated_data:
            instance.subcategory = validated_data['subcategory']
        
        # Ensure total_amount is recalculated based on price and quantity
        instance.total_amount = instance.price * instance.quantity

        instance.save()
        return instance
