import React from 'react';
import { useSelector } from 'react-redux';
import { Box, Typography, Paper, Avatar, Chip } from '@mui/material';

const Profile = () => {
  const { user } = useSelector((state) => state.auth);

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Profile
      </Typography>
      <Paper sx={{ p: 4 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
          <Avatar
            src={user?.avatar}
            sx={{ width: 100, height: 100, mr: 3 }}
          />
          <Box>
            <Typography variant="h5">{user?.full_name}</Typography>
            <Typography variant="body1" color="text.secondary">
              {user?.email}
            </Typography>
            <Chip label={user?.role} sx={{ mt: 1 }} />
          </Box>
        </Box>

        <Typography variant="h6" gutterBottom>
          Learning Information
        </Typography>
        <Typography variant="body1" paragraph>
          Learning Style: {user?.learning_style}
        </Typography>
        {user?.grade_level && (
          <Typography variant="body1" paragraph>
            Grade Level: {user?.grade_level}
          </Typography>
        )}
      </Paper>
    </Box>
  );
};

export default Profile;