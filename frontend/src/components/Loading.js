import React from 'react';
import { Box, Typography, keyframes } from '@mui/material';
import { AutoAwesome } from '@mui/icons-material';

const pulse = keyframes`
  0%, 100% {
    transform: scale(1);
    opacity: 1;
  }
  50% {
    transform: scale(1.1);
    opacity: 0.8;
  }
`;

const float = keyframes`
  0%, 100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-20px);
  }
`;

const rotate = keyframes`
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
`;

const shimmer = keyframes`
  0% {
    background-position: -1000px 0;
  }
  100% {
    background-position: 1000px 0;
  }
`;

/**
 * Premium Loading component with glassmorphism and animations
 */
const Loading = ({ message = 'Loading...', fullScreen = false }) => {
  const containerSx = fullScreen ? {
    minHeight: '100vh',
  } : {
    minHeight: '60vh',
  };

  return (
    <Box
      sx={{
        ...containerSx,
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        gap: 3,
      }}
    >
      {/* Animated Icon Container */}
      <Box
        sx={{
          position: 'relative',
          width: 120,
          height: 120,
        }}
      >
        {/* Outer Rotating Ring */}
        <Box
          sx={{
            position: 'absolute',
            inset: 0,
            borderRadius: '50%',
            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            opacity: 0.2,
            animation: `${rotate} 3s linear infinite`,
          }}
        />
        
        {/* Middle Ring */}
        <Box
          sx={{
            position: 'absolute',
            inset: 10,
            borderRadius: '50%',
            background: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
            opacity: 0.3,
            animation: `${rotate} 2s linear infinite reverse`,
          }}
        />
        
        {/* Inner Circle with Icon */}
        <Box
          sx={{
            position: 'absolute',
            inset: 20,
            borderRadius: '50%',
            background: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            animation: `${pulse} 2s ease-in-out infinite`,
            boxShadow: '0 8px 32px rgba(102, 126, 234, 0.5)',
          }}
        >
          <AutoAwesome
            sx={{
              fontSize: 40,
              color: 'white',
              animation: `${float} 3s ease-in-out infinite`,
            }}
          />
        </Box>
      </Box>

      {/* Loading Text with Shimmer Effect */}
      <Box sx={{ textAlign: 'center' }}>
        <Typography
          variant="h5"
          sx={{
            fontFamily: 'Poppins',
            fontWeight: 700,
            background: 'linear-gradient(90deg, #667eea 0%, #764ba2 50%, #667eea 100%)',
            backgroundSize: '200% auto',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
            animation: `${shimmer} 2s linear infinite`,
            mb: 1,
          }}
        >
          {message}
        </Typography>
        
        {/* Animated Dots */}
        <Box sx={{ display: 'flex', gap: 1, justifyContent: 'center' }}>
          {[0, 1, 2].map((i) => (
            <Box
              key={i}
              sx={{
                width: 8,
                height: 8,
                borderRadius: '50%',
                background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                animation: `${pulse} 1.5s ease-in-out infinite`,
                animationDelay: `${i * 0.2}s`,
              }}
            />
          ))}
        </Box>
      </Box>

      {/* Progress Bar */}
      <Box
        sx={{
          width: '200px',
          height: '4px',
          borderRadius: '2px',
          background: 'rgba(102, 126, 234, 0.2)',
          overflow: 'hidden',
          position: 'relative',
        }}
      >
        <Box
          sx={{
            position: 'absolute',
            top: 0,
            left: 0,
            height: '100%',
            width: '50%',
            background: 'linear-gradient(90deg, #667eea 0%, #764ba2 100%)',
            animation: `${shimmer} 1.5s ease-in-out infinite`,
            backgroundSize: '200% 100%',
          }}
        />
      </Box>
    </Box>
  );
};

export default Loading;
