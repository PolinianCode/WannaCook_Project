// pages/_app.js
import '../styles/global.css';
import Head from 'next/head';
import { useState, useEffect } from 'react';
import Cookies from 'js-cookie';
import AuthContext from '../contexts/authContext';
import { useRouter } from 'next/router';

function MyApp({ Component, pageProps }) {

  const [authStatus, setAuthStatus] = useState(false);//

  const router = useRouter()

  useEffect(() => {
    const checkToken = async () => {
      const url_excepts = ['/', '/recipe/[id]']

      try {
        const response = await fetch('http://localhost:8000/api/user/token_check/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Token ${Cookies.get('token')} `,
          },
        });

        if (response.status === 200) {
          setAuthStatus(true);
        } else {
          setAuthStatus(false);
          if(!url_excepts.includes(router.pathname)) {
            router.push({
              pathname: '/error',
              query: { code: response.status, message: "You are not logged in to visit this page" },
            });
          }
        }
      } catch (error) {
        console.error('Error checking token:', error);
        
      }
    };

    checkToken();
  }, [router.pathname]);


  return (
    <AuthContext.Provider value={{ authStatus, setAuthStatus }}>
      <Head>
        
        <link
          rel="stylesheet"
          href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap"
        />
      </Head>
     
      <Component {...pageProps} />
    </AuthContext.Provider>
  );
}

export default MyApp;
