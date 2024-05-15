from rest_framework import serializers
from maps.models import Building, Facility, Menu, Restaurant, Tag

class BuildingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Building
        fields = '__all__'

class FacilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Facility
        fields = '__all__'

class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class RestaurantSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)

    class Meta:
        model = Restaurant
        fields = '__all__'
