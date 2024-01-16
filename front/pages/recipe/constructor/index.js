"use client"
import Layout from "../../../components/layout"
import React, { useState, useEffect } from 'react';
import styles from '../../../styles/RecipePage/RecipeConstructor.module.css'
import { universalApi } from '../../../utils/api';
import Cookies from "js-cookie";
import Head from 'next/head';
import { useRouter } from "next/router";

export default function RecipeConstructor() {

    const [recipe, setRecipe] = useState({
        title: '',
        description: '',
        category: '',
        ingredients: [{ ingredient: '', quantity: '', unit: '' }],
        instructions: '',
      });

    const [categories, setCategories] = useState([])
    const [ingredients, setIngredients] = useState([{}])

    const router = useRouter();

    //Get categories from API
    useEffect(() => {
        async function fetchCategories() {
           try {
               const response = await universalApi('categories/', 'GET');
               setCategories(response)

               if (response.length > 0) {
                setRecipe((prevRecipe) => ({ ...prevRecipe, category: response[0].id }));
              }
           } catch (error) {
               console.error('Error getting categories:', error);
           }
        }

        fetchCategories()
    }, []);


    //Get ingredients from API  
    useEffect(() => {
        async function fetchIngredients() {
           try {
               const response = await universalApi('ingredients/', 'GET');
               setIngredients(response)

               
           } catch (error) {
               console.error('Error getting ingredients:', error);
           }
        }

        fetchIngredients()
    }, []);

    const handleInputChange = (field, value) => {
        setRecipe((prevRecipe) => ({ ...prevRecipe, [field]: value }));
    }

    const handleIngredientChange = (index, field, value) => {
        const updatedIngredients = [...recipe.ingredients];
        updatedIngredients[index] = { ...updatedIngredients[index], [field]: value };
        setRecipe((prevRecipe) => ({ ...prevRecipe, ingredients: updatedIngredients }));
    };
    
    const handleAddIngredient = () => {
    setRecipe((prevRecipe) => ({ ...prevRecipe, ingredients: [...prevRecipe.ingredients, { ingredient: ingredients[0].id, quantity: '', unit: '' }] }));
    };
    
    const handleRemoveIngredient = (index) => {
    const updatedIngredients = [...recipe.ingredients];
    updatedIngredients.splice(index, 1);
    setRecipe((prevRecipe) => ({ ...prevRecipe, ingredients: updatedIngredients }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        const userData = await universalApi('user/user_data/', 'GET', { token: Cookies.get('token') });

        const sendData = {
            title: recipe.title,
            description: recipe.description,
            category: parseInt(recipe.category),
            instruction: recipe.instructions,
            rating_num: 0,
            rating_sum: 0,
            user: userData.id,
        };

        console.log(sendData);

        try {
            const recipeResponse = await universalApi('recipes/', 'POST', sendData);

            for (const ingredient of recipe.ingredients) {
                try {
                    const ingredientData = {
                        ingredient: parseInt(ingredient.ingredient),
                        quantity: ingredient.quantity,
                        unit: ingredient.unit,
                        recipe: recipeResponse.id,
                    };
                    

                    const ingredientResponse = await universalApi('recipeIngredients/', 'POST', ingredientData);
                    console.log(ingredientResponse);

                } catch (error) {
                    console.error('Error creating ingredient:', error);
                }
            }

            router.push(`/recipe/${recipeResponse.id}`);

            console.log(recipeResponse);
        } catch (error) {
            console.error('Error creating recipe:', error);
        }
    }

    return (
        <Layout>
            <Head>
                <title>Adding recipe</title>
            </Head>
            <form className={styles.formContainer}>
                <label>
                    Category
                    <select value={recipe.category} onChange={(e) => handleInputChange('category', e.target.value)}>
                        {categories.map((category) => (
                            <option key={category.id} value={category.id}>
                                {category.name}
                            </option>
                        ))}
                    </select>
                </label>
                <label>
                    Title
                    <input type="text" value={recipe.title} onChange={(e) => handleInputChange('title', e.target.value)} />
                </label>
                <label>
                    Ingredients
                    {recipe.ingredients.map((ingredient, index) => (
                        <div key={index} className={styles.ingredientsInputs}>
                        <select value={ingredient.ingredient} onChange={(e) => handleIngredientChange(index, 'ingredient', e.target.value)}>
                            {ingredients.map((ingredientOption) => (
                            <option key={ingredientOption.id} value={ingredientOption.id}>
                                {ingredientOption.name}
                            </option>
                            ))}
                        </select>
                        <input type="text" placeholder="Quantity" value={ingredient.quantity} onChange={(e) => handleIngredientChange(index, 'quantity', e.target.value)} />
                        <input type="text" placeholder="Unit" value={ingredient.unit} onChange={(e) => handleIngredientChange(index, 'unit', e.target.value)} />
                        <button type="button" className={styles.ingredientRemoveButton} onClick={() => handleRemoveIngredient(index)}>
                            Remove
                        </button>
                        </div>
                    ))}
                    <button type="button" className={styles.ingredientAddButton} onClick={handleAddIngredient}>
                        Add Ingredient
                    </button>
                </label>
                <label>
                    Description
                    <input type="text" value={recipe.description} onChange={(e) => handleInputChange('description', e.target.value)} />
                </label>
                <label>
                    Instruction
                    <textarea value={recipe.instructions} onChange={(e) =>  handleInputChange('instructions', e.target.value)} style={{height: "150px"}}>

                    </textarea>
                </label>
                <div className={styles.actionButtons}>
                    <button type="submit" className={styles.ingredientAddButton} onClick={(e) => handleSubmit(e)}>Submit</button>
                    <button type="submit" className={styles.cancelBtn}>Cancel</button>
                </div>
            </form>
        </Layout>
    )
}
