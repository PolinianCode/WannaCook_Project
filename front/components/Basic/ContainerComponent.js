import styles from "../../styles/Basic/Container.module.css"

export default function Container( {children } ) {
    return (
        <div className={styles.container}>
            {children}
        </div>
    )
}