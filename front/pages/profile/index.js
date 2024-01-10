import { useEffect, useState } from 'react';
import { universalApi } from '../../utils/api';

export default function Profile() {
  
  return (
    <>
      {user ? (
        <div>
          <p>Welcome, {user.nickname}!</p>
          <button>Logout</button>
        </div>
      ) : (
        <p>Error</p>
      )}
    </>
  );
}
