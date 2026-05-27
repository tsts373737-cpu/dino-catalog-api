from rest_framework import serializers
from .models import Period, Diet, Dinosaur


class PeriodSerializer(serializers.ModelSerializer):
    """Сериализатор для геологического периода."""
    class Meta:
        model = Period
        fields = ['id', 'name', 'start_mya', 'end_mya']


class DietSerializer(serializers.ModelSerializer):
    """Сериализатор для типа питания."""
    class Meta:
        model = Diet
        fields = ['id', 'name', 'description']


class DinosaurSerializer(serializers.ModelSerializer):
    """
    Сериализатор для динозавра.
    При чтении показывает полную информацию о периоде и питании.
    При записи принимает только id периода и id питания.
    """
    # Для чтения — вложенные объекты с деталями
    period_detail = PeriodSerializer(source='period', read_only=True)
    diet_detail = DietSerializer(source='diet', read_only=True)

    # Для записи — только id
    period_id = serializers.PrimaryKeyRelatedField(
        queryset=Period.objects.all(),
        source='period',
        write_only=True,
        help_text='ID геологического периода'
    )
    diet_id = serializers.PrimaryKeyRelatedField(
        queryset=Diet.objects.all(),
        source='diet',
        write_only=True,
        help_text='ID типа питания'
    )

    class Meta:
        model = Dinosaur
        fields = [
            'id',
            'name',
            'length_m',
            'weight_t',
            'period_id',       # для записи
            'diet_id',         # для записи
            'period_detail',   # для чтения
            'diet_detail',     # для чтения
            'description',
        ]