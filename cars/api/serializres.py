from rest_framework import serializers
from cars.models import Car
from jp_center.models import FrontCar





class CarSerializer(serializers.ModelSerializer):
    make = serializers.SerializerMethodField()
    model = serializers.SerializerMethodField()
    color = serializers.SerializerMethodField()
    kpp = serializers.SerializerMethodField()
    priv = serializers.SerializerMethodField()
    
    class Meta:
        model = Car
        fields = '__all__'
    
    def get_kpp(self, obj):
        return obj.kpp.true_kpp if obj.kpp else None
    
    def get_priv(self, obj):
        return obj.priv.true_priv if obj.priv else None
    
    def get_make(self, obj):
        return obj.make.name if obj.make else None

    def get_model(self, obj):
        return obj.model.name if obj.model else None

    def get_color(self, obj):
        return obj.color.true_color if obj.color else None

class MainPageSerializer(serializers.ModelSerializer):
    make = serializers.SerializerMethodField()
    model = serializers.SerializerMethodField()
    color = serializers.SerializerMethodField()
    kpp = serializers.SerializerMethodField()
    privod = serializers.SerializerMethodField()
    export_country = serializers.SerializerMethodField()
    body_type = serializers.SerializerMethodField()
    wheel_position = serializers.SerializerMethodField()


    class Meta:
        model = FrontCar
        fields = '__all__'
    
    def get_kpp(self, obj):
        return obj.kpp.true_kpp if obj.kpp else None
    
    def get_privod(self, obj):
        return obj.privod.true_priv if obj.privod else None
    
    def get_export_country(self, obj):
        return obj.export_country.name if obj.export_country else None
    
    def get_body_type(self, obj):
        return obj.body_type.name if obj.body_type else None
    
    def get_wheel_position(self, obj):
        return obj.wheel_position.name if obj.wheel_position else None
    
    def get_make(self, obj):
        return obj.make.name if obj.make else None

    def get_model(self, obj):
        return obj.model.name if obj.model else None

    def get_color(self, obj):
        return obj.color.true_color if obj.color else None