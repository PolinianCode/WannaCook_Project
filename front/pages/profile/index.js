import { useEffect, useState } from 'react';
import { universalApi } from '../../utils/api';
import Cookies from 'js-cookie';
import { useRouter } from 'next/router';
import Layout from '../../components/layout';

export default function Profile() {

  const router = useRouter()

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

      console.log(response);
      if(response.status === 200) {
        setResponse(response.status);
      } else {  
        setResponse(response.status);
        router.push({
          pathname: '/error',
          query: { code: response.status, message: "You are not logged in to visit this page" },
        });
      }
    };
    getUser();
  }, [router])

  
  return (
    <Layout>
      {response === 200 ? (
            <div>
                <h1>Profile</h1>
            </div>
        ) : (
            <div>
                <h1>Not logged in</h1>
            </div>
        )}
    </Layout>
  );
}
