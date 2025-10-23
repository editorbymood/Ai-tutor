import React from 'react';
import { Box, CircularProgress, Typography, Backdrop } from '@mui/material';
import { AutoAwesome } from '@mui/icons-material';

const LoadingOverlay = ({ open, message = 'Loading...' }) => {
  return (
    <Backdrop
      sx={{
        color: '#fff',
        zIndex: (theme) => theme.zIndex.drawer + 1,
        background: 'rgba(102, 126, 234, 0.8)',
        backdropFilter: 'blur(10px)',
      }}
      open={open}
    >
      <Box
        sx={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          gap: 3,
        }}
      >
        <Box
          sx={{
            position: 'relative',
            width: 100,
            height: 100,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
          }}
        >
          <CircularProgress
            size={100}
            thickness={2}
            sx={{
              color: 'white',
              position: 'absolute',
            }}
          />
          <AutoAwesome
            sx={{
              fontSize: 48,
              color: 'white',
              animation: 'floating 2s ease-in-out infinite',
            }}
          />
        </Box>
        <Typography
          variant="h5"
          sx={{
            fontWeight: 600,
            color: 'white',
            textAlign: 'center',
            animation: 'pulse 1.5s ease-in-out infinite',
          }}
        >
          {message}
        </Typography>
      </Box>
    </Backdrop>
  );
};

export default LoadingOverlay;
