
"use client"

import styles from "../../styles/Header/Header.module.css"
import { useRouter } from "next/router";
import { useEffect, useState } from "react";
import Image from "next/Image";
import Container from "../Basic/ContainerComponent";
import Search from "./SearchComponent";
import { useContext } from "react";
import AuthContext from "../../contexts/authContext";
import Cookies from 'js-cookie';
import { universalApi } from "../../utils/api";
import Link from "next/link";

export default function Header( {onOpenModal } ) {

    const router = useRouter()

    const handleClick = (e, path) => {
        e.preventDefault()
        router.push('/')
    }

    const { authStatus } = useContext(AuthContext);
    const [userData, setUserData] = useState(null);


    async function handleLogout() {
        try {
          const response = await fetch('http://localhost:8000/api/user/logout/', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Token ${Cookies.get('token')} `,
            },
          });
      
          if (response.status === 200) {
            console.log('Logout successful');
            Cookies.remove('token')
            router.reload()
          } else {
            console.log('Error logging out:', response.statusText);
          }
        } catch (error) {
          console.error('Error:', error);
        }
    }


    useEffect(() => {
        if(authStatus == true) {
            const getUserData = async () => {
                try {
                    const response = await universalApi('user/user_data/', 'GET')
                    setUserData(response)
                } catch (error) {
                    console.error(error)
                }
            }
            getUserData()
        } else {
            setUserData(null)
        }
    }, [authStatus]);

  return (
    
      <header className={styles.main}>
          <Container>
            <Image 
                src="/logo.png"
                width={70}
                height={60}
                alt="Wanna Cook Logo"
                priority={false}
                onClick={(e) => handleClick(e, "/")}
                className={styles.Logo}
                />
                <Search></Search>
                {authStatus ? (
                    <>
                        {userData && (
                            <div
                                style={{
                                    display: "flex",
                                    flexDirection: "row",
                                    alignItems: "center",
                                    gap: "10px",
                                }}
                            >
                                <Link href={`/profile/`}>{userData.username}</Link>
                                <button onClick={handleLogout} className={styles.loginBtn}>
                                    <svg
                                        width="15"
                                        height="18"
                                        viewBox="0 0 15 18"
                                        fill="none"
                                        xmlns="http://www.w3.org/2000/svg"
                                        style={{ marginLeft: "0px", marginRight: "2px" }}
                                    >
                                        <path
                                        d="M.946 9.513H10l-2.585 2.584a.512.512 0 1 0 .725.725l3.46-3.459.008-.01a.524.524 0 0 0 .056-.068c.01-.015.017-.03.025-.046.007-.014.016-.028.022-.042l.018-.057.011-.04a.523.523 0 0 0 .01-.1v-.005a.52.52 0 0 0-.01-.095c-.003-.017-.01-.033-.015-.05-.004-.015-.008-.03-.014-.045-.008-.021-.02-.04-.03-.06-.006-.009-.01-.019-.017-.028a.53.53 0 0 0-.065-.08L8.142 5.177a.511.511 0 0 0-.726 0c-.2.2-.2.525 0 .725L10 8.487H.946a.513.513 0 1 0 0 1.026ZM4.71 5.717c.284 0 .513-.23.513-.513V1.539c0-.283.23-.513.513-.513h7.724c.283 0 .513.23.513.513V16.46c0 .283-.23.513-.513.513H5.737a.513.513 0 0 1-.513-.513v-3.528a.513.513 0 1 0-1.026 0v3.528c0 .849.69 1.539 1.54 1.539h7.723A1.54 1.54 0 0 0 15 16.461V1.54A1.54 1.54 0 0 0 13.461 0H5.737a1.54 1.54 0 0 0-1.539 1.539v3.665c0 .283.23.513.513.513Z"
                                        fill="#241F20"
                                        ></path>
                                    </svg>
                                </button>
                            </div>
                            
                        )}
                        
                    </>
                ) : (
                    <button onClick={onOpenModal} className={styles.loginBtn}>
                    Log In
                    <svg width="15" height="18" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path
                        d="M.946 9.513H10l-2.585 2.584a.512.512 0 1 0 .725.725l3.46-3.459.008-.01a.524.524 0 0 0 .056-.068c.01-.015.017-.03.025-.046.007-.014.016-.028.022-.042l.018-.057.011-.04a.523.523 0 0 0 .01-.1v-.005a.52.52 0 0 0-.01-.095c-.003-.017-.01-.033-.015-.05-.004-.015-.008-.03-.014-.045-.008-.021-.02-.04-.03-.06-.006-.009-.01-.019-.017-.028a.53.53 0 0 0-.065-.08L8.142 5.177a.511.511 0 0 0-.726 0c-.2.2-.2.525 0 .725L10 8.487H.946a.513.513 0 1 0 0 1.026ZM4.71 5.717c.284 0 .513-.23.513-.513V1.539c0-.283.23-.513.513-.513h7.724c.283 0 .513.23.513.513V16.46c0 .283-.23.513-.513.513H5.737a.513.513 0 0 1-.513-.513v-3.528a.513.513 0 1 0-1.026 0v3.528c0 .849.69 1.539 1.54 1.539h7.723A1.54 1.54 0 0 0 15 16.461V1.54A1.54 1.54 0 0 0 13.461 0H5.737a1.54 1.54 0 0 0-1.539 1.539v3.665c0 .283.23.513.513.513Z"
                        fill="#241F20"
                        ></path>
                    </svg>
                    </button>
                )}
          </Container>

      </header>
  );
}