import React from 'react';
import { Button as MuiButton } from '@mui/material';

const AnimatedButton = ({
  children,
  variant = 'contained',
  gradient,
  glow = false,
  bounce = false,
  sx = {},
  ...props
}) => {
  const getGradient = () => {
    if (gradient) return gradient;
    return 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)';
  };

  return (
    <MuiButton
      variant={variant}
      className={`${bounce ? 'bounce-in' : ''}`}
      sx={{
        position: 'relative',
        overflow: 'hidden',
        borderRadius: '16px',
        padding: '12px 32px',
        fontSize: '1rem',
        fontWeight: 700,
        textTransform: 'none',
        background: variant === 'contained' ? getGradient() : 'transparent',
        border: variant === 'outlined' ? '2px solid' : 'none',
        borderColor: variant === 'outlined' ? '#667eea' : 'transparent',
        color: variant === 'contained' ? 'white' : '#667eea',
        boxShadow: variant === 'contained' ? '0 8px 24px rgba(102, 126, 234, 0.4)' : 'none',
        transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
        '&:hover': {
          background:
            variant === 'contained'
              ? 'linear-gradient(135deg, #5568d3 0%, #6a3f8f 100%)'
              : 'rgba(102, 126, 234, 0.1)',
          transform: 'translateY(-4px) scale(1.02)',
          boxShadow:
            variant === 'contained'
              ? glow
                ? '0 12px 32px rgba(102, 126, 234, 0.6), 0 0 40px rgba(102, 126, 234, 0.4)'
                : '0 12px 32px rgba(102, 126, 234, 0.6)'
              : '0 4px 12px rgba(102, 126, 234, 0.2)',
        },
        '&:active': {
          transform: 'translateY(-2px) scale(0.98)',
        },
        '&::before': {
          content: '""',
          position: 'absolute',
          top: '50%',
          left: '50%',
          width: '0',
          height: '0',
          borderRadius: '50%',
          background: 'rgba(255, 255, 255, 0.3)',
          transform: 'translate(-50%, -50%)',
          transition: 'width 0.6s, height 0.6s',
        },
        '&:active::before': {
          width: '300px',
          height: '300px',
        },
        ...sx,
      }}
      {...props}
    >
      {children}
    </MuiButton>
  );
};

export default AnimatedButton;
