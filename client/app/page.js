"use client"


import Image from 'next/image'
import { useState, useEffect } from 'react';
import Comment from './Components/Recipe/Comment';

export default function Home() {

  const [comments, setComments] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch('http://localhost:8000/api/comment/get/4/');
        const data = await response.json();
        setComments(data.Comments);
      } catch (error) {
        console.error('Error get comment:', error);
      }
    };

    fetchData();
  }, []);


  return (
    <div>
      {comments.map((comment) => (
        <div key={comment.id}>
          <Comment author={comment.user} content={comment.comment_text} createdAt={comment.comment_date} />
        </div>
      ))}
    </div>
  )
}
