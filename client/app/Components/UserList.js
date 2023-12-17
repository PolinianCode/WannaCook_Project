"use client"

import React, { useEffect, useState } from 'react';
import axios from 'axios';

const UserList = () => {
  const [users, setUsers] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get('http://localhost:8000/api/users/');
        const parsedData = JSON.parse(response.data.latest_recipes);
        setUsers(parsedData);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
  }, []);

  return (
    <div>
      <h1>User List</h1>
      <table>
        <thead>
          <tr>
            <th>Nickname</th>
            <th>Email</th>
            <th>Registration Date</th>
            <th>Moderator</th>
          </tr>
        </thead>
        <tbody>
          {users.map((user) => (
            <tr key={user.pk}>
              <td>{user.fields.nickname}</td>
              <td>{user.fields.email}</td>
              <td>{user.fields.registration_date}</td>
              <td>{user.fields.is_moderator ? 'Yes' : 'No'}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default UserList;
