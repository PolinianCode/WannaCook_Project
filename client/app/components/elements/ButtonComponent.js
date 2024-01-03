"use client"

import styles from "@/app/components/componentsStyles/Buttons.module.css"


export default function Button({ type, onClickHandle, children }) {
    const buttonStyle = type === 'yellow' ? styles.acceptBtn : type === 'white' ? styles.declineBtn : type === 'red' ? styles.errorBtn : styles.defaultbtn;

    return (
        <button className={`${buttonStyle} ${styles.defaultbtn}`} onClick={onClickHandle}>
            {children}
        </button>
    );
}