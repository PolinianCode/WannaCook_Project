'use client'
import Cookies from 'js-cookie';

export default function Profile() {

  const user = Cookies.get('user') ? JSON.parse(Cookies.get('user')) : null;

  const ClearCookies = () =>  {
    Cookies.remove('user');
  }

   return (
    <>
            {user ? (
              <div>
                <p>Welcome, {user.nickname}!</p>
                 <button onClick={() => ClearCookies()}>Logout</button>
              </div>    
            ) : (
                <p>Error</p>
            )}
        </>
   )
 }