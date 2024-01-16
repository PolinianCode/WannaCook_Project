import { useEffect, useState } from 'react';
import { universalApi } from '../../utils/api';
import Cookies from 'js-cookie';
import Layout from '../../components/layout';
import RecipeCard from '../../components/Basic/RecipeCardComponent';
import styles from '../../styles/Basic/Grid4.module.css';
import addStyles from '../../styles/RecipePage/RecipeConstructor.module.css';
import Head from 'next/head';

export default function Profile() {
  const [user, setUser] = useState(null);
  const [recipes, setRecipes] = useState(null);
  const [favorites, setFavorites] = useState(null);
  const [displayFavorites, setDisplayFavorites] = useState(false);

  

  useEffect(() => {
    const getUserData = async () => {
      try {
        const userData = await universalApi('user/user_data/', 'GET', { token: Cookies.get('token') });
        setUser(userData);
      } catch (error) {
        console.error('Error fetching user data:', error);
      }
    };

    getUserData();
  }, []);

  useEffect(() => {
    if (user?.id) {
      const getRecipes = async (id) => {
        try {
          const recipesData = await universalApi(`recipes/get_by_user_id/${id}/`, 'GET');
          setRecipes(recipesData);
        } catch (error) {
          console.error('Error fetching recipes:', error);
        }
      };

      getRecipes(user.id);
    }
  }, [user?.id]);

  useEffect(() => {
    const fetchFavorites = async (id) => {
      try {
        const favoritesData = await universalApi(`favorites/get_by_user_id/${id}/`, 'GET');
        if (favoritesData && favoritesData.length > 0) {
          const favoritesPromises = favoritesData.map(async (favorite) => {
            try {
              const recipeData = await universalApi(`recipes/${favorite.recipe}/`, 'GET');
              return recipeData;
            } catch (error) {
              console.error('Error fetching recipe:', error);
              return null;
            }
          });

          const recipesData = await Promise.allSettled(favoritesPromises);
          const resolvedRecipes = recipesData
            .filter((result) => result.status === 'fulfilled')
            .map((result) => result.value);

          setFavorites(resolvedRecipes);
        } else {
          setFavorites([]);
        }
      } catch (error) {
        console.error('Error fetching favorites:', error);
      }
    };

    if (user?.id) {
      fetchFavorites(user.id);
    }
  }, [user?.id]);

  const handleFavorites = () => {
    setDisplayFavorites(true);
  };

  const handleRecipes = () => {
    setDisplayFavorites(false);
  };

  return (
    
    <Layout>
      <Head>
        <title>Profile</title>
      </Head>
      <div style={{ marginTop: '50px' }}>
        {user ? (
          <div>
            <h2
              style={{
                fontSize: '40px',
                fontWeight: 'bold',
                marginBottom: '50px',
              }}
            >Hello, <b>{user.username}</b>!</h2>

            <div style={{ marginTop: '50px' }} className={addStyles.actionButtons}>
              <button
                onClick={handleRecipes}
                className={`${addStyles.ingredientAddButton} ${!displayFavorites ? addStyles.active : ''}`}
              >
                My recipes
              </button>
              <button
                onClick={handleFavorites}
                className={`${addStyles.cancelBtn} ${displayFavorites ? addStyles.active : ''}`}
              >
                My favourites
              </button>
            </div>

            <div className={styles.grid}>
              {displayFavorites ? (
                favorites?.map((favorite) => (
                  <RecipeCard
                    key={favorite.recipe.id}
                    title={favorite.recipe.title}
                    description={favorite.recipe.description}
                    category={favorite.recipe.category}
                    rating={(favorite.recipe.rating_sum / favorite.recipe.rating_num).toFixed(1)}
                    recipe_id={favorite.recipe.id}
                  />
                ))
              ) : (
                recipes?.map((recipe) => (
                  <RecipeCard
                    key={recipe.id}
                    title={recipe.title}
                    description={recipe.description}
                    category={recipe.category}
                    rating={(recipe.rating_sum / recipe.rating_num).toFixed(1)}
                    recipe_id={recipe.id}
                    editable={true}
                  />
                ))
              )}
            </div>
          </div>
        ) : (
          <p>Loading user data...</p>
        )}
      </div>
    </Layout>
  );
}
