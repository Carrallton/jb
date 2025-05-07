from rest_framework import serializers
from .models import WalkingRoute, RoutePoint, RouteCategory
from django.urls import reverse

class RouteCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = RouteCategory
        fields = ['id', 'name', 'slug', 'icon']

class RoutePointSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = RoutePoint
        fields = ['order', 'latitude', 'longitude', 'comment', 'image_url']

    def get_image_url(self, obj):
        if obj.image:
            return self.context['request'].build_absolute_uri(obj.image.url)
        return None

class WalkingRouteSerializer(serializers.ModelSerializer):
    points = RoutePointSerializer(many=True, read_only=True)
    author = serializers.StringRelatedField()
    categories = RouteCategorySerializer(many=True, read_only=True)
    gpx_download_url = serializers.SerializerMethodField()
    main_image_url = serializers.SerializerMethodField()

    class Meta:
        model = WalkingRoute
        fields = [
            'id', 'title', 'slug', 'description', 'created_at', 'updated_at',
            'author', 'is_published', 'points', 'categories', 'main_image_url',
            'transport_type', 'distance_km', 'estimated_time_min', 'gpx_download_url'
        ]

    def get_gpx_download_url(self, obj):
        if obj.gpx_file:
            return self.context['request'].build_absolute_uri(
                reverse('route-gpx-download', kwargs={'pk': obj.pk}))
        return None

    def get_main_image_url(self, obj):
        if obj.main_image:
            return self.context['request'].build_absolute_uri(obj.main_image.url)
        return None

class GPXUploadSerializer(serializers.Serializer):
    gpx_file = serializers.FileField()

    def validate_gpx_file(self, value):
        # Basic validation that the file is GPX
        if not value.name.lower().endswith('.gpx'):
            raise serializers.ValidationError("File must be a GPX file")
        return value