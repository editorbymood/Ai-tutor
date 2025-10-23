import React from 'react';
import { Card, CardContent, Box, Typography, Stack } from '@mui/material';
import { TrendingUp } from '@mui/icons-material';

const StatCard = ({
  title,
  value,
  icon: Icon,
  gradient = 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
  bgGradient = 'linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%)',
  suffix = '',
  trend,
  trendValue,
  className = '',
}) => {
  return (
    <Card
      className={`hover-lift ${className}`}
      sx={{
        borderRadius: '20px',
        background: bgGradient,
        border: '1px solid rgba(0, 0, 0, 0.05)',
        transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
        '&:hover': {
          transform: 'translateY(-8px)',
          boxShadow: '0 12px 40px rgba(0, 0, 0, 0.15)',
        },
      }}
    >
      <CardContent sx={{ p: 3 }}>
        <Stack direction="row" spacing={2} alignItems="flex-start">
          {Icon && (
            <Box
              sx={{
                width: 56,
                height: 56,
                borderRadius: '16px',
                background: gradient,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                color: 'white',
                boxShadow: '0 4px 12px rgba(0, 0, 0, 0.15)',
              }}
            >
              <Icon sx={{ fontSize: 28 }} />
            </Box>
          )}
          <Box sx={{ flex: 1 }}>
            <Typography
              variant="h3"
              sx={{
                fontWeight: 800,
                mb: 0.5,
                display: 'flex',
                alignItems: 'baseline',
              }}
            >
              {value}
              {suffix && (
                <Typography
                  component="span"
                  variant="h6"
                  sx={{ ml: 0.5, opacity: 0.7, fontWeight: 600 }}
                >
                  {suffix}
                </Typography>
              )}
            </Typography>
            <Typography
              variant="body2"
              color="text.secondary"
              sx={{ fontWeight: 600, mb: trend ? 1 : 0 }}
            >
              {title}
            </Typography>
            {trend && (
              <Stack direction="row" spacing={0.5} alignItems="center">
                <TrendingUp
                  sx={{
                    fontSize: 16,
                    color: trend === 'up' ? '#4facfe' : '#f5576c',
                    transform: trend === 'down' ? 'rotate(180deg)' : 'none',
                  }}
                />
                <Typography
                  variant="caption"
                  sx={{
                    color: trend === 'up' ? '#4facfe' : '#f5576c',
                    fontWeight: 700,
                  }}
                >
                  {trendValue}
                </Typography>
              </Stack>
            )}
          </Box>
        </Stack>
      </CardContent>
    </Card>
  );
};

export default StatCard;
