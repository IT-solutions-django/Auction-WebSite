from rest_framework import serializers
from cars.models import Car



class CarSerializer(serializers.ModelSerializer):
    """Используем такое большое количество методов,
    чтобы заменить 'некрасивые' значения полей 
    на более симпатичные"""

    make = serializers.SerializerMethodField() 
    model = serializers.SerializerMethodField()

    color = serializers.SerializerMethodField()
    kpp = serializers.SerializerMethodField()

    priv = serializers.SerializerMethodField()

    class Meta:
        model = Car
        fields = "__all__"

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

"""Вообще основная идея в том, 
чтобы избежать создания новых классов для новой модели
вместо этого я решил, что обе модели будут использовать 
одни и те же классы, но по разному"""

