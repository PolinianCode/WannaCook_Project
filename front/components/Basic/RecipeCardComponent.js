import { useRouter } from 'next/router'
import styles from '../../styles/Basic/RecipeCard.module.css'


export default function RecipeCard({ title, description, rating, recipe_id}) {

    const router = useRouter()

    const handleClick = () => {
        router.push({
            pathname: '/recipe',
            query
        })
    }

    return (
        <div className={styles.recipeCard} onClick={(e) => handleClick}>
            <div className={styles.recipeCardContent}>
                <h3 className={styles.recipeTitle}>{title}</h3>
                <p className={styles.recipeDescription}>
                    {description}
                </p>
                <div className={styles.recipeRating}>{rating}</div>
            </div>
        </div>
    )
}