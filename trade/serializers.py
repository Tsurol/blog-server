from blog.serializers import CustomFieldsSerializer
from trade.models import Order


class OrderSerializer(CustomFieldsSerializer):
    class Meta:
        model = Order
        fields = '__all__'
