// @ts-ignore
import React, { useState, useEffect, useCallback } from 'react';

interface User {
    name: string;
    email: string;
}

interface UserDataProps {
    userId: string;
}

const UserData: React.FC<UserDataProps> = ({ userId }) => {
    const [user, setUser] = useState<User | null>(null);
    const [seconds, setSeconds] = useState(0);
    const intervalIdRef = React.useRef<NodeJS.Timeout | null>(null);

    const fetchUserData = useCallback(() => {
        fetch(`https://secret.url/user/${userId}`)
            .then(response => response.json())
            .then(data => setUser(data))
            .catch(error => console.error('Error fetching user data:', error));
    }, [userId]);

    useEffect(() => {
        fetchUserData();
        intervalIdRef.current = setInterval(() => {
            setSeconds(prevSeconds => prevSeconds + 1);
        }, 1000);

        return () => {
            if (intervalIdRef.current) {
                clearInterval(intervalIdRef.current);
            }
        };
    }, [fetchUserData]);

    useEffect(() => {
        fetchUserData();
    }, [userId, fetchUserData]);

    return (
        <div>
            <h1>User Data Component</h1>
            {user? (
                <div>
                    <p>Name: {user.name}</p>
                    <p>Email: {user.email}</p>
                </div>
            ) : (
                <p>Loading user data...</p>
            )}
            <p>Timer: {seconds} seconds</p>
        </div>
    );
};

export default UserData;