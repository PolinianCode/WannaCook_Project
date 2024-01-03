import styles from "@/app/components/componentsStyles/Container.module.css"

export default function Container( {children } ) {
    return (
        <div className={styles.container}>
            {children}
        </div>
    )
}