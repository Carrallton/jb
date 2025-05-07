from django.contrib import admin
from django import forms
from leaflet.admin import LeafletGeoAdmin
from .models import WalkingRoute, RoutePoint, RouteCategory
from gpxpy import parse as gpx_parse
from django.core.files.uploadedfile import SimpleUploadedFile
import tempfile

class RoutePointInline(admin.TabularInline):
    model = RoutePoint
    extra = 1
    fields = ('order', 'latitude', 'longitude', 'comment', 'image')
    readonly_fields = ('latitude', 'longitude')

class RouteCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

class WalkingRouteForm(forms.ModelForm):
    class Meta:
        model = WalkingRoute
        fields = '__all__'

    def clean_gpx_file(self):
        gpx_file = self.cleaned_data.get('gpx_file')
        if gpx_file:
            try:
                gpx_content = gpx_file.read().decode('utf-8')
                gpx = gpx_parse(gpx_content)
                
                if not gpx.tracks or not gpx.tracks[0].segments or not gpx.tracks[0].segments[0].points:
                    raise forms.ValidationError("GPX file doesn't contain any track points")
                    
            except Exception as e:
                raise forms.ValidationError(f"Invalid GPX file: {str(e)}")
            
            gpx_file.seek(0)
        return gpx_file

@admin.register(WalkingRoute)
class WalkingRouteAdmin(admin.ModelAdmin):
    form = WalkingRouteForm
    list_display = ('title', 'author', 'distance_km', 'estimated_time_min', 'transport_type', 'is_published')
    list_filter = ('is_published', 'transport_type', 'categories', 'created_at')
    search_fields = ('title', 'description')
    inlines = [RoutePointInline]
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('distance_km', 'estimated_time_min')
    filter_horizontal = ('categories',)

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.author = request.user
        
        # Handle GPX file upload
        gpx_file = form.cleaned_data.get('gpx_file')
        if gpx_file:
            self.process_gpx_file(obj, gpx_file)
        
        super().save_model(request, obj, form, change)

    def process_gpx_file(self, route, gpx_file):
        try:
            gpx_content = gpx_file.read().decode('utf-8')
            gpx = gpx_parse(gpx_content)
            
            # Clear existing points
            route.points.all().delete()
            
            # Create new points from GPX
            points = []
            for i, track_point in enumerate(gpx.tracks[0].segments[0].points):
                points.append(RoutePoint(
                    route=route,
                    order=i+1,
                    latitude=track_point.latitude,
                    longitude=track_point.longitude,
                ))
            
            RoutePoint.objects.bulk_create(points)
            route.calculate_distance_and_time()
            
        except Exception as e:
            # If error occurs, just skip GPX processing
            pass

class WalkingRouteForm(forms.ModelForm):
    gpx_file = forms.FileField(
        label="GPX File",
        help_text="Upload a GPX file to automatically create route points",
        widget=forms.ClearableFileInput(attrs={'accept': '.gpx'}),
        required=False
    )

admin.site.register(RouteCategory, RouteCategoryAdmin)