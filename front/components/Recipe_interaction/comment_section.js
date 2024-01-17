'use client'

import { useRouter } from 'next/router'
import { universalApi } from '../../utils/api'
import { useContext } from 'react';

import { useEffect, useState } from 'react';
import styles from '../../styles/RecipePage/Comments.module.css';
import AuthContext from '../../contexts/authContext';

const CommentsSection = ({recipe_id}) => {

  const [comments, setComments] = useState([]);
  const [newComment, setNewComment] = useState('');

  const { authStatus } = useContext(AuthContext);

  useEffect(() => {
    const fetchComments = async () => {
      try {
        const commentsResponse = await universalApi(`comments/?recipe_id=${recipe_id}`, 'GET');
        const commentsWithUserData = await Promise.all(
          commentsResponse.map(async (comment) => {
            const userData = await universalApi(`user/get_user_by_id/${comment.user}/`, 'GET');
            return { ...comment, username: userData.username };
          })
        );
  
        setComments(commentsWithUserData);
  
      } catch (error) {
        console.error('Error getting comments:', error);
      }
    };
  
    fetchComments();
  }, [recipe_id]);

const formateDate = (date) => {
  const originalDateString = date;
  const dateObject = new Date(originalDateString);

  const formattedDate = new Intl.DateTimeFormat("en-GB", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
    hour: "numeric",
    minute: "numeric",
    hour12: false,
    timeZone: "UTC",
  }).format(dateObject);

  return formattedDate
}


const handleCommentSubmit = async (e) => {
  e.preventDefault();

  const userData = await universalApi('user/user_data/', 'GET', { token: Cookies.get('token') });


  const comment = {
    comment_text: newComment,
    recipe: recipe_id,
    user: 29,
  }

  const responseComment = await universalApi(`comments/`, 'POST', comment);

  setComments((prevComments) => [...prevComments, responseComment]);
  setNewComment('');
}


  return (
    <div className={styles.commentsContainer}>
      <h2>Comments</h2>
      {authStatus ? (
        <form className={styles.commentForm} onSubmit={handleCommentSubmit}>
        <textarea
          value={newComment}
          onChange={(e) => setNewComment(e.target.value)}
          placeholder="Add a comment..."
          rows={3}
        />
        <button type="submit">
          Add Comment
        </button>
      </form>
      ) : (
        <p>Log in to add comments.</p>
      )}
      

      {comments.length > 0 ? (
        <ul className={styles.list}>
          {comments.map((comment) => (
            <li key={comment.id} className={styles.commentBlock}>
              <p className={styles.date}>{formateDate(comment.comment_date)}</p>
              <p className={styles.userName}>{comment.username}</p>
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
