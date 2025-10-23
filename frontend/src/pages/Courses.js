import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import {
  Grid,
  Card,
  CardContent,
  CardMedia,
  Typography,
  Button,
  Chip,
  Box,
  CircularProgress,
} from '@mui/material';
import { School } from '@mui/icons-material';
import { fetchCourses } from '../redux/slices/coursesSlice';

const Courses = () => {
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const { courses, loading } = useSelector((state) => state.courses);

  useEffect(() => {
    dispatch(fetchCourses());
  }, [dispatch]);

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Available Courses
      </Typography>

      <Grid container spacing={3} sx={{ mt: 2 }}>
        {courses && courses.length > 0 ? (
          courses.map((course) => (
            <Grid item xs={12} sm={6} md={4} key={course.id}>
              <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
                <CardMedia
                  component="div"
                  sx={{
                    height: 140,
                    backgroundColor: '#1976d2',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                  }}
                >
                  <School sx={{ fontSize: 60, color: 'white' }} />
                </CardMedia>
                <CardContent sx={{ flexGrow: 1 }}>
                  <Typography gutterBottom variant="h6" component="div">
                    {course.title}
                  </Typography>
                  <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                    {course.description && course.description.substring(0, 100)}...
                  </Typography>
                  <Box sx={{ mb: 2 }}>
                    <Chip label={course.difficulty} size="small" sx={{ mr: 1 }} />
                    <Chip label={course.category} size="small" variant="outlined" />
                  </Box>
                  <Typography variant="body2" color="text.secondary">
                    {course.total_lessons || 0} lessons • {course.estimated_duration || 0} hours
                  </Typography>
                </CardContent>
                <Box sx={{ p: 2 }}>
                  <Button
                    fullWidth
                    variant="contained"
                    onClick={() => navigate(`/courses/${course.id}`)}
                  >
                    View Course
                  </Button>
                </Box>
              </Card>
            </Grid>
          ))
        ) : (
          <Grid item xs={12}>
            <Box sx={{ textAlign: 'center', py: 8 }}>
              <School sx={{ fontSize: 80, color: 'text.secondary', mb: 2 }} />
              <Typography variant="h6" color="text.secondary">
                No courses available at the moment
              </Typography>
              <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                Check back later for new courses!
              </Typography>
            </Box>
          </Grid>
        )}
      </Grid>
    </Box>
  );
};

export default Courses;