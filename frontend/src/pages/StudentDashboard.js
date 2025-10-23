import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Grid,
  Card,
  CardContent,
  Typography,
  Box,
  LinearProgress,
  Button,
  Paper,
  Avatar,
  Chip,
  Stack,
  IconButton,
} from '@mui/material';
import {
  School,
  TrendingUp,
  EmojiEvents,
  LocalFireDepartment,
  AutoAwesome,
  ArrowForward,
  Star,
  Timer,
  CheckCircle,
  PlayCircleOutline,
} from '@mui/icons-material';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, AreaChart, Area } from 'recharts';
import api from '../services/api';

const StudentDashboard = () => {
  const navigate = useNavigate();
  const [dashboardData, setDashboardData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      const response = await api.get('/analytics/dashboard/student/');
      setDashboardData(response.data.data);
    } catch (error) {
      console.error('Failed to fetch dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '70vh' }}>
        <Box sx={{ textAlign: 'center' }}>
          <LinearProgress sx={{ width: 200, mb: 2 }} />
          <Typography color="text.secondary">Loading your dashboard...</Typography>
        </Box>
      </Box>
    );
  }

  const stats = [
    {
      title: 'Courses Enrolled',
      value: dashboardData?.analytics?.courses_enrolled || 0,
      icon: <School />,
      gradient: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      bgGradient: 'linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%)',
    },
    {
      title: 'Current Streak',
      value: `${dashboardData?.analytics?.current_streak || 0}`,
      suffix: 'days',
      icon: <LocalFireDepartment />,
      gradient: 'linear-gradient(135deg, #fa709a 0%, #fee140 100%)',
      bgGradient: 'linear-gradient(135deg, rgba(250, 112, 154, 0.1) 0%, rgba(254, 225, 64, 0.1) 100%)',
    },
    {
      title: 'Avg Quiz Score',
      value: `${Math.round(dashboardData?.analytics?.average_quiz_score || 0)}`,
      suffix: '%',
      icon: <TrendingUp />,
      gradient: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
      bgGradient: 'linear-gradient(135deg, rgba(79, 172, 254, 0.1) 0%, rgba(0, 242, 254, 0.1) 100%)',
    },
    {
      title: 'Study Time',
      value: `${dashboardData?.analytics?.total_study_time || 0}`,
      suffix: 'min',
      icon: <Timer />,
      gradient: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
      bgGradient: 'linear-gradient(135deg, rgba(240, 147, 251, 0.1) 0%, rgba(245, 87, 108, 0.1) 100%)',
    },
  ];

  return (
    <Box className="fade-in">
      {/* Welcome Header */}
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
          <Stack direction="row" spacing={3} alignItems="center">
            <Avatar
              sx={{
                width: 80,
                height: 80,
                border: '4px solid rgba(255, 255, 255, 0.3)',
                background: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
                fontSize: '2rem',
              }}
            >
              {dashboardData?.user_info?.name?.charAt(0).toUpperCase()}
            </Avatar>
            <Box sx={{ flex: 1 }}>
              <Typography variant="h3" sx={{ fontWeight: 800, mb: 1 }}>
                Welcome back, {dashboardData?.user_info?.name}! 👋
              </Typography>
              <Stack direction="row" spacing={2} alignItems="center">
                <Chip
                  icon={<AutoAwesome />}
                  label={`Learning Style: ${dashboardData?.user_info?.learning_style || 'Not set'}`}
                  sx={{
                    background: 'rgba(255, 255, 255, 0.2)',
                    color: 'white',
                    fontWeight: 600,
                    '& .MuiChip-icon': { color: 'white' },
                  }}
                />
                <Chip
                  icon={<EmojiEvents />}
                  label="Level 5 Learner"
                  sx={{
                    background: 'rgba(255, 255, 255, 0.2)',
                    color: 'white',
                    fontWeight: 600,
                    '& .MuiChip-icon': { color: '#fee140' },
                  }}
                />
              </Stack>
            </Box>
            <Button
              variant="contained"
              endIcon={<ArrowForward />}
              onClick={() => navigate('/ai-tutor')}
              sx={{
                background: 'white',
                color: '#667eea',
                px: 3,
                py: 1.5,
                borderRadius: '12px',
                fontWeight: 700,
                '&:hover': {
                  background: 'rgba(255, 255, 255, 0.9)',
                  transform: 'translateY(-2px)',
                },
                transition: 'all 0.3s ease',
              }}
            >
              Chat with AI
            </Button>
          </Stack>
        </Box>
      </Paper>

      {/* Stats Grid */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        {stats.map((stat, index) => (
          <Grid item xs={12} sm={6} md={3} key={index}>
            <Card
              className="hover-lift"
              sx={{
                height: '100%',
                borderRadius: '20px',
                background: stat.bgGradient,
                border: '1px solid rgba(0, 0, 0, 0.05)',
                transition: 'all 0.3s ease',
              }}
            >
              <CardContent sx={{ p: 3 }}>
                <Stack direction="row" spacing={2} alignItems="flex-start">
                  <Box
                    sx={{
                      width: 56,
                      height: 56,
                      borderRadius: '16px',
                      background: stat.gradient,
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      color: 'white',
                      fontSize: 28,
                      boxShadow: '0 4px 12px rgba(0, 0, 0, 0.15)',
                    }}
                  >
                    {stat.icon}
                  </Box>
                  <Box sx={{ flex: 1 }}>
                    <Typography variant="h3" sx={{ fontWeight: 800, mb: 0.5 }}>
                      {stat.value}
                      {stat.suffix && (
                        <Typography component="span" variant="h6" sx={{ ml: 0.5, opacity: 0.7 }}>
                          {stat.suffix}
                        </Typography>
                      )}
                    </Typography>
                    <Typography variant="body2" color="text.secondary" sx={{ fontWeight: 600 }}>
                      {stat.title}
                    </Typography>
                  </Box>
                </Stack>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      <Grid container spacing={3}>
        {/* Quiz Performance */}
        <Grid item xs={12} md={8}>
          <Paper
            sx={{
              p: 4,
              borderRadius: '24px',
              height: '100%',
              background: 'white',
              boxShadow: '0 4px 20px rgba(0, 0, 0, 0.08)',
            }}
          >
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
              <Box>
                <Typography variant="h5" sx={{ fontWeight: 700, mb: 0.5 }}>
                  Recent Quiz Performance
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Track your progress over time
                </Typography>
              </Box>
              <IconButton
                sx={{
                  background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                  color: 'white',
                  '&:hover': { background: 'linear-gradient(135deg, #5568d3 0%, #6a3f8f 100%)' },
                }}
              >
                <TrendingUp />
              </IconButton>
            </Box>

            {dashboardData?.recent_quizzes?.length > 0 ? (
              <Box>
                {dashboardData.recent_quizzes.map((quiz, index) => (
                  <Box
                    key={index}
                    sx={{
                      mb: 3,
                      p: 3,
                      borderRadius: '16px',
                      background: quiz.passed
                        ? 'linear-gradient(135deg, rgba(79, 172, 254, 0.05) 0%, rgba(0, 242, 254, 0.05) 100%)'
                        : 'linear-gradient(135deg, rgba(244, 67, 54, 0.05) 0%, rgba(233, 30, 99, 0.05) 100%)',
                      border: '1px solid',
                      borderColor: quiz.passed ? 'rgba(79, 172, 254, 0.2)' : 'rgba(244, 67, 54, 0.2)',
                      transition: 'all 0.3s ease',
                      '&:hover': {
                        transform: 'translateX(8px)',
                        boxShadow: '0 4px 12px rgba(0, 0, 0, 0.1)',
                      },
                    }}
                  >
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                        {quiz.passed ? (
                          <CheckCircle sx={{ color: '#4facfe', fontSize: 32 }} />
                        ) : (
                          <PlayCircleOutline sx={{ color: '#f44336', fontSize: 32 }} />
                        )}
                        <Box>
                          <Typography variant="h6" sx={{ fontWeight: 700 }}>
                            {quiz.quiz_title}
                          </Typography>
                          <Typography variant="caption" color="text.secondary">
                            Completed recently
                          </Typography>
                        </Box>
                      </Box>
                      <Box sx={{ textAlign: 'right' }}>
                        <Typography
                          variant="h4"
                          sx={{
                            fontWeight: 800,
                            color: quiz.passed ? '#4facfe' : '#f44336',
                          }}
                        >
                          {Math.round(quiz.score)}%
                        </Typography>
                        <Chip
                          label={quiz.passed ? 'Passed' : 'Retry'}
                          size="small"
                          sx={{
                            background: quiz.passed
                              ? 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)'
                              : 'linear-gradient(135deg, #f44336 0%, #e91e63 100%)',
                            color: 'white',
                            fontWeight: 600,
                          }}
                        />
                      </Box>
                    </Box>
                    <LinearProgress
                      variant="determinate"
                      value={quiz.score}
                      sx={{
                        height: 8,
                        borderRadius: '4px',
                        backgroundColor: 'rgba(0, 0, 0, 0.05)',
                        '& .MuiLinearProgress-bar': {
                          borderRadius: '4px',
                          background: quiz.passed
                            ? 'linear-gradient(90deg, #4facfe 0%, #00f2fe 100%)'
                            : 'linear-gradient(90deg, #f44336 0%, #e91e63 100%)',
                        },
                      }}
                    />
                  </Box>
                ))}
              </Box>
            ) : (
              <Box sx={{ textAlign: 'center', py: 8 }}>
                <EmojiEvents sx={{ fontSize: 80, color: 'text.disabled', mb: 2 }} />
                <Typography variant="h6" color="text.secondary" gutterBottom>
                  No quiz attempts yet
                </Typography>
                <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
                  Start taking quizzes to track your progress
                </Typography>
                <Button
                  variant="contained"
                  onClick={() => navigate('/courses')}
                  sx={{
                    borderRadius: '12px',
                    px: 4,
                    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                  }}
                >
                  Browse Courses
                </Button>
              </Box>
            )}
          </Paper>
        </Grid>

        {/* Quick Actions & Achievements */}
        <Grid item xs={12} md={4}>
          <Stack spacing={3}>
            {/* Quick Actions */}
            <Paper
              sx={{
                p: 3,
                borderRadius: '24px',
                background: 'white',
                boxShadow: '0 4px 20px rgba(0, 0, 0, 0.08)',
              }}
            >
              <Typography variant="h6" sx={{ fontWeight: 700, mb: 3 }}>
                Quick Actions
              </Typography>
              <Stack spacing={2}>
                <Button
                  fullWidth
                  variant="contained"
                  startIcon={<School />}
                  onClick={() => navigate('/courses')}
                  sx={{
                    py: 1.5,
                    borderRadius: '12px',
                    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                    justifyContent: 'flex-start',
                    textTransform: 'none',
                    fontWeight: 600,
                    '&:hover': {
                      transform: 'translateX(4px)',
                    },
                    transition: 'all 0.3s ease',
                  }}
                >
                  Browse Courses
                </Button>
                <Button
                  fullWidth
                  variant="outlined"
                  startIcon={<AutoAwesome />}
                  onClick={() => navigate('/ai-tutor')}
                  sx={{
                    py: 1.5,
                    borderRadius: '12px',
                    borderColor: '#667eea',
                    color: '#667eea',
                    justifyContent: 'flex-start',
                    textTransform: 'none',
                    fontWeight: 600,
                    '&:hover': {
                      borderColor: '#667eea',
                      background: 'rgba(102, 126, 234, 0.05)',
                      transform: 'translateX(4px)',
                    },
                    transition: 'all 0.3s ease',
                  }}
                >
                  Chat with AI Tutor
                </Button>
                <Button
                  fullWidth
                  variant="outlined"
                  startIcon={<EmojiEvents />}
                  onClick={() => navigate('/profile')}
                  sx={{
                    py: 1.5,
                    borderRadius: '12px',
                    borderColor: '#fa709a',
                    color: '#fa709a',
                    justifyContent: 'flex-start',
                    textTransform: 'none',
                    fontWeight: 600,
                    '&:hover': {
                      borderColor: '#fa709a',
                      background: 'rgba(250, 112, 154, 0.05)',
                      transform: 'translateX(4px)',
                    },
                    transition: 'all 0.3s ease',
                  }}
                >
                  View Achievements
                </Button>
              </Stack>
            </Paper>

            {/* Recent Achievements */}
            <Paper
              sx={{
                p: 3,
                borderRadius: '24px',
                background: 'linear-gradient(135deg, rgba(250, 112, 154, 0.1) 0%, rgba(254, 225, 64, 0.1) 100%)',
                border: '1px solid rgba(250, 112, 154, 0.2)',
              }}
            >
              <Typography variant="h6" sx={{ fontWeight: 700, mb: 2 }}>
                Recent Achievements 🏆
              </Typography>
              <Stack spacing={2}>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                  <Box
                    sx={{
                      width: 48,
                      height: 48,
                      borderRadius: '12px',
                      background: 'linear-gradient(135deg, #fa709a 0%, #fee140 100%)',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      fontSize: '24px',
                    }}
                  >
                    🔥
                  </Box>
                  <Box>
                    <Typography variant="body2" sx={{ fontWeight: 700 }}>
                      7-Day Streak!
                    </Typography>
                    <Typography variant="caption" color="text.secondary">
                      Keep up the momentum
                    </Typography>
                  </Box>
                </Box>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                  <Box
                    sx={{
                      width: 48,
                      height: 48,
                      borderRadius: '12px',
                      background: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      fontSize: '24px',
                    }}
                  >
                    ⭐
                  </Box>
                  <Box>
                    <Typography variant="body2" sx={{ fontWeight: 700 }}>
                      Perfect Score
                    </Typography>
                    <Typography variant="caption" color="text.secondary">
                      100% on Python Quiz
                    </Typography>
                  </Box>
                </Box>
              </Stack>
            </Paper>
          </Stack>
        </Grid>
      </Grid>
    </Box>
  );
};

export default StudentDashboard;