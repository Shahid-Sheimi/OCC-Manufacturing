from process_occ.models import Order,Quote, Product
from rest_framework import serializers



class LastOrderdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quote
        # fields = ['order_id','order_date','payment_method','current_status']
        fields = '__all__'


class ActiveOrerdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['order_id','order_date','payment_method','current_status']


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"




class QuoteSerializer(serializers.ModelSerializer):
    order_id = OrderSerializer()
    class Meta:
        model = Quote
        fields = "__all__"





class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = []