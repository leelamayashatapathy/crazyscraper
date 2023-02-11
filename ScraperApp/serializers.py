from .models import ScrapeData
from  rest_framework.serializers import ModelSerializer
class ScrapeDataSerializer(ModelSerializer):
    class Meta:
        model =ScrapeData
        fields = '__all__'