import React, { useState } from 'react';
import { Fab, Box, Zoom, Tooltip, SpeedDial, SpeedDialAction, SpeedDialIcon } from '@mui/material';
import {
  Add,
  Chat,
  School,
  Assessment,
  EmojiEvents,
  Settings,
  Close,
} from '@mui/icons-material';

/**
 * Premium Floating Action Button with Speed Dial
 * 
 * Features:
 * - Glassmorphism effect
 * - Smooth animations
 * - Multiple quick actions
 * - Gradient backgrounds
 */
const FloatingActionButton = ({ actions = [], mainAction, position = 'bottom-right' }) => {
  const [open, setOpen] = useState(false);

  const defaultActions = [
    { icon: <Chat />, name: 'AI Tutor', gradient: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)' },
    { icon: <School />, name: 'New Course', gradient: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)' },
    { icon: <Assessment />, name: 'Quiz', gradient: 'linear-gradient(135deg, #fa709a 0%, #fee140 100%)' },
    { icon: <EmojiEvents />, name: 'Achievements', gradient: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' },
  ];

  const actionsList = actions.length > 0 ? actions : defaultActions;

  const positionStyles = {
    'bottom-right': { position: 'fixed', bottom: 24, right: 24 },
    'bottom-left': { position: 'fixed', bottom: 24, left: 24 },
    'top-right': { position: 'fixed', top: 80, right: 24 },
    'top-left': { position: 'fixed', top: 80, left: 24 },
  };

  return (
    <Box
      sx={{
        ...positionStyles[position],
        zIndex: 1000,
      }}
    >
      <SpeedDial
        ariaLabel="Quick Actions"
        icon={
          <SpeedDialIcon
            icon={<Add />}
            openIcon={<Close />}
          />
        }
        onClose={() => setOpen(false)}
        onOpen={() => setOpen(true)}
        open={open}
        direction="up"
        FabProps={{
          sx: {
            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            color: 'white',
            width: 64,
            height: 64,
            boxShadow: '0 8px 32px rgba(102, 126, 234, 0.5)',
            backdropFilter: 'blur(10px)',
            border: '1px solid rgba(255, 255, 255, 0.2)',
            '&:hover': {
              background: 'linear-gradient(135deg, #5568d3 0%, #6a3f8f 100%)',
              boxShadow: '0 12px 48px rgba(102, 126, 234, 0.7)',
              transform: 'scale(1.05) rotate(90deg)',
            },
            transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
          },
        }}
      >
        {actionsList.map((action, index) => (
          <SpeedDialAction
            key={action.name}
            icon={action.icon}
            tooltipTitle={action.name}
            tooltipOpen
            onClick={action.onClick}
            FabProps={{
              sx: {
                background: action.gradient || 'rgba(255, 255, 255, 0.9)',
                backdropFilter: 'blur(10px)',
                border: '1px solid rgba(255, 255, 255, 0.3)',
                color: 'white',
                boxShadow: '0 4px 16px rgba(0, 0, 0, 0.2)',
                '&:hover': {
                  background: action.gradient || 'rgba(255, 255, 255, 1)',
                  boxShadow: '0 8px 24px rgba(0, 0, 0, 0.3)',
                  transform: 'scale(1.1)',
                },
                transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
                animation: `slideIn 0.3s ease-out ${index * 0.05}s both`,
                '@keyframes slideIn': {
                  from: {
                    opacity: 0,
                    transform: 'translateY(20px) scale(0.8)',
                  },
                  to: {
                    opacity: 1,
                    transform: 'translateY(0) scale(1)',
                  },
                },
              },
            }}
          />
        ))}
      </SpeedDial>
    </Box>
  );
};

/**
 * Simple Premium FAB
 */
export const SimpleFAB = ({ icon, onClick, tooltip, gradient, position = 'bottom-right' }) => {
  const positionStyles = {
    'bottom-right': { position: 'fixed', bottom: 24, right: 24 },
    'bottom-left': { position: 'fixed', bottom: 24, left: 24 },
    'top-right': { position: 'fixed', top: 80, right: 24 },
    'top-left': { position: 'fixed', top: 80, left: 24 },
  };

  return (
    <Zoom in={true}>
      <Tooltip title={tooltip} placement="left">
        <Fab
          color="primary"
          onClick={onClick}
          sx={{
            ...positionStyles[position],
            width: 64,
            height: 64,
            background: gradient || 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            backdropFilter: 'blur(10px)',
            border: '1px solid rgba(255, 255, 255, 0.2)',
            boxShadow: '0 8px 32px rgba(102, 126, 234, 0.5)',
            '&:hover': {
              background: gradient || 'linear-gradient(135deg, #5568d3 0%, #6a3f8f 100%)',
              boxShadow: '0 12px 48px rgba(102, 126, 234, 0.7)',
              transform: 'scale(1.1) rotate(15deg)',
            },
            '&:active': {
              transform: 'scale(0.95)',
            },
            transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
            zIndex: 1000,
          }}
        >
          {icon}
        </Fab>
      </Tooltip>
    </Zoom>
  );
};

export default FloatingActionButton;
