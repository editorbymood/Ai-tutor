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
} from '@mui/material';
import {
  School,
  TrendingUp,
  EmojiEvents,
  LocalFireDepartment,
} from '@mui/icons-material';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
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
    return <LinearProgress />;
  }

  const stats = [
    {
      title: 'Courses Enrolled',
      value: dashboardData?.analytics?.courses_enrolled || 0,
      icon: <School fontSize="large" />,
      color: '#1976d2',
    },
    {
      title: 'Current Streak',
      value: `${dashboardData?.analytics?.current_streak || 0} days`,
      icon: <LocalFireDepartment fontSize="large" />,
      color: '#ff9800',
    },
    {
      title: 'Avg Quiz Score',
      value: `${Math.round(dashboardData?.analytics?.average_quiz_score || 0)}%`,
      icon: <TrendingUp fontSize="large" />,
      color: '#4caf50',
    },
    {
      title: 'Study Time',
      value: `${dashboardData?.analytics?.total_study_time || 0} min`,
      icon: <EmojiEvents fontSize="large" />,
      color: '#9c27b0',
    },
  ];

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Welcome back, {dashboardData?.user_info?.name}!
      </Typography>
      <Typography variant="body1" color="text.secondary" gutterBottom>
        Learning Style: {dashboardData?.user_info?.learning_style}
      </Typography>

      <Grid container spacing={3} sx={{ mt: 2 }}>
        {stats.map((stat, index) => (
          <Grid item xs={12} sm={6} md={3} key={index}>
            <Card>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <Box sx={{ color: stat.color, mr: 2 }}>
                    {stat.icon}
                  </Box>
                  <Box>
                    <Typography variant="h4">{stat.value}</Typography>
                    <Typography variant="body2" color="text.secondary">
                      {stat.title}
                    </Typography>
                  </Box>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      <Grid container spacing={3} sx={{ mt: 2 }}>
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Recent Quiz Performance
            </Typography>
            {dashboardData?.recent_quizzes?.length > 0 ? (
              <Box>
                {dashboardData.recent_quizzes.map((quiz, index) => (
                  <Box key={index} sx={{ mb: 2 }}>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                      <Typography variant="body2">{quiz.quiz_title}</Typography>
                      <Typography variant="body2" color={quiz.passed ? 'success.main' : 'error.main'}>
                        {Math.round(quiz.score)}%
                      </Typography>
                    </Box>
                    <LinearProgress
                      variant="determinate"
                      value={quiz.score}
                      color={quiz.passed ? 'success' : 'error'}
                    />
                  </Box>
                ))}
              </Box>
            ) : (
              <Typography variant="body2" color="text.secondary">
                No quiz attempts yet
              </Typography>
            )}
          </Paper>
        </Grid>

        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Quick Actions
            </Typography>
            <Button
              fullWidth
              variant="contained"
              sx={{ mb: 2 }}
              onClick={() => navigate('/courses')}
            >
              Browse Courses
            </Button>
            <Button
              fullWidth
              variant="outlined"
              sx={{ mb: 2 }}
              onClick={() => navigate('/ai-tutor')}
            >
              Chat with AI Tutor
            </Button>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default StudentDashboard;