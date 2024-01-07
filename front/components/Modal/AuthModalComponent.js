'use client'

import JSONtoURL from '../../utils/api';
import React, { useState } from 'react';
import styles from '../../styles/Modal/AuthModal.module.css';
import { useRouter } from 'next/router';
import Cookies from 'js-cookie';

export default function AuthModal({ onClose }) {
  const [authMode, setAuthMode] = useState('login');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [email, setEmail] = useState('');
  const [repeatPassword, setRepeatPassword] = useState('');



  const router = useRouter()

  const handleLogin = async (e) => {
    e.preventDefault();
    
    const userData = {
      nickname: username,
      password: password
    };

    try {
      const fullUrl = JSONtoURL(userData, 'user/login/')

      const response = await fetch(fullUrl, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json'
        },
      });


      if (!response.ok) {
        throw new Error('Login failed');
      }

      const responseData = await response.json();
      const user = responseData.user;

      
      Cookies.set('user', JSON.stringify(user), { expires: 7, secure: true });
      router.push('/profile');
      
    } catch (error) {
      console.error('Error:', error);
    }
    

    
  };

  const handleRegister = (e) => {
    e.preventDefault();
    // Add your registration logic here
  };

  return (
    <div className={styles.authModalContent}>
      {authMode === 'login' && (
        <form onSubmit={handleLogin}>
          <label htmlFor="loginUsername" className={styles.label}>
            Username:
          </label>
          <input
            type="text"
            id="loginUsername"
            name="loginUsername"
            className={styles.input}
            onChange={(e) => setUsername(e.target.value)}
            required
          />

          <label htmlFor="loginPassword" className={styles.label}>
            Password:
          </label>
          <input
            type="password"
            id="loginPassword"
            name="loginPassword"
            className={styles.input}
            onChange={(e) => setPassword(e.target.value)}
            required
          />

          <button type="submit" className={styles.loginBtn}>
            Log In
          </button>
          <div className={styles.tabButtons}>
            <button onClick={() => {
              setAuthMode('register')
              setUsername('')
              setPassword('')
            }} className={styles.tabBtn}>
              Register
            </button>
           </div>
        </form>
      )}

      {authMode === 'register' && (
        <form onSubmit={handleRegister}>
          <label htmlFor="registerUsername" className={styles.label}>
            Username:
          </label>
          <input
            type="text"
            id="registerUsername"
            name="registerUsername"
            className={styles.input}
            onChange={(e) => setUsername(e.target.value)}
            required
          />

        <label htmlFor="registerUsername" className={styles.label}>
            Email:
          </label>
          <input
            type="text"
            id="registerEmail"
            name="registerEmail"
            className={styles.input}
            onChange={(e) => setEmail(e.target.value)}
            required
          />

          <label htmlFor="registerPassword" className={styles.label}>
            Password:
          </label>
          <input
            type="password"
            id="registerPassword"
            name="registerPassword"
            className={styles.input}
            onChange={(e) => setPassword(e.target.value)}
            required
          />

            <label htmlFor="registerPassword" className={styles.label}>
            Repeat password
          </label>
          <input
            type="password"
            id="registerRepeatPassword"
            name="registerRepeatPassword"
            className={styles.input}
            onChange={(e) => setRepeatPassword(e.target.value)}
            required
          />

          <button type="submit" className={styles.registerBtn}>
            Register
          </button>
          <div className={styles.tabButtons}>
        <button onClick={() => {
          setAuthMode('login')
          setUsername('')
          setPassword('')
          setRepeatPassword('')
          setEmail('')
        }} className={styles.tabBtn}>
          Login
        </button>
      </div>
        </form>
      )}

      
    </div>
  );
}
