import React from 'react';
import styles from '../../styles/Basic/addRecipeButton.module.css'
import { useRouter } from 'next/router';
import { useContext } from 'react';
import AuthContext from '../../contexts/authContext';

const AddRecipeButtonComponent = () => {

    const { authStatus } = useContext(AuthContext);

    const router = useRouter()

    const handleClick = () => {
        if (authStatus == true) {
            router.push('/recipe/constructor')
        } else {
            router.push({
                pathname: '/error',
                query: { code: 401, message: "You are not logged in to visit this page" },
            })
        }
    }


    return (
        <div
            className={styles.roundPlusContainer}
        >
            <button className={styles.roundPlus} onClick={() => handleClick()}>+</button>
        </div>
    );
};

export default AddRecipeButtonComponent;
