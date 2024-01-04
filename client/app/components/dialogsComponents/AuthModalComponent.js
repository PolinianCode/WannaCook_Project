// AuthModal.js
import React, { useState } from 'react';
import styles from '@/app/components/dialogsComponents/styles/AuthModal.module.css';

export default function AuthModal({ onClose }) {
  const [authMode, setAuthMode] = useState('login');

  const handleLogin = (e) => {
    e.preventDefault();
    // Add your login logic here
  };

  const handleRegister = (e) => {
    e.preventDefault();
    // Add your registration logic here
  };

  const handleForgotPassword = (e) => {
    e.preventDefault();
    // Add your forgot password logic here
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
            required
          />

          <button type="submit" className={styles.loginBtn}>
            Log In
          </button>
          <div className={styles.tabButtons}>
        <button onClick={() => setAuthMode('register')} className={styles.tabBtn}>
          Register
        </button>
        <button onClick={() => setAuthMode('forgot')} className={styles.tabBtn}>
          Forgot Password
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
            required
          />

          <button type="submit" className={styles.registerBtn}>
            Register
          </button>
          <div className={styles.tabButtons}>
        <button onClick={() => setAuthMode('login')} className={styles.tabBtn}>
          Login
        </button>
      </div>
        </form>
      )}

      {authMode === 'forgot' && (
        <form onSubmit={handleForgotPassword}>
          <label htmlFor="forgotEmail" className={styles.label}>
            Email:
          </label>
          <input
            type="email"
            id="forgotEmail"
            name="forgotEmail"
            className={styles.input}
            required
          />

          <button type="submit" className={styles.forgotBtn}>
            Reset Password
          </button>

          <div className={styles.tabButtons}>
            <button onClick={() => setAuthMode('login')} className={styles.tabBtn}>
            Login
            </button>
            <button onClick={() => setAuthMode('register')} className={styles.tabBtn}>
            Register
            </button>
         </div>
        </form>
      )}
      
    </div>
  );
}
