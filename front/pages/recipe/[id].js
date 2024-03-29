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
      
      console.log('Selected rating:', stars);
      
      if (rating !== null) {
        console.log("PATCH")
        universalApi(`ratings/${rating.id}/`, 'PATCH', { recipe: id, user: userData.user, value: stars });
      }
      else {
        const response = await universalApi(`ratings/`, 'POST', { recipe: id, user: userData.id, value: stars });
        setRating(response); 
      }
      
    } catch (error) {
      console.error('Error updating rating:', error);
    }
  };
  
  const deleteRating = async () => {
    try {
      universalApi(`ratings/${rating.id}/`, 'DELETE');
      setRating(null);
    } catch (error) {
      console.error('Error deleting rating:', error);
    }
  }

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
            
            setUserData(response);
            const rating_response = await universalApi(`ratings/get_rating_by_user_recipe/?user=${response.id}&recipe=${id}`, 'GET');
            if (!(rating_response instanceof Promise)) {
              console.log("TEST")
              setRating(rating_response);
              console.log("NOT PROMISE")
            }
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
  }, [id, authStatus]);

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
              {rating !== null ? (
                <div>
                <ReactStars 
                count={5}
                value={rating.value} 
                size={24}
                half={false} 
                color2={'#ffd700'}
                onChange={rate}
                />
                <button
                  className={styles.deleteRating}
                  onClick={() => deleteRating()}
                  >Delete rating</button>
                </div> 
                ): (
                  <ReactStars 
                  count={5}
                  value={0} 
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
