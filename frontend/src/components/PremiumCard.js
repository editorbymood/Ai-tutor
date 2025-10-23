import React from 'react';
import { Card as MuiCard, Box } from '@mui/material';

const PremiumCard = ({
  children,
  gradient,
  hover = true,
  glow = false,
  className = '',
  sx = {},
  ...props
}) => {
  return (
    <MuiCard
      className={`${hover ? 'hover-lift' : ''} ${glow ? 'glow' : ''} ${className}`}
      sx={{
        position: 'relative',
        overflow: 'hidden',
        borderRadius: '24px',
        background: gradient || 'rgba(255, 255, 255, 0.95)',
        backdropFilter: 'blur(20px)',
        border: '1px solid rgba(255, 255, 255, 0.3)',
        boxShadow: '0 8px 32px rgba(0, 0, 0, 0.1)',
        transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
        '&:hover': hover
          ? {
              transform: 'translateY(-8px) scale(1.02)',
              boxShadow: '0 16px 48px rgba(0, 0, 0, 0.2)',
            }
          : {},
        '&::before': gradient
          ? {
              content: '""',
              position: 'absolute',
              top: 0,
              left: 0,
              right: 0,
              bottom: 0,
              background: gradient,
              opacity: 0.1,
              zIndex: 0,
            }
          : {},
        ...sx,
      }}
      {...props}
    >
      {gradient && (
        <Box
          sx={{
            position: 'absolute',
            top: -100,
            right: -100,
            width: 200,
            height: 200,
            borderRadius: '50%',
            background: 'rgba(255, 255, 255, 0.1)',
            filter: 'blur(40px)',
            zIndex: 0,
          }}
        />
      )}
      <Box sx={{ position: 'relative', zIndex: 1 }}>{children}</Box>
    </MuiCard>
  );
};

export default PremiumCard;

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
