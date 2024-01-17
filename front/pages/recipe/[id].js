"use client"
import { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import { universalApi } from '../../utils/api';
import styles from '../../styles/Basic/RecipePage.module.css';
import Layout from '../../components/layout';
import CommentsSection from '../../components/Recipe_interaction/comment_section';
import Head from 'next/head';
import Cookies from 'js-cookie';
import AuthContext from '../../contexts/authContext';
import { useContext } from 'react';

import React from 'react'; 
import ReactStars from 'react-stars'

const RecipePage = () => {
  const router = useRouter();
  const { id } = router.query;
  const { authStatus } = useContext(AuthContext);

  const [recipe, setRecipe] = useState(null);
  const [rating, setRating] = useState(null);
  const [userData, setUserData] = useState(null);
  
  
  const rate = async (stars) => {
    try {
      // Assuming you have a function to send the rating to the server
      // await sendRatingToServer(stars);
      // Update the local state with the selected rating
      
      setRating(stars);
      console.log(rating)
      // Other UI update logic as needed
      console.log('Selected rating:', stars);
      if (rating !== null) {
        universalApi(`ratings/${rating.id}/`, 'PATCH', { recipe: id, user: rating.user, value: stars });
      }
      else {
        universalApi(`ratings/`, 'POST', { recipe_id: id, user_id: userData.id, value: stars });
      }
    } catch (error) {
      console.error('Error updating rating:', error);
    }
  };
  

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

          
          if (authStatus === true) {
            const response = await universalApi('user/user_data/', 'GET', { token: Cookies.get('token') });
            const rating_response = await universalApi(`ratings/get_rating_by_user_recipe/?user_id=${response.id}&recipe_id=${id}`, 'GET');
            console.log("AAAAAAAAAA")
            setRating(rating_response);
          };


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
          <Head>
            <title>{recipe.recipe.title}</title>
          </Head>
          <div className={styles.recipeContainer}>
          <div className={styles.recipeDetails}>
            <div className={styles.recipeTitle}>{recipe.recipe.title}</div>
            <div className={styles.recipeDescription}>{recipe.recipe.description}</div>

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

            <div className={styles.recipeInstructions}>
              <h3>Instructions:</h3>
              {recipe.recipe.instruction}
            </div>
            
            <div> 
              {rating !== null && (
                <ReactStars 
                count={5}
                value={rating.value} 
                size={24}
                half={false} 
                color2={'#ffd700'}
                onChange={rate}
                 /> 
              )}
            </div> 
              <CommentsSection recipe_id={id} />
            </div>
          </div>
        
      </Layout>
  );
};

export default RecipePage;
