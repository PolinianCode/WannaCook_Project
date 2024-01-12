'use client'
import { useRouter } from "next/router";
import RecipeCard from "../../components/Basic/RecipeCardComponent";
import styles from "../../styles/Basic/Grid4.module.css"
import Layout from "../../components/layout";

export default function SearchResult() {
    const router = useRouter();
    const { data } = router.query;

    


    try {
        const searchData = JSON.parse(decodeURIComponent(data));

        if (!searchData.search_results || searchData.search_results.length === 0) {
            router.push({
                pathname: '/error',
                query: { code: '404', message: 'Try to change search requirements and try again' },
            });
        }

        return (
            <>
                <Layout>
                <div className={styles.grid}>
                            {searchData.search_results.map((result) => (
                                <RecipeCard 
                                    key={result.recipe_id} 
                                    title={result.title} 
                                    description={result.description} 
                                    category={result.category}
                                    rating={(result.rating_sum / result.rating_num).toFixed(1)} 
                                    recipe_id={result.id}
                                />
                            ))}
                    </div>

                </Layout> 
            </>
        );
    } catch (error) {
        console.error('JSON error:', error);
    }
}
