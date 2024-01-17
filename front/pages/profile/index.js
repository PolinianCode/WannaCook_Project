"use client"

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
  const [isEditing, setIsEditing] = useState(false);
  const [value, setValue] = useState('');
  

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

  const handleEdit = () => {
    setIsEditing(true);
  }

  const handleChange = async (e) => {

    console.log(value);
    
    if(value.length > 0){
      const response = await universalApi('user/edit_username/', 'PATCH', { token: Cookies.get('token'), username: value });
      setUser({
        ...user,
        username: value,
      });
    }



    setIsEditing(false);
  }

  return (
    
    <Layout>
      <Head>
        <title>Profile</title>
      </Head>
      <div style={{ marginTop: '50px', width: '100%'}}>
        {user ? (
          <div styles={{
            width: '100%',
          }}>
           <div
            style={{
              display: 'flex',
              justifyContent: 'flex-start',
              flexDirection: 'row', 
            }}
           >
            <h2
                style={{
                  fontSize: '40px',
                  fontWeight: 'bold',
                  marginBottom: '50px',
                  alignItems: 'center',
                }}
              > 
                {isEditing ? (
                  <div
                  style={{
                    display: 'flex',
                    flexDirection: 'row',
                    alignItems: 'center',
                  }}>
                    Hello,<input type="text" onChange={e => { setValue(e.currentTarget.value); }}
                      style={{
                        outline: 'none',
                        borderColor: '#0000000'
                        
                      }}
                    />
                    <button style={{ alignSelf: 'center' }}  onClick={(e) =>handleChange(e)}>
                      Save

                    </button>

                  </div>
                ) : (
                  <div style={{
                    width: '100%',
                    display: 'flex',
                    flexDirection: 'row',
                  }}>
                    <b>Hello,{user.username}!</b>
                    <button style={{ alignSelf: 'center' }} onClick={handleEdit}>Edit</button>
                  </div>
                )}
              </h2>
           </div>

            <div style={{ marginTop: '50px' }} className={addStyles.actionButtons} styles={{
              width: '100%',
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
              marginBottom: '50px',

            }}>

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
