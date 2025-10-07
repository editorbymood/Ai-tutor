import React, { useEffect, useState } from 'react';
import { Grid, Card, CardContent, Typography, Box, LinearProgress, Paper } from '@mui/material';
import { School, People, TrendingUp } from '@mui/icons-material';
import api from '../services/api';

const TeacherDashboard = () => {
  const [dashboardData, setDashboardData] = useState(null);
  const [loading, setLoading] = useState(true);

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

  if (loading) return <LinearProgress />;

  return (
    <Box>
      <Typography variant="h4" gutterBottom>Teacher Dashboard</Typography>
      
      <Grid container spacing={3} sx={{ mt: 2 }}>
        <Grid item xs={12} sm={4}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center' }}>
                <School fontSize="large" color="primary" sx={{ mr: 2 }} />
                <Box>
                  <Typography variant="h4">{dashboardData?.summary?.total_courses || 0}</Typography>
                  <Typography variant="body2" color="text.secondary">Total Courses</Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} sm={4}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center' }}>
                <People fontSize="large" color="success" sx={{ mr: 2 }} />
                <Box>
                  <Typography variant="h4">{dashboardData?.summary?.total_students || 0}</Typography>
                  <Typography variant="body2" color="text.secondary">Total Students</Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} sm={4}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center' }}>
                <TrendingUp fontSize="large" color="warning" sx={{ mr: 2 }} />
                <Box>
                  <Typography variant="h4">{dashboardData?.summary?.total_enrollments || 0}</Typography>
                  <Typography variant="body2" color="text.secondary">Total Enrollments</Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      <Paper sx={{ p: 3, mt: 3 }}>
        <Typography variant="h6" gutterBottom>Course Performance</Typography>
        {dashboardData?.courses?.map((course, index) => (
          <Box key={index} sx={{ mb: 3 }}>
            <Typography variant="subtitle1">{course.title}</Typography>
            <Grid container spacing={2} sx={{ mt: 1 }}>
              <Grid item xs={6} sm={3}>
                <Typography variant="body2" color="text.secondary">Students: {course.total_students}</Typography>
              </Grid>
              <Grid item xs={6} sm={3}>
                <Typography variant="body2" color="text.secondary">
                  Progress: {Math.round(course.average_progress)}%
                </Typography>
              </Grid>
              <Grid item xs={6} sm={3}>
                <Typography variant="body2" color="text.secondary">
                  Rating: {course.average_rating.toFixed(1)} ⭐
                </Typography>
              </Grid>
            </Grid>
            <LinearProgress variant="determinate" value={course.average_progress} sx={{ mt: 1 }} />
          </Box>
        ))}
      </Paper>
    </Box>
  );
};

export default TeacherDashboard;