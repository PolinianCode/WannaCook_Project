import { useEffect, useState } from 'react';
import { universalApi } from '../../utils/api';
import Cookies from 'js-cookie';

export default function Profile() {

  const [response, setResponse] = useState(false);

  useEffect(() => {
    const getUser = async () => {
      const response = await fetch('http://localhost:8000/api/user/token_check/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Token ${Cookies.get('token')} `,
        },
      });
      if(response.Message === 'Token is valid') {
        setResponse(response.status);
      } else {  
        setResponse(response.status);
      }
    };
    getUser();
  })

  
  return (
    <>
        {response === 200 ? (
            <div>
                <h1>Profile</h1>
            </div>
        ) : (
            <div>
                <h1>Not logged in</h1>
            </div>
        )}
    </>
  );
}
