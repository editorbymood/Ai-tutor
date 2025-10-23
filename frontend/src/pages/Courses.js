import React, { useEffect, useState } from 'react';
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
  Paper,
  Stack,
  TextField,
  InputAdornment,
  ToggleButtonGroup,
  ToggleButton,
} from '@mui/material';
import { School, Search, FilterList, Star, AccessTime, Person, TrendingUp } from '@mui/icons-material';
import { fetchCourses } from '../redux/slices/coursesSlice';

const Courses = () => {
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const { courses, loading } = useSelector((state) => state.courses);
  const [searchQuery, setSearchQuery] = useState('');
  const [filterDifficulty, setFilterDifficulty] = useState('all');

  useEffect(() => {
    dispatch(fetchCourses());
  }, [dispatch]);

  const difficultyColors = {
    beginner: { bg: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)', text: '#4facfe' },
    intermediate: { bg: 'linear-gradient(135deg, #fa709a 0%, #fee140 100%)', text: '#fa709a' },
    advanced: { bg: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)', text: '#f093fb' },
  };

  const filteredCourses = courses?.filter((course) => {
    const matchesSearch = course.title.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesDifficulty = filterDifficulty === 'all' || course.difficulty === filterDifficulty;
    return matchesSearch && matchesDifficulty;
  });

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box className="fade-in">
      {/* Header */}
      <Paper
        sx={{
          p: 4,
          mb: 4,
          borderRadius: '24px',
          background: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
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
          <Typography variant="h3" sx={{ fontWeight: 800, mb: 1 }}>
            Explore Courses 📚
          </Typography>
          <Typography variant="h6" sx={{ opacity: 0.9, mb: 3 }}>
            Discover and enroll in courses tailored to your learning journey
          </Typography>

          {/* Search and Filter */}
          <Stack direction={{ xs: 'column', md: 'row' }} spacing={2}>
            <TextField
              fullWidth
              placeholder="Search courses..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              InputProps={{
                startAdornment: (
                  <InputAdornment position="start">
                    <Search sx={{ color: 'white' }} />
                  </InputAdornment>
                ),
              }}
              sx={{
                '& .MuiOutlinedInput-root': {
                  borderRadius: '16px',
                  background: 'rgba(255, 255, 255, 0.2)',
                  color: 'white',
                  '& fieldset': {
                    borderColor: 'rgba(255, 255, 255, 0.3)',
                  },
                  '&:hover fieldset': {
                    borderColor: 'rgba(255, 255, 255, 0.5)',
                  },
                  '&.Mui-focused fieldset': {
                    borderColor: 'white',
                  },
                },
                '& .MuiInputBase-input::placeholder': {
                  color: 'rgba(255, 255, 255, 0.8)',
                  opacity: 1,
                },
              }}
            />
            <ToggleButtonGroup
              value={filterDifficulty}
              exclusive
              onChange={(e, value) => value && setFilterDifficulty(value)}
              sx={{
                background: 'rgba(255, 255, 255, 0.2)',
                borderRadius: '16px',
                '& .MuiToggleButton-root': {
                  color: 'white',
                  border: 'none',
                  px: 3,
                  '&.Mui-selected': {
                    background: 'white',
                    color: '#4facfe',
                    fontWeight: 700,
                    '&:hover': {
                      background: 'rgba(255, 255, 255, 0.9)',
                    },
                  },
                },
              }}
            >
              <ToggleButton value="all">All</ToggleButton>
              <ToggleButton value="beginner">Beginner</ToggleButton>
              <ToggleButton value="intermediate">Intermediate</ToggleButton>
              <ToggleButton value="advanced">Advanced</ToggleButton>
            </ToggleButtonGroup>
          </Stack>
        </Box>
      </Paper>

      {loading ? (
        <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '50vh' }}>
          <Box sx={{ textAlign: 'center' }}>
            <CircularProgress size={60} sx={{ color: '#4facfe', mb: 2 }} />
            <Typography color="text.secondary">Loading courses...</Typography>
          </Box>
        </Box>
      ) : (
        <Grid container spacing={3}>
          {filteredCourses && filteredCourses.length > 0 ? (
            filteredCourses.map((course) => (
              <Grid item xs={12} sm={6} md={4} key={course.id}>
                <Card
                  className="hover-lift"
                  sx={{
                    height: '100%',
                    display: 'flex',
                    flexDirection: 'column',
                    borderRadius: '24px',
                    overflow: 'hidden',
                    border: '1px solid rgba(0, 0, 0, 0.08)',
                    transition: 'all 0.3s ease',
                    '&:hover': {
                      borderColor: '#4facfe',
                    },
                  }}
                >
                  {/* Course Image/Icon */}
                  <Box
                    sx={{
                      height: 200,
                      background: difficultyColors[course.difficulty]?.bg || 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      position: 'relative',
                    }}
                  >
                    <School sx={{ fontSize: 80, color: 'white', opacity: 0.9 }} />
                    <Chip
                      label={course.difficulty}
                      size="small"
                      sx={{
                        position: 'absolute',
                        top: 16,
                        right: 16,
                        background: 'white',
                        color: difficultyColors[course.difficulty]?.text || '#667eea',
                        fontWeight: 700,
                        textTransform: 'capitalize',
                      }}
                    />
                  </Box>

                  <CardContent sx={{ flexGrow: 1, p: 3 }}>
                    <Typography
                      variant="h6"
                      sx={{
                        fontWeight: 700,
                        mb: 2,
                        overflow: 'hidden',
                        textOverflow: 'ellipsis',
                        display: '-webkit-box',
                        WebkitLineClamp: 2,
                        WebkitBoxOrient: 'vertical',
                      }}
                    >
                      {course.title}
                    </Typography>
                    <Typography
                      variant="body2"
                      color="text.secondary"
                      sx={{
                        mb: 3,
                        overflow: 'hidden',
                        textOverflow: 'ellipsis',
                        display: '-webkit-box',
                        WebkitLineClamp: 3,
                        WebkitBoxOrient: 'vertical',
                        lineHeight: 1.6,
                      }}
                    >
                      {course.description || 'No description available'}
                    </Typography>

                    {/* Course Info */}
                    <Stack direction="row" spacing={1} sx={{ mb: 3 }} flexWrap="wrap">
                      <Chip
                        icon={<School />}
                        label={course.category || 'General'}
                        size="small"
                        sx={{
                          background: 'rgba(79, 172, 254, 0.1)',
                          color: '#4facfe',
                          '& .MuiChip-icon': { color: '#4facfe' },
                        }}
                      />
                      <Chip
                        icon={<AccessTime />}
                        label={`${course.estimated_duration || 0}h`}
                        size="small"
                        sx={{
                          background: 'rgba(250, 112, 154, 0.1)',
                          color: '#fa709a',
                          '& .MuiChip-icon': { color: '#fa709a' },
                        }}
                      />
                    </Stack>

                    <Stack direction="row" spacing={2} alignItems="center" sx={{ mb: 2 }}>
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
                        <Star sx={{ fontSize: 18, color: '#fee140' }} />
                        <Typography variant="body2" sx={{ fontWeight: 600 }}>
                          4.8
                        </Typography>
                      </Box>
                      <Typography variant="body2" color="text.secondary">
                        •
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        {course.total_lessons || 0} lessons
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        •
                      </Typography>
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
                        <Person sx={{ fontSize: 16, color: 'text.secondary' }} />
                        <Typography variant="body2" color="text.secondary">
                          {course.instructor?.full_name || 'Expert'}
                        </Typography>
                      </Box>
                    </Stack>
                  </CardContent>

                  <Box sx={{ p: 3, pt: 0 }}>
                    <Button
                      fullWidth
                      variant="contained"
                      onClick={() => navigate(`/courses/${course.id}`)}
                      sx={{
                        py: 1.5,
                        borderRadius: '12px',
                        fontWeight: 700,
                        textTransform: 'none',
                        background: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
                        boxShadow: '0 4px 12px rgba(79, 172, 254, 0.3)',
                        '&:hover': {
                          background: 'linear-gradient(135deg, #3e9be6 0%, #00d9e6 100%)',
                          transform: 'translateY(-2px)',
                          boxShadow: '0 6px 16px rgba(79, 172, 254, 0.4)',
                        },
                        transition: 'all 0.3s ease',
                      }}
                    >
                      View Course
                    </Button>
                  </Box>
                </Card>
              </Grid>
            ))
          ) : (
            <Grid item xs={12}>
              <Box sx={{ textAlign: 'center', py: 12 }}>
                <Box
                  sx={{
                    width: 120,
                    height: 120,
                    borderRadius: '32px',
                    background: 'linear-gradient(135deg, rgba(79, 172, 254, 0.1) 0%, rgba(0, 242, 254, 0.1) 100%)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    mx: 'auto',
                    mb: 3,
                  }}
                >
                  <School sx={{ fontSize: 64, color: '#4facfe' }} />
                </Box>
                <Typography variant="h5" sx={{ fontWeight: 700, mb: 1 }}>
                  {searchQuery ? 'No courses found' : 'No courses available'}
                </Typography>
                <Typography variant="body1" color="text.secondary" sx={{ mb: 4 }}>
                  {searchQuery
                    ? 'Try adjusting your search or filters'
                    : 'Check back later for new courses!'}
                </Typography>
                {searchQuery && (
                  <Button
                    variant="outlined"
                    onClick={() => {
                      setSearchQuery('');
                      setFilterDifficulty('all');
                    }}
                    sx={{
                      borderRadius: '12px',
                      px: 4,
                      borderColor: '#4facfe',
                      color: '#4facfe',
                    }}
                  >
                    Clear Filters
                  </Button>
                )}
              </Box>
            </Grid>
          )}
        </Grid>
      )}
    </Box>
  );
};

export default Courses;