import React from 'react';
import { Card, CardContent, CardActions, Box, Typography, IconButton, Chip } from '@mui/material';
import { MoreVert, Favorite, Share, TrendingUp } from '@mui/icons-material';

/**
 * Premium Card Component with Glassmorphism and Hover Effects
 * 
 * @param {Object} props
 * @param {string} props.title - Card title
 * @param {string} props.subtitle - Card subtitle
 * @param {string} props.description - Card description
 * @param {string} props.gradient - Custom gradient for the card
 * @param {React.ReactNode} props.icon - Icon to display
 * @param {Array} props.tags - Tags to display as chips
 * @param {Function} props.onClick - Click handler
 * @param {React.ReactNode} props.children - Custom content
 */
const PremiumCard = ({
  title,
  subtitle,
  description,
  gradient = 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
  icon,
  tags = [],
  onClick,
  children,
  ...props
}) => {
  return (
    <Card
      onClick={onClick}
      className="glass hover-lift scale-in"
      sx={{
        borderRadius: '20px',
        overflow: 'visible',
        position: 'relative',
        cursor: onClick ? 'pointer' : 'default',
        transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
        '&:hover': {
          transform: onClick ? 'translateY(-8px) scale(1.02)' : 'translateY(-8px)',
          boxShadow: '0 20px 60px rgba(102, 126, 234, 0.3)',
        },
        '&::before': {
          content: '""',
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          height: '5px',
          background: gradient,
          borderRadius: '20px 20px 0 0',
        },
        ...props.sx,
      }}
      {...props}
    >
      {/* Floating Icon Badge */}
      {icon && (
        <Box
          sx={{
            position: 'absolute',
            top: -20,
            right: 24,
            width: 60,
            height: 60,
            borderRadius: '16px',
            background: gradient,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            boxShadow: '0 8px 24px rgba(102, 126, 234, 0.4)',
            color: 'white',
            fontSize: 28,
            zIndex: 1,
            transform: 'rotate(-10deg)',
            transition: 'transform 0.3s ease',
            '&:hover': {
              transform: 'rotate(0deg) scale(1.1)',
            },
          }}
        >
          {icon}
        </Box>
      )}

      <CardContent sx={{ pt: icon ? 4 : 3, pb: 2 }}>
        {/* Header Section */}
        <Box sx={{ mb: 2 }}>
          {subtitle && (
            <Typography
              variant="caption"
              sx={{
                color: 'text.secondary',
                fontWeight: 600,
                textTransform: 'uppercase',
                letterSpacing: '0.1em',
                mb: 0.5,
                display: 'block',
              }}
            >
              {subtitle}
            </Typography>
          )}
          
          {title && (
            <Typography
              variant="h5"
              sx={{
                fontFamily: 'Poppins',
                fontWeight: 700,
                background: gradient,
                WebkitBackgroundClip: 'text',
                WebkitTextFillColor: 'transparent',
                mb: 1,
              }}
            >
              {title}
            </Typography>
          )}

          {description && (
            <Typography
              variant="body2"
              color="text.secondary"
              sx={{ lineHeight: 1.7 }}
            >
              {description}
            </Typography>
          )}
        </Box>

        {/* Tags */}
        {tags.length > 0 && (
          <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap', mt: 2 }}>
            {tags.map((tag, index) => (
              <Chip
                key={index}
                label={tag}
                size="small"
                sx={{
                  background: 'rgba(102, 126, 234, 0.1)',
                  color: '#667eea',
                  fontWeight: 600,
                  fontSize: '0.75rem',
                  '&:hover': {
                    background: gradient,
                    color: 'white',
                  },
                  transition: 'all 0.3s ease',
                }}
              />
            ))}
          </Box>
        )}

        {/* Custom Children Content */}
        {children}
      </CardContent>

      {/* Actions */}
      <CardActions sx={{ px: 2, pb: 2, justifyContent: 'space-between' }}>
        <Box sx={{ display: 'flex', gap: 0.5 }}>
          <IconButton
            size="small"
            className="ripple"
            sx={{
              '&:hover': {
                background: 'rgba(102, 126, 234, 0.1)',
                color: '#667eea',
              },
            }}
          >
            <Favorite fontSize="small" />
          </IconButton>
          <IconButton
            size="small"
            className="ripple"
            sx={{
              '&:hover': {
                background: 'rgba(102, 126, 234, 0.1)',
                color: '#667eea',
              },
            }}
          >
            <Share fontSize="small" />
          </IconButton>
        </Box>
        
        <IconButton
          size="small"
          sx={{
            '&:hover': {
              background: 'rgba(102, 126, 234, 0.1)',
              color: '#667eea',
              transform: 'rotate(90deg)',
            },
            transition: 'all 0.3s ease',
          }}
        >
          <MoreVert fontSize="small" />
        </IconButton>
      </CardActions>
    </Card>
  );
};

/**
 * Stat Card Component - For displaying statistics
 */
export const StatCard = ({ title, value, change, icon, gradient }) => {
  const isPositive = change >= 0;
  
  return (
    <PremiumCard
      sx={{
        background: gradient || 'rgba(255, 255, 255, 0.9)',
        color: gradient ? 'white' : 'inherit',
      }}
    >
      <CardContent>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
          <Box>
            <Typography
              variant="caption"
              sx={{
                opacity: 0.8,
                fontWeight: 600,
                textTransform: 'uppercase',
                letterSpacing: '0.1em',
              }}
            >
              {title}
            </Typography>
            <Typography
              variant="h3"
              sx={{
                fontFamily: 'Poppins',
                fontWeight: 800,
                mt: 1,
                mb: 1,
              }}
            >
              {value}
            </Typography>
            {change !== undefined && (
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
                <TrendingUp
                  fontSize="small"
                  sx={{
                    transform: isPositive ? 'none' : 'rotate(180deg)',
                    color: isPositive ? '#4facfe' : '#f5576c',
                  }}
                />
                <Typography
                  variant="body2"
                  sx={{
                    color: isPositive ? '#4facfe' : '#f5576c',
                    fontWeight: 600,
                  }}
                >
                  {isPositive ? '+' : ''}{change}%
                </Typography>
              </Box>
            )}
          </Box>
          {icon && (
            <Box
              sx={{
                fontSize: 40,
                opacity: 0.3,
              }}
            >
              {icon}
            </Box>
          )}
        </Box>
      </CardContent>
    </PremiumCard>
  );
};

export default PremiumCard;
