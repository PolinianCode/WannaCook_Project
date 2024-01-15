'use client'

import { useRouter } from 'next/router'
import { universalApi } from '../../utils/api'

import { useEffect, useState } from 'react';
import styles from '../../styles/RecipePage/Comments.module.css';

const handleCommentSubmit = (e) => {
    e.preventDefault();

    // Add the new comment to the comments array
    setComments([...comments, newComment]);

    // Clear the input field
    setNewComment('');
  };

const CommentsSection = ({recipe_id}) => {

  const [comments, setComments] = useState([]);
  const [newComment, setNewComment] = useState('');

  useEffect(() => {
    const fetchComments = async () => {
        try {
            const response = await universalApi(`comments/?recipe_id=${recipe_id}`, 'GET');
            setComments(response);

        } catch (error) {
            console.error('Error getting category details:', error);
        }
    };

    fetchComments();
}, [recipe_id]);

  // Function to handle submission of a new comment


  return (
    <div className={styles.commentsContainer}>
      <h2>Comments</h2>
      {comments.length > 0 ? (
        <ul className={styles.list}>
          {comments.map((comment) => (
            <li key={comment.id} className={styles.commentBlock}>
              <p className={styles.date}>{comment.comment_date}</p>
              <p className={styles.text}>{comment.comment_text}</p>
            </li>
          ))}
        </ul>
      ) : (
        <p>No comments yet.</p>
      )}
    </div>
  );
};


export default CommentsSection;
