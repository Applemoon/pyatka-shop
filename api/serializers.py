from rest_framework import serializers, exceptions
from api.models import Category, Item


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ItemSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.name', required=False)

    class Meta:
        model = Item
        fields = '__all__'

    def create(self, validated_data):
        new_data = validated_data.copy()

        if 'category' in validated_data:
            try:
                category = Category.objects.get(
                    name=validated_data['category']['name']
                )
            except Category.DoesNotExist:
                raise exceptions.NotFound("Category does not exist")
            new_data['category'] = category

        return Item.objects.create(**new_data)
