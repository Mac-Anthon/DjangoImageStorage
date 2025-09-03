# Django views.py - Fixed upload handler
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
import os
import uuid
from datetime import datetime

@api_view(['POST'])
def upload_image(request):
    try:
        print(f"Upload request received: {request.method}")
        print(f"Request data: {request.data}")
        print(f"Request FILES: {request.FILES}")
        
        if 'image' not in request.FILES:
            return Response({
                'success': False,
                'error': 'No image file provided'
            }, status=status.HTTP_400_BAD_REQUEST)

        image_file = request.FILES['image']
        
        # Generate unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_extension = os.path.splitext(image_file.name)[1]
        if not file_extension:
            file_extension = '.jpg'
        
        unique_filename = f"products/{timestamp}_{uuid.uuid4().hex[:8]}{file_extension}"
        
        # Save the file
        file_path = default_storage.save(unique_filename, ContentFile(image_file.read()))
        
        # Generate the full URL
        if hasattr(settings, 'MEDIA_URL') and hasattr(settings, 'MEDIA_ROOT'):
            # Use MEDIA_URL for proper URL construction
            image_url = f"{settings.MEDIA_URL}{file_path}"
        else:
            # Fallback to simple path
            image_url = f"/media/{file_path}"
        
        print(f"File saved to: {file_path}")
        print(f"Image URL: {image_url}")
        
        # Return response matching what React Native expects
        return Response({
            'success': True,
            'data': {
                'image': image_url,  # This is what your RN code looks for
                'file_path': file_path,
                'original_name': image_file.name
            },
            'message': 'Image uploaded successfully'
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        print(f"Upload error: {str(e)}")
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)









