from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator
from django.conf import settings
import os
import uuid
from geopy.distance import geodesic

User = get_user_model()

def route_image_upload_path(instance, filename):
    return f'route_images/{uuid.uuid4()}{os.path.splitext(filename)[1]}'

def point_image_upload_path(instance, filename):
    return f'point_images/{uuid.uuid4()}{os.path.splitext(filename)[1]}'

class RouteCategory(models.Model):
    name = models.CharField(_('name'), max_length=100)
    slug = models.SlugField(_('slug'), unique=True)
    icon = models.CharField(_('icon'), max_length=50, blank=True)

    class Meta:
        verbose_name = _('route category')
        verbose_name_plural = _('route categories')

    def __str__(self):
        return self.name

class WalkingRoute(models.Model):
    TRANSPORT_CHOICES = [
        ('walking', _('Walking')),
        ('public', _('Public Transport')),
        ('mixed', _('Mixed')),
    ]

    title = models.CharField(_('title'), max_length=255)
    slug = models.SlugField(_('slug'), unique=True)
    description = models.TextField(_('description'), blank=True)
    categories = models.ManyToManyField(RouteCategory, related_name='routes', blank=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='walking_routes')
    is_published = models.BooleanField(_('is published'), default=True)
    main_image = models.ImageField(_('main image'), upload_to=route_image_upload_path, blank=True, null=True)
    transport_type = models.CharField(_('transport type'), max_length=10, choices=TRANSPORT_CHOICES, default='walking')
    distance_km = models.FloatField(_('distance (km)'), blank=True, null=True)
    estimated_time_min = models.PositiveIntegerField(_('estimated time (min)'), blank=True, null=True)
    gpx_file = models.FileField(_('GPX file'), upload_to='gpx_files/', blank=True, null=True)

    class Meta:
        verbose_name = _('walking route')
        verbose_name_plural = _('walking routes')
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Calculate distance if points exist
        if self.pk and self.points.exists():
            self.calculate_distance_and_time()
        super().save(*args, **kwargs)

    def calculate_distance_and_time(self):
        points = list(self.points.order_by('order'))
        if len(points) < 2:
            return

        total_distance = 0.0
        for i in range(len(points)-1):
            point1 = (points[i].latitude, points[i].longitude)
            point2 = (points[i+1].latitude, points[i+1].longitude)
            total_distance += geodesic(point1, point2).kilometers

        self.distance_km = round(total_distance, 2)
        
        # Calculate estimated time based on transport type
        if self.transport_type == 'walking':
            avg_speed_km_h = 5  # average walking speed
        elif self.transport_type == 'public':
            avg_speed_km_h = 15  # average public transport speed
        else:  # mixed
            avg_speed_km_h = 8
            
        self.estimated_time_min = int((total_distance / avg_speed_km_h) * 60)

class RoutePoint(models.Model):
    route = models.ForeignKey(WalkingRoute, on_delete=models.CASCADE, related_name='points')
    order = models.PositiveIntegerField(_('order'))
    latitude = models.DecimalField(_('latitude'), max_digits=9, decimal_places=6)
    longitude = models.DecimalField(_('longitude'), max_digits=9, decimal_places=6)
    comment = models.TextField(_('comment'), blank=True)
    image = models.ImageField(_('image'), upload_to=point_image_upload_path, blank=True, null=True)

    class Meta:
        verbose_name = _('route point')
        verbose_name_plural = _('route points')
        ordering = ['order']

    def __str__(self):
        return f"Point {self.order} for {self.route.title}"