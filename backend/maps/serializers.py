from rest_framework import serializers
from .models import Menu, Facility, Restaurant, Tag

class MenuSerializer(serializers.ModelSerializer):
    facility_name = serializers.SerializerMethodField()

    class Meta:
        model = Menu
        fields = ['id', 'facility', 'facility_name', 'date', 'items_by_corner']

    def get_facility_name(self, obj):
        return obj.facility.name if obj.facility else None


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']

class RestaurantSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    open_hours = serializers.SerializerMethodField()

    class Meta:
        model = Restaurant
        fields = [
            'id', 'name', 'address', 'category', 'trav_time', 'place', 
            'avg_Price', 'tags', 'times', 'image', 'NaverMap', 
            'OneLiner', 'open_hours'
        ]

    def get_open_hours(self, obj):
        return obj.get_open_hours()

    def create(self, validated_data):
        tags_data = validated_data.pop('tags')
        restaurant = Restaurant.objects.create(**validated_data)
        for tag_data in tags_data:
            tag, created = Tag.objects.get_or_create(name=tag_data['name'])
            restaurant.tags.add(tag)
        return restaurant

    def update(self, instance, validated_data):
        tags_data = validated_data.pop('tags')
        instance.name = validated_data.get('name', instance.name)
        instance.address = validated_data.get('address', instance.address)
        instance.category = validated_data.get('category', instance.category)
        instance.trav_time = validated_data.get('trav_time', instance.trav_time)
        instance.place = validated_data.get('place', instance.place)
        instance.avg_Price = validated_data.get('avg_Price', instance.avg_Price)
        instance.times = validated_data.get('times', instance.times)
        instance.image = validated_data.get('image', instance.image)
        # instance.MapLink = validated_data.get('MapLink', instance.MapLink)
        instance.NaverMap = validated_data.get('NaverMap', instance.NaverMap)
        instance.OneLiner = validated_data.get('OneLiner', instance.OneLiner)
        instance.save()

        instance.tags.clear()
        for tag_data in tags_data:
            tag, created = Tag.objects.get_or_create(name=tag_data['name'])
            instance.tags.add(tag)

        return instance