// pages/recipe/[id].js
import { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import { universalApi } from '../../utils/api';
import styles from '../../styles/Basic/RecipePage.module.css';
import Layout from '../../components/layout';
import CommentsSection from '../../components/Recipe_interaction/comment_section';

const RecipePage = () => {
  const router = useRouter();
  const { id } = router.query;

  const [recipe, setRecipe] = useState(null);

  useEffect(() => {
    const fetchRecipe = async () => {
      try {
        const response = await universalApi(`recipes/${id}/`, 'GET');
        if (response && response.recipe && response.ingredients) {
          const ingredientsWithDetails = await Promise.all(
            response.ingredients.map(async (ingredient) => {
              const ingredientDetails = await fetchIngredientDetails(ingredient.ingredient);
              return {
                ...ingredient,
                ingredientDetails,
              };
            })
          );

          setRecipe({
            ...response,
            ingredients: ingredientsWithDetails,
          });
        } else {
          console.error('Invalid API response structure:', response);
        }
      } catch (error) {
        console.error('Error getting recipe:', error);
      }
    };

    if (id) {
      fetchRecipe();
    }
  }, [id]);

  const fetchIngredientDetails = async (ingredientId) => {
    try {
      const response = await universalApi(`ingredients/${ingredientId}/`, 'GET');
      return response;
    } catch (error) {
      console.error('Error getting ingredient details:', error);
      return null;
    }
  };

  if (!recipe) {
    return <p>Loading...</p>;
  }

  return (
      <Layout>
          <div className={styles.recipeContainer}>
          <div className={styles.recipeDetails}>
            <div className={styles.recipeTitle}>{recipe.recipe.title}</div>
            <div className={styles.recipeDescription}>{recipe.recipe.description}</div>
            <div className={styles.recipeInstructions}>
              <h3>Instructions:</h3>
              {recipe.recipe.instruction}
            </div>
            <div className={styles.recipeIngredients}>
              <h3>Ingredients:</h3>
              <ul className={styles.ingredientsList}>
                {recipe.ingredients.map((ingredient, index) => (
                  <li key={index}>
                    {ingredient.ingredientDetails && ingredient.ingredientDetails.name} - {ingredient.quantity} {ingredient.unit}
                  </li>
                ))}
              </ul>
            </div>
            <CommentsSection recipe_id={id} />
          </div>
        </div>
      </Layout>
  );
};

export default RecipePage;
