from rest_framework import serializers
from .models import ProductImage
from django.conf import settings

class ProductImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    
    class Meta:
        model = ProductImage
        fields = '__all__'
    
    def get_image(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return f"http://172.20.10.4:8000{obj.image.url}"
        return None
