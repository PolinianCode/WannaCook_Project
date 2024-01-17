from rest_framework import viewsets
from rest_framework.response import Response
from .models import Ratings
from .serializers import RatingsSerializer
from recipes.models import Recipes
from rest_framework.decorators import action
from rest_framework import status


class RatingsViewSet(viewsets.ModelViewSet):
    queryset = Ratings.objects.all()
    serializer_class = RatingsSerializer

    @action(detail=False, methods=['GET'])
    def get_rating_by_user_recipe(self, request):
        try:
            rating = Ratings.objects.get(user_id=request.query_params.get('user_id'), recipe_id = request.query_params.get('recipe_id'))
            #rating = Ratings.objects.filter(user_id=request.query_params.get('user_id'), recipe_id = request.query_params.get('recipe_id'))
            serializer = self.get_serializer(rating, many=False)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"message": "Error getting ratings by user_id"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




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
            