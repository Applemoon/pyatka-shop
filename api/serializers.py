from rest_framework import serializers, exceptions
from api.models import Category, Item


class ItemSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=100
    )
    category = serializers.CharField(source='category.name', required=False)

    class Meta:
        model = Item
        fields = '__all__'

    def _getCategory(self, validated_data):
        '''
        Try to find category instance by name
        '''
        try:
            return Category.objects.get(
                name=validated_data['category']['name']
            )
        except Category.DoesNotExist:
            raise exceptions.NotFound("Category does not exist")

    def create(self, validated_data):
        new_data = validated_data.copy()
        if 'category' in validated_data:
            new_data['category'] = self._getCategory(validated_data)
        return Item.objects.create(**new_data)

    def update(self, instance, validated_data):
        for validated_field in validated_data:
            if validated_field == 'category':
                value = self._getCategory(validated_data)
            else:
                value = validated_data[validated_field]
            setattr(instance, validated_field, value)
        instance.save()
        return instance


class CategorySerializer(serializers.ModelSerializer):
    item_set = ItemSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = '__all__'
