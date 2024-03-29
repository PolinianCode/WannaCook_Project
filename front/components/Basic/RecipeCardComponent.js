import { useRouter } from 'next/router'
import styles from '../../styles/Basic/RecipeCard.module.css'
import { universalApi } from '../../utils/api'
import { useEffect, useState } from 'react'
import Cookies from 'js-cookie'


export default function RecipeCard({ title, description, rating, recipe_id, category, editable = false}) {

    const router = useRouter()

    

    const [categoryDetails, setCategoryDetails] = useState(null);
    const [saved, setSaved] = useState(false);

    useEffect(() => {
        const fetchCategory = async () => {
            try {
                const response = await universalApi(`categories/${category}/`, 'GET');
                setCategoryDetails(response);
            } catch (error) {
                console.error('Error getting category details:', error);
            }
        };

        fetchCategory();
    }, [category]);

    const checkIfSaved = async () => {
        const userData = await universalApi('user/user_data/', 'GET', { token: Cookies.get('token') });
        const response = await universalApi(`favorites/favorite_exist_check/${userData.id}/${recipe_id}/`, 'GET');

        console.log(response)

        if (response.message === "Favorite exists") {
            setSaved(true);
        } else {
            setSaved(false);
        }
    }

    useEffect(() => {
        checkIfSaved();
    }, []);

    const handleSave = async (e) => {

        const userData = await  universalApi('user/user_data/', 'GET', { token: Cookies.get('token') });

        console.log("Clicked on" + recipe_id)


        const saveRecipe = {
            user: parseInt(userData.id),
            recipe: Number(recipe_id),
        }

        if(saved) {
            setSaved(false);
            await universalApi(`favorites/delete_favorite/${userData.id}/${recipe_id}/`, 'DELETE', saveRecipe)
        }else {
            setSaved(true); 
            await universalApi('favorites/', 'POST', saveRecipe);
        }
    }

    const handleEdit = async (e) => {
        router.push(`/recipe/editor/${recipe_id}`);
    }

    const handleClick = (e) => {
        router.push(`/recipe/${recipe_id}`);
      };

    return (
        <div className={styles.recipeCard}>
                <div className={styles.recipeContent} onClick={(e) => handleClick()}>
                    

                    <p className={styles.recipeTags}>
                        {categoryDetails && categoryDetails.name}
                    </p>

                    <h1 className={styles.recipeTitle}>{title}</h1>

                    <p className={styles.recipeMetadata}>
                        {isNaN(rating) ? (
                            <span className={styles.recipeRating}>0.0★</span>
                        )  : (
                            <span className={styles.recipeRating}>{rating}★</span>
                        )}
                    </p>
                    <div className={styles.recipeDescContainer}>
                        <p className={styles.recipeDesc}>{description}</p>
                    </div>

                    

                </div>

                {editable ? (
                    <div style={{
                        display: 'flex',
                        flexDirection: 'row',
                        justifyContent: 'space-between',
                        alignItems: 'center',
                        gap: '10px',
                        width: '100%',
                        marginTop: '1rem'
                    
                    }}>
                        <button className={saved ? styles.recipeSaved : styles.recipeSave} type="but ton" onClick={(e) => handleSave(e)}>
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="#000000"><path d="M 6.0097656 2 C 4.9143111 2 4.0097656 2.9025988 4.0097656 3.9980469 L 4 22 L 12 19 L 20 22 L 20 20.556641 L 20 4 C 20 2.9069372 19.093063 2 18 2 L 6.0097656 2 z M 6.0097656 4 L 18 4 L 18 19.113281 L 12 16.863281 L 6.0019531 19.113281 L 6.0097656 4 z" fill="currentColor"/></svg>
                            Save
                        </button>

                        <button className={styles.recipeSave} type="but ton" onClick={(e) => handleEdit(e)}>
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                            <path d="M18.364 4.05l1.414 1.415-4.95 4.95-1.415-1.415 4.95-4.95zM3 17l6.414-6.414 4.95 4.95L7.95 21H3v-3.95z"/>
                        </svg>

                            Edit
                        </button>
                    </div>
                ) : (
                    <button className={saved ? styles.recipeSaved : styles.recipeSave} type="but ton" onClick={(e) => handleSave(e)}>
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="#000000"><path d="M 6.0097656 2 C 4.9143111 2 4.0097656 2.9025988 4.0097656 3.9980469 L 4 22 L 12 19 L 20 22 L 20 20.556641 L 20 4 C 20 2.9069372 19.093063 2 18 2 L 6.0097656 2 z M 6.0097656 4 L 18 4 L 18 19.113281 L 12 16.863281 L 6.0019531 19.113281 L 6.0097656 4 z" fill="currentColor"/></svg>
                        Save
                    </button>
                )}

                
        </div>
    )
}