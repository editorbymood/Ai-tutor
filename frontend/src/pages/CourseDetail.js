import React, { useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import {
  Box,
  Typography,
  Button,
  Paper,
  Chip,
  List,
  ListItem,
  ListItemText,
  CircularProgress,
  Alert,
} from '@mui/material';
import { PlayCircleOutline } from '@mui/icons-material';
import { fetchCourseDetail, enrollCourse } from '../redux/slices/coursesSlice';

const CourseDetail = () => {
  const { id } = useParams();
  const dispatch = useDispatch();
  const { currentCourse, loading, error } = useSelector((state) => state.courses);

  useEffect(() => {
    dispatch(fetchCourseDetail(id));
  }, [dispatch, id]);

  const handleEnroll = async () => {
    await dispatch(enrollCourse(id));
  };

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
        <CircularProgress />
      </Box>
    );
  }

  if (!currentCourse) return null;

  return (
    <Box>
      <Paper sx={{ p: 4, mb: 3 }}>
        <Typography variant="h3" gutterBottom>
          {currentCourse.title}
        </Typography>
        <Box sx={{ mb: 2 }}>
          <Chip label={currentCourse.difficulty} sx={{ mr: 1 }} />
          <Chip label={currentCourse.category} variant="outlined" />
        </Box>
        <Typography variant="body1" paragraph>
          {currentCourse.description}
        </Typography>
        <Typography variant="body2" color="text.secondary" gutterBottom>
          Instructor: {currentCourse.instructor?.full_name}
        </Typography>
        <Typography variant="body2" color="text.secondary" gutterBottom>
          Duration: {currentCourse.estimated_duration} hours • {currentCourse.total_lessons} lessons
        </Typography>
        <Button variant="contained" size="large" sx={{ mt: 2 }} onClick={handleEnroll}>
          Enroll Now
        </Button>
      </Paper>

      <Paper sx={{ p: 3 }}>
        <Typography variant="h5" gutterBottom>
          Course Content
        </Typography>
        <List>
          {currentCourse.lessons?.map((lesson, index) => (
            <ListItem key={lesson.id} divider>
              <PlayCircleOutline sx={{ mr: 2, color: 'primary.main' }} />
              <ListItemText
                primary={`${index + 1}. ${lesson.title}`}
                secondary={`${lesson.duration} minutes`}
              />
            </ListItem>
          ))}
        </List>
      </Paper>
    </Box>
  );
};

export default CourseDetail;