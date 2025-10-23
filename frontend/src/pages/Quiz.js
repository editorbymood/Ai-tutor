import React from 'react';
import { Box, Typography, Paper, Button } from '@mui/material';
import { Quiz as QuizIcon, Construction } from '@mui/icons-material';

const Quiz = () => {
  return (
    <Box className="fade-in">
      {/* Header */}
      <Paper
        sx={{
          p: 4,
          mb: 4,
          borderRadius: '24px',
          background: 'linear-gradient(135deg, #fa709a 0%, #fee140 100%)',
          color: 'white',
        }}
      >
        <Typography variant="h3" sx={{ fontWeight: 800, mb: 1 }}>
          Quiz Center 🎯
        </Typography>
        <Typography variant="h6" sx={{ opacity: 0.9 }}>
          Test your knowledge and track your progress
        </Typography>
      </Paper>

      {/* Coming Soon */}
      <Paper
        sx={{
          p: 8,
          borderRadius: '24px',
          textAlign: 'center',
          background: 'white',
        }}
      >
        <Box
          sx={{
            width: 120,
            height: 120,
            borderRadius: '32px',
            background: 'linear-gradient(135deg, rgba(250, 112, 154, 0.1) 0%, rgba(254, 225, 64, 0.1) 100%)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            mx: 'auto',
            mb: 3,
          }}
        >
          <Construction sx={{ fontSize: 64, color: '#fa709a' }} />
        </Box>
        <Typography variant="h4" sx={{ fontWeight: 700, mb: 2 }}>
          Quiz Functionality Coming Soon! 🚀
        </Typography>
        <Typography variant="body1" color="text.secondary" sx={{ mb: 4, maxWidth: 600, mx: 'auto' }}>
          We're building an amazing quiz experience with adaptive difficulty,
          instant feedback, and personalized learning paths. Stay tuned!
        </Typography>
        <Button
          variant="contained"
          size="large"
          sx={{
            px: 4,
            py: 1.5,
            borderRadius: '12px',
            background: 'linear-gradient(135deg, #fa709a 0%, #fee140 100%)',
            fontWeight: 700,
          }}
        >
          Notify Me When Ready
        </Button>
      </Paper>
    </Box>
  );
};

export default Quiz;