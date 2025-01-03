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

# from rest_framework import serializers
# from .models import Expense, Category, SubCategory, User
# from .serializers import CategorySerializer, SubCategorySerializer, UserSerializer

# class ExpenseSerializer(serializers.ModelSerializer):
#     # Use nested serializers for read operations
#     category = CategorySerializer(read_only=True)
#     subcategory = SubCategorySerializer(read_only=True)
#     user = UserSerializer(read_only=True)

#     # Use PrimaryKeyRelatedField for write operations
#     category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), source='category', write_only=True, required=False)
#     subcategory_id = serializers.PrimaryKeyRelatedField(queryset=SubCategory.objects.all(), source='subcategory', write_only=True, required=False)

#     # Custom fields for image paths
#     transaction_image = serializers.SerializerMethodField()
#     bill_image = serializers.SerializerMethodField()

#     class Meta:
#         model = Expense
#         fields = '__all__'
#         read_only_fields = ('user', 'total_amount')

#     def get_transaction_image(self, obj):
#         # Return the relative URL for the transaction image
#         request = self.context.get('request')
#         if obj.transaction_image and request:
#             return request.build_absolute_uri(obj.transaction_image.url)
#         return None

#     def get_bill_image(self, obj):
#         # Return the relative URL for the bill image
#         request = self.context.get('request')
#         # print(request,"request")
#         # print(obj,"obj")
#         if obj.bill_image and request:
#             print(request.build_absolute_uri(obj.bill_image.url),"image url")
#             return request.build_absolute_uri(obj.bill_image.url)
#         return None


#     def update(self, instance, validated_data):
#         # Extract category and subcategory from validated_data
#         category = validated_data.pop('category', None)
#         subcategory = validated_data.pop('subcategory', None)

#         # Update the Expense instance with the validated data
#         for attr, value in validated_data.items():
#             setattr(instance, attr, value)

#         # If category_id and subcategory_id are provided, update the instance
#         if 'category' in validated_data:
#             instance.category = validated_data['category']
#         if 'subcategory' in validated_data:
#             instance.subcategory = validated_data['subcategory']
        
#         # Ensure total_amount is recalculated based on price and quantity
#         instance.total_amount = instance.price * instance.quantity

#         instance.save()
#         return instance


class ExpenseSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    subcategory = SubCategorySerializer(read_only=True)
    user = UserSerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), source='category', write_only=True, required=False)
    subcategory_id = serializers.PrimaryKeyRelatedField(queryset=SubCategory.objects.all(), source='subcategory', write_only=True, required=False)
    
    class Meta:
        model = Expense
        fields = '__all__'
        read_only_fields = ('user', 'total_amount')

    def create(self, validated_data):
        # Get the category and subcategory instances directly from validated_data
        category = validated_data['category']
        subcategory = validated_data['subcategory']
        
        # Create the expense instance with the retrieved category and subcategory
        expense = Expense.objects.create(
            user=validated_data['user'],
            description=validated_data['description'],
            transaction_image=validated_data['transaction_image'],
            bill_image=validated_data['bill_image'],
            payment_mode=validated_data['payment_mode'],
            price=validated_data['price'],
            quantity=validated_data['quantity'],
            # expense_date=validated_data['expense_date'],
            category=category,
            subcategory=subcategory
        )
        
        # Return the created expense instance
        return expense
    def to_representation(self, instance):
        """
        Override this method to remove the domain from the URLs in the response.
        """
        representation = super().to_representation(instance)

        # Modify URLs for transaction_image and bill_image
        request = self.context.get('request')
        if request:
            # Remove domain and just return the path
            if representation.get('transaction_image'):
                representation['transaction_image'] = request.build_absolute_uri(representation['transaction_image']).replace(f"{request.scheme}://{request.get_host()}", "")
            if representation.get('bill_image'):
                representation['bill_image'] = request.build_absolute_uri(representation['bill_image']).replace(f"{request.scheme}://{request.get_host()}", "")

        return representation