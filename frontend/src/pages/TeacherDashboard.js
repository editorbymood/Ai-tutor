import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Grid, Card, CardContent, Typography, Box, LinearProgress, Paper, Avatar, Stack, Button, Chip } from '@mui/material';
import { School, People, TrendingUp, Add, BarChart, Star, EmojiEvents } from '@mui/icons-material';
import api from '../services/api';

const TeacherDashboard = () => {
  const [dashboardData, setDashboardData] = useState(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      const response = await api.get('/analytics/dashboard/teacher/');
      setDashboardData(response.data.data);
    } catch (error) {
      console.error('Failed to fetch dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return (
    <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '70vh' }}>
      <Box sx={{ textAlign: 'center' }}>
        <LinearProgress sx={{ width: 200, mb: 2 }} />
        <Typography color="text.secondary">Loading dashboard...</Typography>
      </Box>
    </Box>
  );

  return (
    <Box className="fade-in">
      {/* Header */}
      <Paper
        sx={{
          p: 4,
          mb: 4,
          borderRadius: '24px',
          background: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
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
        <Box sx={{ position: 'relative', zIndex: 1, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <Box>
            <Typography variant="h3" sx={{ fontWeight: 800, mb: 1 }}>
              Teacher Dashboard 🎓
            </Typography>
            <Typography variant="h6" sx={{ opacity: 0.9 }}>
              Manage your courses and track student progress
            </Typography>
          </Box>
          <Button
            variant="contained"
            startIcon={<Add />}
            sx={{
              background: 'white',
              color: '#f093fb',
              px: 4,
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
            Create Course
          </Button>
        </Box>
      </Paper>

      {/* Stats Grid */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={4}>
          <Card
            className="hover-lift"
            sx={{
              borderRadius: '20px',
              background: 'linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%)',
              border: '1px solid rgba(102, 126, 234, 0.2)',
            }}
          >
            <CardContent sx={{ p: 3 }}>
              <Stack direction="row" spacing={2} alignItems="center">
                <Box
                  sx={{
                    width: 64,
                    height: 64,
                    borderRadius: '16px',
                    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    color: 'white',
                    boxShadow: '0 4px 12px rgba(102, 126, 234, 0.3)',
                  }}
                >
                  <School sx={{ fontSize: 32 }} />
                </Box>
                <Box>
                  <Typography variant="h3" sx={{ fontWeight: 800 }}>
                    {dashboardData?.summary?.total_courses || 0}
                  </Typography>
                  <Typography variant="body2" color="text.secondary" sx={{ fontWeight: 600 }}>
                    Total Courses
                  </Typography>
                </Box>
              </Stack>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={4}>
          <Card
            className="hover-lift"
            sx={{
              borderRadius: '20px',
              background: 'linear-gradient(135deg, rgba(79, 172, 254, 0.1) 0%, rgba(0, 242, 254, 0.1) 100%)',
              border: '1px solid rgba(79, 172, 254, 0.2)',
            }}
          >
            <CardContent sx={{ p: 3 }}>
              <Stack direction="row" spacing={2} alignItems="center">
                <Box
                  sx={{
                    width: 64,
                    height: 64,
                    borderRadius: '16px',
                    background: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    color: 'white',
                    boxShadow: '0 4px 12px rgba(79, 172, 254, 0.3)',
                  }}
                >
                  <People sx={{ fontSize: 32 }} />
                </Box>
                <Box>
                  <Typography variant="h3" sx={{ fontWeight: 800 }}>
                    {dashboardData?.summary?.total_students || 0}
                  </Typography>
                  <Typography variant="body2" color="text.secondary" sx={{ fontWeight: 600 }}>
                    Total Students
                  </Typography>
                </Box>
              </Stack>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={4}>
          <Card
            className="hover-lift"
            sx={{
              borderRadius: '20px',
              background: 'linear-gradient(135deg, rgba(250, 112, 154, 0.1) 0%, rgba(254, 225, 64, 0.1) 100%)',
              border: '1px solid rgba(250, 112, 154, 0.2)',
            }}
          >
            <CardContent sx={{ p: 3 }}>
              <Stack direction="row" spacing={2} alignItems="center">
                <Box
                  sx={{
                    width: 64,
                    height: 64,
                    borderRadius: '16px',
                    background: 'linear-gradient(135deg, #fa709a 0%, #fee140 100%)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    color: 'white',
                    boxShadow: '0 4px 12px rgba(250, 112, 154, 0.3)',
                  }}
                >
                  <TrendingUp sx={{ fontSize: 32 }} />
                </Box>
                <Box>
                  <Typography variant="h3" sx={{ fontWeight: 800 }}>
                    {dashboardData?.summary?.total_enrollments || 0}
                  </Typography>
                  <Typography variant="body2" color="text.secondary" sx={{ fontWeight: 600 }}>
                    Total Enrollments
                  </Typography>
                </Box>
              </Stack>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Course Performance */}
      <Paper
        sx={{
          p: 4,
          borderRadius: '24px',
          background: 'white',
          boxShadow: '0 4px 20px rgba(0, 0, 0, 0.08)',
        }}
      >
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 4 }}>
          <Box>
            <Typography variant="h5" sx={{ fontWeight: 700, mb: 0.5 }}>
              Course Performance Overview
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Monitor student engagement and progress
            </Typography>
          </Box>
          <Button
            startIcon={<BarChart />}
            sx={{
              borderRadius: '12px',
              textTransform: 'none',
              fontWeight: 600,
            }}
          >
            View Analytics
          </Button>
        </Box>

        {dashboardData?.courses && dashboardData.courses.length > 0 ? (
          dashboardData.courses.map((course, index) => (
            <Paper
              key={index}
              sx={{
                p: 3,
                mb: 3,
                borderRadius: '16px',
                background: 'linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%)',
                border: '1px solid rgba(102, 126, 234, 0.1)',
                transition: 'all 0.3s ease',
                '&:hover': {
                  transform: 'translateX(8px)',
                  boxShadow: '0 4px 12px rgba(0, 0, 0, 0.1)',
                },
              }}
            >
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                <Box sx={{ flex: 1 }}>
                  <Typography variant="h6" sx={{ fontWeight: 700, mb: 1 }}>
                    {course.title}
                  </Typography>
                  <Stack direction="row" spacing={2} flexWrap="wrap">
                    <Chip
                      icon={<People />}
                      label={`${course.total_students} Students`}
                      size="small"
                      sx={{ background: 'rgba(102, 126, 234, 0.1)', color: '#667eea' }}
                    />
                    <Chip
                      icon={<TrendingUp />}
                      label={`${Math.round(course.average_progress)}% Avg Progress`}
                      size="small"
                      sx={{ background: 'rgba(79, 172, 254, 0.1)', color: '#4facfe' }}
                    />
                    <Chip
                      icon={<Star />}
                      label={`${course.average_rating.toFixed(1)} Rating`}
                      size="small"
                      sx={{ background: 'rgba(254, 225, 64, 0.2)', color: '#fa709a' }}
                    />
                  </Stack>
                </Box>
                <Button
                  variant="outlined"
                  size="small"
                  sx={{
                    borderRadius: '8px',
                    borderColor: '#667eea',
                    color: '#667eea',
                    '&:hover': {
                      borderColor: '#667eea',
                      background: 'rgba(102, 126, 234, 0.05)',
                    },
                  }}
                >
                  View Details
                </Button>
              </Box>
              <Box>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                  <Typography variant="body2" color="text.secondary">
                    Class Progress
                  </Typography>
                  <Typography variant="body2" sx={{ fontWeight: 700, color: '#667eea' }}>
                    {Math.round(course.average_progress)}%
                  </Typography>
                </Box>
                <LinearProgress
                  variant="determinate"
                  value={course.average_progress}
                  sx={{
                    height: 8,
                    borderRadius: '4px',
                    backgroundColor: 'rgba(102, 126, 234, 0.1)',
                    '& .MuiLinearProgress-bar': {
                      borderRadius: '4px',
                      background: 'linear-gradient(90deg, #667eea 0%, #764ba2 100%)',
                    },
                  }}
                />
              </Box>
            </Paper>
          ))
        ) : (
          <Box sx={{ textAlign: 'center', py: 8 }}>
            <School sx={{ fontSize: 80, color: 'text.disabled', mb: 2 }} />
            <Typography variant="h6" color="text.secondary" gutterBottom>
              No courses created yet
            </Typography>
            <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
              Create your first course to start teaching
            </Typography>
            <Button
              variant="contained"
              startIcon={<Add />}
              sx={{
                borderRadius: '12px',
                px: 4,
                background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
              }}
            >
              Create Course
            </Button>
          </Box>
        )}
      </Paper>
    </Box>
  );
};

export default TeacherDashboard;