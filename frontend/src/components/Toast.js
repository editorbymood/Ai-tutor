import React from 'react';
import { Snackbar, Alert, Slide } from '@mui/material';

function SlideTransition(props) {
  return <Slide {...props} direction="up" />;
}

const Toast = ({ open, onClose, severity = 'success', message }) => {
  return (
    <Snackbar
      open={open}
      autoHideDuration={4000}
      onClose={onClose}
      anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
      TransitionComponent={SlideTransition}
    >
      <Alert
        onClose={onClose}
        severity={severity}
        variant="filled"
        sx={{
          width: '100%',
          borderRadius: '16px',
          fontWeight: 600,
          fontSize: '1rem',
          boxShadow: '0 8px 32px rgba(0, 0, 0, 0.3)',
          background:
            severity === 'success'
              ? 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)'
              : severity === 'error'
              ? 'linear-gradient(135deg, #f5576c 0%, #d44454 100%)'
              : severity === 'warning'
              ? 'linear-gradient(135deg, #fa709a 0%, #fee140 100%)'
              : 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        }}
      >
        {message}
      </Alert>
    </Snackbar>
  );
};

export default Toast;
