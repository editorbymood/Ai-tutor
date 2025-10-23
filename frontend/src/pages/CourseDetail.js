import React, { useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
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
  Stack,
  Avatar,
  Divider,
  LinearProgress,
  Grid,
  Card,
  CardContent,
} from '@mui/material';
import {
  PlayCircleOutline,
  School,
  AccessTime,
  Person,
  Star,
  CheckCircle,
  EmojiEvents,
  TrendingUp,
  Lock,
} from '@mui/icons-material';
import { fetchCourseDetail, enrollCourse } from '../redux/slices/coursesSlice';

const CourseDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
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
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '70vh' }}>
        <Box sx={{ textAlign: 'center' }}>
          <CircularProgress size={60} sx={{ color: '#667eea', mb: 2 }} />
          <Typography color="text.secondary">Loading course details...</Typography>
        </Box>
      </Box>
    );
  }

  if (!currentCourse) return null;

  const difficultyColors = {
    beginner: '#4facfe',
    intermediate: '#fa709a',
    advanced: '#f093fb',
  };

  return (
    <Box className="fade-in">
      {/* Hero Section */}
      <Paper
        sx={{
          p: 5,
          mb: 4,
          borderRadius: '32px',
          background: `linear-gradient(135deg, ${difficultyColors[currentCourse.difficulty] || '#667eea'} 0%, #764ba2 100%)`,
          color: 'white',
          position: 'relative',
          overflow: 'hidden',
        }}
      >
        <Box
          sx={{
            position: 'absolute',
            top: -100,
            right: -100,
            width: 300,
            height: 300,
            borderRadius: '50%',
            background: 'rgba(255, 255, 255, 0.1)',
            filter: 'blur(60px)',
          }}
        />
        <Box sx={{ position: 'relative', zIndex: 1 }}>
          <Stack direction="row" spacing={2} sx={{ mb: 3 }}>
            <Chip
              label={currentCourse.difficulty}
              sx={{
                background: 'rgba(255, 255, 255, 0.2)',
                color: 'white',
                fontWeight: 700,
                textTransform: 'capitalize',
              }}
            />
            <Chip
              label={currentCourse.category}
              variant="outlined"
              sx={{
                borderColor: 'rgba(255, 255, 255, 0.5)',
                color: 'white',
                fontWeight: 600,
              }}
            />
          </Stack>

          <Typography variant="h2" sx={{ fontWeight: 900, mb: 2 }}>
            {currentCourse.title}
          </Typography>
          
          <Typography variant="h6" sx={{ mb: 4, opacity: 0.95, lineHeight: 1.6 }}>
            {currentCourse.description}
          </Typography>

          <Grid container spacing={4} sx={{ mb: 4 }}>
            <Grid item xs={12} sm={6} md={3}>
              <Stack direction="row" spacing={1.5} alignItems="center">
                <Avatar
                  sx={{
                    width: 48,
                    height: 48,
                    background: 'rgba(255, 255, 255, 0.2)',
                  }}
                >
                  <Person />
                </Avatar>
                <Box>
                  <Typography variant="caption" sx={{ opacity: 0.8 }}>
                    Instructor
                  </Typography>
                  <Typography variant="body1" sx={{ fontWeight: 700 }}>
                    {currentCourse.instructor?.full_name || 'Expert Teacher'}
                  </Typography>
                </Box>
              </Stack>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <Stack direction="row" spacing={1.5} alignItems="center">
                <Avatar
                  sx={{
                    width: 48,
                    height: 48,
                    background: 'rgba(255, 255, 255, 0.2)',
                  }}
                >
                  <AccessTime />
                </Avatar>
                <Box>
                  <Typography variant="caption" sx={{ opacity: 0.8 }}>
                    Duration
                  </Typography>
                  <Typography variant="body1" sx={{ fontWeight: 700 }}>
                    {currentCourse.estimated_duration} hours
                  </Typography>
                </Box>
              </Stack>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <Stack direction="row" spacing={1.5} alignItems="center">
                <Avatar
                  sx={{
                    width: 48,
                    height: 48,
                    background: 'rgba(255, 255, 255, 0.2)',
                  }}
                >
                  <School />
                </Avatar>
                <Box>
                  <Typography variant="caption" sx={{ opacity: 0.8 }}>
                    Lessons
                  </Typography>
                  <Typography variant="body1" sx={{ fontWeight: 700 }}>
                    {currentCourse.total_lessons} lessons
                  </Typography>
                </Box>
              </Stack>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <Stack direction="row" spacing={1.5} alignItems="center">
                <Avatar
                  sx={{
                    width: 48,
                    height: 48,
                    background: 'rgba(255, 255, 255, 0.2)',
                  }}
                >
                  <Star sx={{ color: '#fee140' }} />
                </Avatar>
                <Box>
                  <Typography variant="caption" sx={{ opacity: 0.8 }}>
                    Rating
                  </Typography>
                  <Typography variant="body1" sx={{ fontWeight: 700 }}>
                    4.8 (1,234)
                  </Typography>
                </Box>
              </Stack>
            </Grid>
          </Grid>

          <Button
            variant="contained"
            size="large"
            onClick={handleEnroll}
            startIcon={<CheckCircle />}
            sx={{
              px: 6,
              py: 2,
              borderRadius: '16px',
              background: 'white',
              color: difficultyColors[currentCourse.difficulty] || '#667eea',
              fontWeight: 700,
              fontSize: '1.1rem',
              textTransform: 'none',
              boxShadow: '0 8px 24px rgba(0, 0, 0, 0.2)',
              '&:hover': {
                background: 'rgba(255, 255, 255, 0.95)',
                transform: 'translateY(-2px)',
                boxShadow: '0 12px 32px rgba(0, 0, 0, 0.3)',
              },
              transition: 'all 0.3s ease',
            }}
          >
            Enroll Now - Free
          </Button>
        </Box>
      </Paper>

      {/* Stats Cards */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} md={4}>
          <Card
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
                  <Typography variant="h4" sx={{ fontWeight: 800, color: '#4facfe' }}>
                    2,345
                  </Typography>
                  <Typography variant="body2" color="text.secondary" sx={{ fontWeight: 600 }}>
                    Students Enrolled
                  </Typography>
                </Box>
              </Stack>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={4}>
          <Card
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
                    width: 56,
                    height: 56,
                    borderRadius: '12px',
                    background: 'linear-gradient(135deg, #fa709a 0%, #fee140 100%)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    color: 'white',
                  }}
                >
                  <EmojiEvents sx={{ fontSize: 28 }} />
                </Box>
                <Box>
                  <Typography variant="h4" sx={{ fontWeight: 800, color: '#fa709a' }}>
                    89%
                  </Typography>
                  <Typography variant="body2" color="text.secondary" sx={{ fontWeight: 600 }}>
                    Completion Rate
                  </Typography>
                </Box>
              </Stack>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={4}>
          <Card
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
                  <CheckCircle sx={{ fontSize: 28 }} />
                </Box>
                <Box>
                  <Typography variant="h4" sx={{ fontWeight: 800, color: '#667eea' }}>
                    1,890
                  </Typography>
                  <Typography variant="body2" color="text.secondary" sx={{ fontWeight: 600 }}>
                    Certificates Issued
                  </Typography>
                </Box>
              </Stack>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Course Content */}
      <Paper
        sx={{
          p: 4,
          borderRadius: '24px',
          background: 'white',
          boxShadow: '0 4px 20px rgba(0, 0, 0, 0.08)',
        }}
      >
        <Typography variant="h4" sx={{ fontWeight: 700, mb: 1 }}>
          Course Content
        </Typography>
        <Typography variant="body1" color="text.secondary" sx={{ mb: 4 }}>
          {currentCourse.lessons?.length || 0} lessons • {currentCourse.estimated_duration} hours total
        </Typography>

        <List sx={{ p: 0 }}>
          {currentCourse.lessons?.map((lesson, index) => (
            <Paper
              key={lesson.id}
              sx={{
                mb: 2,
                borderRadius: '16px',
                overflow: 'hidden',
                border: '1px solid rgba(0, 0, 0, 0.08)',
                transition: 'all 0.3s ease',
                '&:hover': {
                  borderColor: difficultyColors[currentCourse.difficulty] || '#667eea',
                  boxShadow: '0 4px 12px rgba(0, 0, 0, 0.1)',
                },
              }}
            >
              <ListItem
                sx={{
                  p: 3,
                  cursor: 'pointer',
                }}
              >
                <Box
                  sx={{
                    width: 48,
                    height: 48,
                    borderRadius: '12px',
                    background: `linear-gradient(135deg, ${difficultyColors[currentCourse.difficulty] || '#667eea'} 0%, #764ba2 100%)`,
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    color: 'white',
                    mr: 2,
                    fontSize: '1.2rem',
                    fontWeight: 700,
                  }}
                >
                  {index + 1}
                </Box>
                <ListItemText
                  primary={
                    <Typography variant="h6" sx={{ fontWeight: 700, mb: 0.5 }}>
                      {lesson.title}
                    </Typography>
                  }
                  secondary={
                    <Stack direction="row" spacing={2} alignItems="center" sx={{ mt: 1 }}>
                      <Chip
                        icon={<AccessTime />}
                        label={`${lesson.duration} min`}
                        size="small"
                        sx={{
                          background: 'rgba(0, 0, 0, 0.05)',
                          '& .MuiChip-icon': { color: 'text.secondary' },
                        }}
                      />
                      <Chip
                        icon={<PlayCircleOutline />}
                        label="Video"
                        size="small"
                        sx={{
                          background: 'rgba(0, 0, 0, 0.05)',
                          '& .MuiChip-icon': { color: 'text.secondary' },
                        }}
                      />
                    </Stack>
                  }
                />
                <Lock sx={{ color: 'text.disabled', fontSize: 24 }} />
              </ListItem>
            </Paper>
          ))}
        </List>

        {!currentCourse.lessons || currentCourse.lessons.length === 0 && (
          <Box sx={{ textAlign: 'center', py: 8 }}>
            <School sx={{ fontSize: 80, color: 'text.disabled', mb: 2 }} />
            <Typography variant="h6" color="text.secondary">
              Course content will be available after enrollment
            </Typography>
          </Box>
        )}
      </Paper>
    </Box>
  );
};

export default CourseDetail;