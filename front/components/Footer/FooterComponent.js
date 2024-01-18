import React from 'react';
import styles from '../../styles/Footer/Footer.module.css';

const FooterComponent = () => {
    return (
        <footer className={styles.footer}>
            <div className={styles.footerContent}>
                <p>&copy; 2024 WannaCook. All rights reserved.</p>
            </div>
        </footer>
    );
};

export default FooterComponent;
