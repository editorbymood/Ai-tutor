import React from 'react';
import { useSelector } from 'react-redux';
import { Box, Typography, Paper, Avatar, Chip, Stack, Grid, Card, CardContent, Button, Divider } from '@mui/material';
import { Edit, EmojiEvents, School, TrendingUp, Star, Psychology, Email, Person } from '@mui/icons-material';

const Profile = () => {
  const { user } = useSelector((state) => state.auth);

  const achievements = [
    { icon: '🔥', title: '7-Day Streak', color: '#fa709a' },
    { icon: '⭐', title: 'Top Performer', color: '#fee140' },
    { icon: '🏆', title: 'Course Complete', color: '#4facfe' },
    { icon: '💡', title: 'Quick Learner', color: '#f093fb' },
  ];

  return (
    <Box className="fade-in">
      {/* Header */}
      <Paper
        sx={{
          p: 4,
          mb: 4,
          borderRadius: '24px',
          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
          color: 'white',
          position: 'relative',
          overflow: 'hidden',
        }}
      >
        <Box
          sx={{
            position: 'absolute',
            top: -50,
            right: -50,
            width: 200,
            height: 200,
            borderRadius: '50%',
            background: 'rgba(255, 255, 255, 0.1)',
            filter: 'blur(40px)',
          }}
        />
        <Box sx={{ position: 'relative', zIndex: 1 }}>
          <Stack direction={{ xs: 'column', md: 'row' }} spacing={4} alignItems="center">
            <Avatar
              src={user?.avatar}
              sx={{
                width: 120,
                height: 120,
                border: '6px solid rgba(255, 255, 255, 0.3)',
                background: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
                fontSize: '3rem',
                fontWeight: 800,
              }}
            >
              {user?.full_name?.charAt(0).toUpperCase()}
            </Avatar>
            <Box sx={{ flex: 1, textAlign: { xs: 'center', md: 'left' } }}>
              <Typography variant="h3" sx={{ fontWeight: 900, mb: 1 }}>
                {user?.full_name}
              </Typography>
              <Typography variant="h6" sx={{ opacity: 0.9, mb: 2 }}>
                {user?.email}
              </Typography>
              <Stack direction="row" spacing={1} flexWrap="wrap" justifyContent={{ xs: 'center', md: 'flex-start' }}>
                <Chip
                  label={user?.role}
                  sx={{
                    background: 'rgba(255, 255, 255, 0.2)',
                    color: 'white',
                    fontWeight: 700,
                    textTransform: 'capitalize',
                  }}
                />
                <Chip
                  icon={<Psychology />}
                  label={`${user?.learning_style || 'Visual'} Learner`}
                  sx={{
                    background: 'rgba(255, 255, 255, 0.2)',
                    color: 'white',
                    fontWeight: 600,
                    '& .MuiChip-icon': { color: 'white' },
                  }}
                />
              </Stack>
            </Box>
            <Button
              variant="contained"
              startIcon={<Edit />}
              sx={{
                px: 4,
                py: 1.5,
                borderRadius: '12px',
                background: 'white',
                color: '#667eea',
                fontWeight: 700,
                '&:hover': {
                  background: 'rgba(255, 255, 255, 0.9)',
                },
              }}
            >
              Edit Profile
            </Button>
          </Stack>
        </Box>
      </Paper>

      <Grid container spacing={3}>
        {/* Learning Stats */}
        <Grid item xs={12} md={8}>
          <Paper
            sx={{
              p: 4,
              borderRadius: '24px',
              background: 'white',
              boxShadow: '0 4px 20px rgba(0, 0, 0, 0.08)',
            }}
          >
            <Typography variant="h5" sx={{ fontWeight: 700, mb: 3 }}>
              Learning Stats 📊
            </Typography>
            <Grid container spacing={3}>
              <Grid item xs={12} sm={6}>
                <Card
                  sx={{
                    borderRadius: '16px',
                    background: 'linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%)',
                    border: '1px solid rgba(102, 126, 234, 0.2)',
                  }}
                >
                  <CardContent sx={{ p: 3 }}>
                    <Stack direction="row" spacing={2} alignItems="center">
                      <Box
                        sx={{
                          width: 56,
                          height: 56,
                          borderRadius: '12px',
                          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'center',
                          color: 'white',
                        }}
                      >
                        <School sx={{ fontSize: 28 }} />
                      </Box>
                      <Box>
                        <Typography variant="h3" sx={{ fontWeight: 800, color: '#667eea' }}>
                          12
                        </Typography>
                        <Typography variant="body2" color="text.secondary" sx={{ fontWeight: 600 }}>
                          Courses Completed
                        </Typography>
                      </Box>
                    </Stack>
                  </CardContent>
                </Card>
              </Grid>
              <Grid item xs={12} sm={6}>
                <Card
                  sx={{
                    borderRadius: '16px',
                    background: 'linear-gradient(135deg, rgba(79, 172, 254, 0.1) 0%, rgba(0, 242, 254, 0.1) 100%)',
                    border: '1px solid rgba(79, 172, 254, 0.2)',
                  }}
                >
                  <CardContent sx={{ p: 3 }}>
                    <Stack direction="row" spacing={2} alignItems="center">
                      <Box
                        sx={{
                          width: 56,
                          height: 56,
                          borderRadius: '12px',
                          background: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'center',
                          color: 'white',
                        }}
                      >
                        <TrendingUp sx={{ fontSize: 28 }} />
                      </Box>
                      <Box>
                        <Typography variant="h3" sx={{ fontWeight: 800, color: '#4facfe' }}>
                          87%
                        </Typography>
                        <Typography variant="body2" color="text.secondary" sx={{ fontWeight: 600 }}>
                          Average Score
                        </Typography>
                      </Box>
                    </Stack>
                  </CardContent>
                </Card>
              </Grid>
            </Grid>

            <Divider sx={{ my: 4 }} />

            <Typography variant="h6" sx={{ fontWeight: 700, mb: 3 }}>
              Learning Information
            </Typography>
            <Stack spacing={3}>
              <Box>
                <Typography variant="body2" color="text.secondary" sx={{ mb: 1, fontWeight: 600 }}>
                  Learning Style
                </Typography>
                <Chip
                  icon={<Psychology />}
                  label={user?.learning_style || 'Visual'}
                  sx={{
                    background: 'linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%)',
                    color: '#667eea',
                    fontWeight: 700,
                    '& .MuiChip-icon': { color: '#667eea' },
                  }}
                />
              </Box>
              {user?.grade_level && (
                <Box>
                  <Typography variant="body2" color="text.secondary" sx={{ mb: 1, fontWeight: 600 }}>
                    Grade Level
                  </Typography>
                  <Chip
                    label={user.grade_level}
                    sx={{
                      background: 'linear-gradient(135deg, rgba(79, 172, 254, 0.1) 0%, rgba(0, 242, 254, 0.1) 100%)',
                      color: '#4facfe',
                      fontWeight: 700,
                    }}
                  />
                </Box>
              )}
            </Stack>
          </Paper>
        </Grid>

        {/* Achievements */}
        <Grid item xs={12} md={4}>
          <Paper
            sx={{
              p: 4,
              borderRadius: '24px',
              background: 'white',
              boxShadow: '0 4px 20px rgba(0, 0, 0, 0.08)',
            }}
          >
            <Typography variant="h5" sx={{ fontWeight: 700, mb: 3 }}>
              Achievements 🏆
            </Typography>
            <Stack spacing={2}>
              {achievements.map((achievement, index) => (
                <Paper
                  key={index}
                  sx={{
                    p: 2,
                    borderRadius: '12px',
                    background: `linear-gradient(135deg, ${achievement.color}15 0%, ${achievement.color}05 100%)`,
                    border: `1px solid ${achievement.color}30`,
                  }}
                >
                  <Stack direction="row" spacing={2} alignItems="center">
                    <Box
                      sx={{
                        width: 48,
                        height: 48,
                        borderRadius: '10px',
                        background: `${achievement.color}20`,
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        fontSize: '24px',
                      }}
                    >
                      {achievement.icon}
                    </Box>
                    <Typography variant="body1" sx={{ fontWeight: 700 }}>
                      {achievement.title}
                    </Typography>
                  </Stack>
                </Paper>
              ))}
            </Stack>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Profile;