
import { useState, useEffect } from 'react';
import { useRouter } from 'next/router';

import styles from "@/app/components/componentsStyles/Search.module.css"

export default function Search () {

    const [searchTerm, setSearchTerm] = useState('')
    const [showAdditionalBlock, setShowAdditionalBlock] = useState(false)
    const [categories, setCategories] = useState([])
    const [selectedCategory, setSelectedCategory] = useState(null)
    const [ingredients, setIngredients] = useState([])
    const [selectedIngredients, setSelectedIngredient] = useState([])

    //Get ingredient from API 
    useEffect(() => {
        fetch('http://localhost:8000/api/ingredients/all/')
        .then(response => response.json())
        .then(data => setIngredients(data.Ingredients || []))
        .catch(error => console.error('Error getting ingredients:', error));
  }, []);

  //Get Categories from API 
  useEffect(() => {
    fetch('http://localhost:8000/api/category/all/')
    .then(response => response.json())
    .then(data => setCategories(data.Categories || []))
    .catch(error => console.error('Error getting categories:', error));
}, []);

    const handleCategory = (category) => {
        const isSelectedCategory = selectedCategory === category

        if (isSelectedCategory) {
            setSelectedCategory('')
          } else {
            setSelectedCategory(category)
          }
    }

    const handleIngredient = (ingredient) => {
        const isSelectedIngredient = selectedIngredients.some(selected => selected.id === ingredient.id)

        if (isSelectedIngredient) {
            setSelectedIngredient(prevSelected => prevSelected.filter(selected => selected.id !== ingredient.id));
          } else {
            setSelectedIngredient(prevSelected => [...prevSelected, ingredient]);
          }

    }

    const handleChange = (e) => {
        setSearchTerm(e.target.value);
    };

    const handleSubmit = (e) => {

        e.preventDefault()

        const request_json = {}

        if(searchTerm != "") request_json.title = searchTerm
        if(selectedCategory != null) request_json.category = selectedCategory.id
        if (selectedIngredients.length > 0) {
            request_json.ingredients = selectedIngredients.map(ingredient => ingredient.id);
        }


        console.log(JSON.stringify(request_json))


        const url = 'http://localhost:8000/api/recipes/search/';

        const jsonString = encodeURIComponent(JSON.stringify(request_json));
        const fullUrl = `${url}?data=${jsonString}`;


        fetch(fullUrl, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
        })
        .catch(error => {
            console.error('Error:', error);
        });

    }

    const handleFocus = () => {
        setShowAdditionalBlock(true);
    }


    return (
        <div>
            <form onSubmit={handleSubmit}>
                <input type="text" 
                    placeholder="Recipes, categories, intgredients" 
                    name="search-bar"
                    className={styles.main} 
                    onChange={handleChange}
                    onFocus={handleFocus}
                />
                <button type="submit">Search</button>  
            </form>

            {showAdditionalBlock && (
                <div className={styles.searchFilter}>
                    <h3>Search filters</h3>
                    <span>Categories</span>
                    <div className={styles.categoriesBlock}>
                        {categories.map(category => (
                            <div key={category.id}
                                onClick={() => handleCategory(category)}
                                className={styles.filterElement}
                                style = {{
                                    backgroundColor: selectedCategory === category ? 'black' : 'lightgray',
                                    color: selectedCategory === category ? 'white' : 'black'
                                }}
                            >
                            {category.name}
                            </div>
                        ))}
                    </div>

                    <span>Ingredients</span>
                    <div className={styles.categoriesBlock}>
                        {ingredients.map(ingredient => (
                            <div key={ingredient.id}
                                onClick={() => handleIngredient(ingredient)}
                                className={styles.filterElement}
                                style={{
                                    backgroundColor: selectedIngredients.some(selected => selected.id === ingredient.id) ? 'black' : 'lightgray',
                                    color: selectedIngredients.some(selected => selected.id === ingredient.id) ? 'white' : 'black',
                                  }}
                            >
                            {ingredient.name}
                            </div>
                        ))}
                    </div>
                </div>
            )}

        </div>
    )
}