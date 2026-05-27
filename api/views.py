from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Period, Diet, Dinosaur
from .serializers import PeriodSerializer, DietSerializer, DinosaurSerializer


class PeriodViewSet(viewsets.ModelViewSet):
    """
    Представление для геологических периодов.

    Эндпоинты:
    - GET /periods/ — список периодов
    - GET /periods/{id}/ — один период
    - POST /periods/ — создать период (один или несколько)
    - PATCH /periods/{id}/ — частично обновить период
    - DELETE /periods/{id}/ — удалить период (один или группу)

    Фильтры:
    - ?name= — поиск по названию
    """
    serializer_class = PeriodSerializer
    queryset = Period.objects.all()

    def get_queryset(self):
        qs = super().get_queryset()
        name = self.request.query_params.get('name')
        if name:
            qs = qs.filter(name__icontains=name)
        return qs

    def create(self, request, *args, **kwargs):
        """Создание одного или нескольких периодов."""
        many = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, many=many)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, *args, **kwargs):
        """Частичное обновление (PATCH) одного или группы."""
        many = isinstance(request.data, list)
        if many:
            instances = [self.queryset.get(pk=item['id']) for item in request.data]
            serializer = self.get_serializer(instances, data=request.data, partial=True, many=True)
        else:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """Удаление одного периода или группы через ?ids=1,2,3."""
        ids = request.query_params.get('ids')
        if ids:
            ids_list = [int(pk) for pk in ids.split(',')]
            self.queryset.filter(pk__in=ids_list).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return super().destroy(request, *args, **kwargs)


class DietViewSet(viewsets.ModelViewSet):
    """
    Представление для типов питания.

    Эндпоинты:
    - GET /diets/ — список типов питания
    - GET /diets/{id}/ — один тип питания
    - POST /diets/ — создать (один или несколько)
    - PATCH /diets/{id}/ — частично обновить
    - DELETE /diets/{id}/ — удалить (один или группу)

    Фильтры:
    - ?name= — поиск по названию
    """
    serializer_class = DietSerializer
    queryset = Diet.objects.all()

    def get_queryset(self):
        qs = super().get_queryset()
        name = self.request.query_params.get('name')
        if name:
            qs = qs.filter(name__icontains=name)
        return qs

    def create(self, request, *args, **kwargs):
        many = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, many=many)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, *args, **kwargs):
        many = isinstance(request.data, list)
        if many:
            instances = [self.queryset.get(pk=item['id']) for item in request.data]
            serializer = self.get_serializer(instances, data=request.data, partial=True, many=True)
        else:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        ids = request.query_params.get('ids')
        if ids:
            ids_list = [int(pk) for pk in ids.split(',')]
            self.queryset.filter(pk__in=ids_list).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return super().destroy(request, *args, **kwargs)


class DinosaurViewSet(viewsets.ModelViewSet):
    """
    Представление для динозавров.

    Эндпоинты:
    - GET /dinosaurs/ — список динозавров с фильтрами
    - GET /dinosaurs/{id}/ — один динозавр
    - POST /dinosaurs/ — создать (один или несколько)
    - PATCH /dinosaurs/{id}/ — частично обновить
    - DELETE /dinosaurs/{id}/ — удалить (один или группу)

    Фильтры:
    - ?period_id= — по ID периода
    - ?diet_id= — по ID типа питания
    - ?name= — поиск по названию
    - ?length_min= & ?length_max= — диапазон длины (м)
    - ?weight_min= & ?weight_max= — диапазон веса (т)
    """
    serializer_class = DinosaurSerializer
    queryset = Dinosaur.objects.all()

    def get_queryset(self):
        qs = super().get_queryset()
        params = self.request.query_params

        # Фильтр по периоду
        period_id = params.get('period_id')
        if period_id:
            qs = qs.filter(period_id=period_id)

        # Фильтр по типу питания
        diet_id = params.get('diet_id')
        if diet_id:
            qs = qs.filter(diet_id=diet_id)

        # Фильтр по названию
        name = params.get('name')
        if name:
            qs = qs.filter(name__icontains=name)

        # Фильтр по длине (от)
        length_min = params.get('length_min')
        if length_min:
            qs = qs.filter(length_m__gte=float(length_min))

        # Фильтр по длине (до)
        length_max = params.get('length_max')
        if length_max:
            qs = qs.filter(length_m__lte=float(length_max))

        # Фильтр по весу (от)
        weight_min = params.get('weight_min')
        if weight_min:
            qs = qs.filter(weight_t__gte=float(weight_min))

        # Фильтр по весу (до)
        weight_max = params.get('weight_max')
        if weight_max:
            qs = qs.filter(weight_t__lte=float(weight_max))

        return qs

    def create(self, request, *args, **kwargs):
        """Создание одного или нескольких динозавров."""
        many = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, many=many)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, *args, **kwargs):
        """Частичное обновление (PATCH) одного или группы."""
        many = isinstance(request.data, list)
        if many:
            instances = [self.queryset.get(pk=item['id']) for item in request.data]
            serializer = self.get_serializer(instances, data=request.data, partial=True, many=True)
        else:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """Удаление одного динозавра или группы через ?ids=1,2,3."""
        ids = request.query_params.get('ids')
        if ids:
            ids_list = [int(pk) for pk in ids.split(',')]
            self.queryset.filter(pk__in=ids_list).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return super().destroy(request, *args, **kwargs)