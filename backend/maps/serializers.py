from rest_framework import serializers
from .models import Menu, Facility

class MenuSerializer(serializers.ModelSerializer):
    facility_name = serializers.SerializerMethodField()

    class Meta:
        model = Menu
        fields = ['id', 'facility', 'facility_name', 'date', 'items_by_corner']

    def get_facility_name(self, obj):
        return obj.facility.name if obj.facility else None
