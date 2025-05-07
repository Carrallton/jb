from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from .models import WalkingRoute
from .serializers import WalkingRouteSerializer, GPXUploadSerializer
import gpxpy
import tempfile
from django.core.files.base import ContentFile

class WalkingRouteViewSet(viewsets.ModelViewSet):
    queryset = WalkingRoute.objects.filter(is_published=True).prefetch_related('points', 'categories')
    serializer_class = WalkingRouteSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by category
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(categories__slug=category)
            
        # Filter by transport type
        transport_type = self.request.query_params.get('transport_type')
        if transport_type:
            queryset = queryset.filter(transport_type=transport_type)
            
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['get'])
    def download_gpx(self, request, slug=None):
        route = self.get_object()
        if not route.gpx_file:
            return Response({'error': 'GPX file not available'}, status=status.HTTP_404_NOT_FOUND)
        
        response = HttpResponse(route.gpx_file.read(), content_type='application/gpx+xml')
        response['Content-Disposition'] = f'attachment; filename="{route.slug}.gpx"'
        return response

    @action(detail=True, methods=['post'])
    def upload_gpx(self, request, slug=None):
        route = self.get_object()
        serializer = GPXUploadSerializer(data=request.data)
        
        if serializer.is_valid():
            gpx_file = serializer.validated_data['gpx_file']
            
            try:
                # Process GPX file
                gpx_content = gpx_file.read().decode('utf-8')
                gpx = gpxpy.parse(gpx_content)
                
                # Clear existing points
                route.points.all().delete()
                
                # Create new points from GPX
                points = []
                for i, track_point in enumerate(gpx.tracks[0].segments[0].points):
                    points.append(route.points.create(
                        order=i+1,
                        latitude=track_point.latitude,
                        longitude=track_point.longitude,
                    ))
                
                # Save GPX file
                route.gpx_file.save(f'{route.slug}.gpx', ContentFile(gpx_content))
                
                # Recalculate distance and time
                route.calculate_distance_and_time()
                route.save()
                
                return Response({'status': 'GPX file uploaded and processed'})
                
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)