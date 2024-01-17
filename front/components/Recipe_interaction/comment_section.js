'use client'

import { useRouter } from 'next/router'
import { universalApi } from '../../utils/api'
import { useContext } from 'react';

import { useEffect, useState } from 'react';
import styles from '../../styles/RecipePage/Comments.module.css';
import AuthContext from '../../contexts/authContext';
import Cookies from 'js-cookie';

const CommentsSection = ({recipe_id}) => {

  const [comments, setComments] = useState([]);
  const [newComment, setNewComment] = useState('');
  const [userDataHook, setUserData] = useState(null);
  const [editedComment, setEditedComment] = useState({ id: null, text: '' });

  const { authStatus } = useContext(AuthContext);


  const router = useRouter();

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

        const userData = await universalApi('user/user_data/', 'GET', { token: Cookies.get('token') });
        
        setComments(commentsWithUserData);
        setUserData(userData);
  
      } catch (error) {
        console.error('Error getting comments:', error);
      }
    };
  
    fetchComments();
  }, [recipe_id, userDataHook?.id]);




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
    user: userData.id,
  };

  const responseComment = await universalApi(`comments/`, 'POST', comment);

  setComments((prevComments) => [ { ...responseComment, username: userData.username }, ...prevComments ]);
  setNewComment('');
};

const handleDeleteComment = async (commentId) => {
  try {
    await universalApi(`comments/${commentId}/`, 'DELETE');
    setComments((prevComments) => prevComments.filter((comment) => comment.id !== commentId));
  } catch (error) {
    console.error('Error deleting comment:', error);
  };
}

const handleEditComment = async (commentId, commentText) => {
  setEditedComment({ id: commentId, text: commentText });
}


const handleSaveEdit = async () => {
  try {
    const comment = {
      comment_text: editedComment.text,
    };

    const responseComment = await universalApi(`comments/${editedComment.id}/`, 'PATCH', comment);
    setComments((prevComments) =>
      prevComments.map((comment) =>
        comment.id === editedComment.id ? { ...comment, comment_text: responseComment.comment_text } : comment
      )
    );
    setEditedComment({ id: null, text: '' });
  } catch (error) {
    console.error('Error saving edited comment:', error);
  }
};

const handleCancelEdit = () => {
  setEditedComment({ id: null, text: '' });
};

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
        <button type="submit">Add Comment</button>
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
            {editedComment.id === comment.id ? (
              <div>
                <textarea
                  value={editedComment.text}
                  onChange={(e) => setEditedComment({ ...editedComment, text: e.target.value })}
                  rows={3}
                  className={styles.editTextArea}
                />
                <div className={styles.commentActionBtn}>
                  <button onClick={handleSaveEdit}>Save</button>
                  <button onClick={handleCancelEdit}>Cancel</button>
                </div>
                
              </div>
            ) : (
              <div>
                <p className={styles.text}>{comment.comment_text}</p>
                {userDataHook && comment.user === userDataHook.id && (
                  <div className={styles.commentActionBtn}>
                    <button onClick={() => handleEditComment(comment.id, comment.comment_text)}>Edit</button>
                    <button onClick={() => handleDeleteComment(comment.id)}>Delete</button>
                  </div>
                )}
              </div>
            )}
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