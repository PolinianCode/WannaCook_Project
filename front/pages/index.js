
import Layout from "../components/layout"
import Head from 'next/head';
import { universalApi } from "../utils/api";
import RecipeCard from "../components/Basic/RecipeCardComponent";
import styles from "../styles/Basic/Grid4.module.css"

import { useState, useEffect } from 'react';






export default function Home() {
  const [recipes, setRecipes] = useState([]);

  useEffect(() => {
    const fetchHomepageRecipes = async () => {
      try {
        const response = await universalApi('recipes/get_homepage_recipes/', 'GET');
        console.log(response);

        setRecipes(response);
      } catch (error) {
        console.error('Error fetching homepage recipes:', error);
      }
    };

    fetchHomepageRecipes();
  }, []);

  return (
    <>
     <Layout>
      <Head>
        <title>Wanna Cook</title>
      </Head>

      <div>
      <div>
      <h1>Wanna Cook</h1>
      </div>
        <div>
          <h2>Newest recipes</h2>
        </div>
        <div className={styles.grid}>
          {recipes.map((recipe) => (
              <RecipeCard 
                  key={recipe.recipe_id} 
                  title={recipe.title} 
                  description={recipe.description} 
                  category={recipe.category}
                  rating={(recipe.rating_sum / recipe.rating_num).toFixed(1)} 
                  recipe_id={recipe.id}
              />
          ))}
        </div>  
      </div>      

     </Layout>
    </>
  )
}
