'use client'

import {universalApi} from '../../utils/api';
import React, { useState } from 'react';
import styles from '../../styles/Modal/AuthModal.module.css';
import { useRouter } from 'next/router';

export default function AuthModal({ onClose }) {
  const [authMode, setAuthMode] = useState('login');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [email, setEmail] = useState('');
  const [repeatPassword, setRepeatPassword] = useState('');


  const router = useRouter()

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const credentials = {
        username: username,
        password: password
      }
      const response = await universalApi('user/login/', 'POST', credentials)

      console.log(response)

      if(response.message === 'Login successful') {
        console.log("Login successful")
      } else {
        console.log("Login failed")
      }
    } catch (error) {
      console.error(error)
    }
  };

  const handleRegister = async (e) => {
    e.preventDefault();

    try {
      const userData = {
        username: username,
        email: email,
        re_password: repeatPassword,
        password: password
      }

      const response = universalApi('user/register/', 'POST', userData)

      console.log(response)

      if (response.Message === 'User has been created') {
        console.log(response.Message);
      }

    } catch (error) {
      console.error('Error:', error);
    }


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
