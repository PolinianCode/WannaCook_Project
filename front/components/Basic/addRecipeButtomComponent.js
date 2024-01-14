import React from 'react';
import styles from '../../styles/Basic/addRecipeButton.module.css'

const AddRecipeButtonComponent = () => {
    return (
        <div
            className={styles.roundPlusContainer}
        >
            <button className={styles.roundPlus}>+</button>
        </div>
    );
};

export default AddRecipeButtonComponent;
