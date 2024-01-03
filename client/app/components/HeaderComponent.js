
"use client"

import styles from "@/app/components/componentsStyles/Header.module.css"

import Button from "./elements/ButtonComponent"
import Image from "next/image";
import Search from "./elements/SearchComponent";
import Container from "./elements/ContainerComponent";

export default function Header() {

  return (
      <header className={styles.main}>
          <Container>
            <Search></Search>
          </Container>
      </header>
  );
}