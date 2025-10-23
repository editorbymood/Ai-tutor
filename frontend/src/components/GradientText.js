import React from 'react';
import { Box, Typography } from '@mui/material';

const GradientText = ({ children, gradient, variant = 'h4', sx = {}, ...props }) => {
  const defaultGradient = 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)';

  return (
    <Typography
      variant={variant}
      sx={{
        background: gradient || defaultGradient,
        WebkitBackgroundClip: 'text',
        WebkitTextFillColor: 'transparent',
        backgroundClip: 'text',
        fontWeight: 800,
        ...sx,
      }}
      {...props}
    >
      {children}
    </Typography>
  );
};

export default GradientText;
