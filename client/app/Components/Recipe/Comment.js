"use client"
import React from 'react';
import styles from './Styles/Comment.module.css';


const Comment = ({ author, content, createdAt }) => {
    return (
      <div className={styles.comment}>
        <div className={styles.author}>{author}</div>
        <div className={styles.content}>{content}</div>
        <div className={styles.createdAt}>{createdAt}</div>
      </div>
    );
  };
  
  export default Comment;
