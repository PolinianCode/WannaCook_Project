
import { useState, useEffect, useRef  } from 'react';
import { useRouter } from 'next/router';

import styles from "@/app/components/componentsStyles/Search.module.css"

export default function Search () {

    const [searchTerm, setSearchTerm] = useState('')
    const [showAdditionalBlock, setShowAdditionalBlock] = useState(false)
    const [categories, setCategories] = useState([])
    const [selectedCategory, setSelectedCategory] = useState(null)
    const [ingredients, setIngredients] = useState([])
    const [selectedIngredients, setSelectedIngredient] = useState([])

    const searchFilterRef = useRef(null);

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

    //Close additional div with filters
    useEffect(() => {
        const handleOutsideClick = (event) => {
            if (searchFilterRef.current && !searchFilterRef.current.contains(event.target)) {
                setShowAdditionalBlock(false);
            }
        };

        document.addEventListener('click', handleOutsideClick);

        return () => {
            document.removeEventListener('click', handleOutsideClick);
        };
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
        <div ref={searchFilterRef}>
            <form onSubmit={handleSubmit} autoComplete="off">
                <input type="text" 
                    placeholder="Recipes, categories, intgredients" 
                    name="search-bar"
                    className={styles.searchField} 
                    onChange={handleChange}
                    onFocus={handleFocus}
                    style = {{width: 400, backgroundColor: '#f7f7f7', borderColor: '#e0dede'}}
                />
                <button type="submit" className={styles.searchBtn}><svg width="16" height="10" fill="none" viewBox="0 0 25 25" xmlns="http://www.w3.org/2000/svg" class="searchInput_searchSvg__FzrRz"><path d="M10.04 2.5a7.539 7.539 0 1 1 0 15.079 7.539 7.539 0 0 1 0-15.078ZM15.725 15.724 22 22" stroke="#241F20" stroke-miterlimit="10" stroke-linecap="round" stroke-linejoin="round"></path></svg></button>  
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