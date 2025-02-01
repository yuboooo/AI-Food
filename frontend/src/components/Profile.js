import React from 'react';
import './Profile.css'; // You'll need to create this CSS file

const Profile = ({ user }) => {
  // Default user data if no props provided
  const defaultUser = {
    name: 'John Doe',
    email: 'john@example.com',
    avatar: 'https://via.placeholder.com/150',
    bio: 'Software Developer',
  };

  const profileUser = user || defaultUser;

  return (
    <div className="profile-container">
      <div className="profile-card">
        <img 
          src={profileUser.avatar} 
          alt="Profile" 
          className="profile-avatar"
        />
        <h2 className="profile-name">{profileUser.name}</h2>
        <p className="profile-email">{profileUser.email}</p>
        <p className="profile-bio">{profileUser.bio}</p>
      </div>
    </div>
  );
};

export default Profile;
