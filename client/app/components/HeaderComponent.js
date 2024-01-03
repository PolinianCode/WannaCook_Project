
"use client"

import styles from "@/app/components/componentsStyles/Header.module.css"

import Button from "./elements/ButtonComponent"
import Search from "./elements/SearchComponent";

export default function Header() {
  const handleSubmit = () => {
      console.log("Submit Button");
  };

  const handleCancel = () => {
    console.log("Cancel Button");
  };

  const handleExit = () => {
    console.log("Exit Button");
  };

  return (
      <header className={styles.main}>
          <Search></Search>
      </header>
  );
}