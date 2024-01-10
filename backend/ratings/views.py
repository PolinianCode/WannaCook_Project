from rest_framework import viewsets
from rest_framework.response import Response
from .models import Ratings
from .serializers import RatingsSerializer
from recipes.models import Recipes

class RatingsViewSet(viewsets.ModelViewSet):
    queryset = Ratings.objects.all()
    serializer_class = RatingsSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        recipe_id = request.data['recipe']
        recipe = Recipes.objects.get(id=recipe_id)
        recipe.rating_num += 1
        recipe.rating_sum += request.data['value']
        recipe.save()

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)

    def destroy(self, request, pk=None):
        instance = self.get_object()

        recipe_id = instance.recipe.id
        recipe = Recipes.objects.get(id=recipe_id)
        recipe.rating_num -= 1
        recipe.rating_sum -= instance.value
        recipe.save()

        self.perform_destroy(self.get_object())
        return Response(status=204)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        difference = request.data['value'] - instance.value

        recipe_id = instance.recipe.id
        recipe = Recipes.objects.get(id=recipe_id)
        recipe.rating_sum += difference
        recipe.save()
        
        self.perform_update(serializer)

        return Response(serializer.data)
            