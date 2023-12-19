"use client"


import Image from 'next/image'
import { useState, useEffect } from 'react';
import Comment from './Components/Recipe/Comment';

export default function Home() {

  const [comments, setComments] = useState([]);

  useEffect(() => {
    const fetchComments = async () => {
      try {
        const response = await fetch('http://localhost:8000/api/comment/get/4/'); // Assuming you have an API route at '/api/comments'
        const data = await response.json();

        // Check if 'latest_recipes' is present in the response
        if (data && data.latest_recipes) {
          // Parse the JSON string into an array of comments
          const parsedComments = JSON.parse(data.latest_recipes);

          // Extract only the desired fields from each comment
          const transformedComments = parsedComments.map(comment => ({
            recipe_id: comment.fields.recipe,
            user_id: comment.fields.user,
            comment_text: comment.fields.comment_text,
          }));

          // Update the state with the transformed comments
          setComments(transformedComments);
        }
      } catch (error) {
        console.error('Error fetching comments:', error);
      }
    };

    fetchComments();
  }, []);

  return (
    <div>
        {comments.map((comment, index) => (
          <div key={index}>
            Recipe: {comment.recipe}
          </div>
        ))}
      </div>
  )
}
