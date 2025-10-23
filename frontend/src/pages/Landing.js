import React from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  Container,
  Typography,
  Button,
  Grid,
  Card,
  CardContent,
  Avatar,
  Chip,
  Paper,
  Stack,
} from '@mui/material';
import {
  AutoAwesome,
  School,
  Psychology,
  TrendingUp,
  EmojiEvents,
  Speed,
  Star,
  Rocket,
  CheckCircle,
  ArrowForward,
  PlayArrow,
} from '@mui/icons-material';

const Landing = () => {
  const navigate = useNavigate();

  const features = [
    {
      icon: <Psychology />,
      title: 'AI-Powered Learning',
      description: 'Personalized tutoring adapted to your unique learning style',
      gradient: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    },
    {
      icon: <School />,
      title: 'Expert Courses',
      description: 'Access premium courses taught by industry professionals',
      gradient: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
    },
    {
      icon: <TrendingUp />,
      title: 'Track Progress',
      description: 'Real-time analytics to monitor your learning journey',
      gradient: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
    },
    {
      icon: <EmojiEvents />,
      title: 'Gamification',
      description: 'Earn badges, XP, and compete on leaderboards',
      gradient: 'linear-gradient(135deg, #fa709a 0%, #fee140 100%)',
    },
    {
      icon: <Speed />,
      title: 'Fast Learning',
      description: 'Learn 3x faster with our adaptive AI technology',
      gradient: 'linear-gradient(135deg, #30cfd0 0%, #330867 100%)',
    },
    {
      icon: <AutoAwesome />,
      title: 'Smart Recommendations',
      description: 'Get personalized study plans and content suggestions',
      gradient: 'linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)',
    },
  ];

  const stats = [
    { value: '50K+', label: 'Active Students' },
    { value: '1000+', label: 'Courses' },
    { value: '95%', label: 'Success Rate' },
    { value: '24/7', label: 'AI Support' },
  ];

  const testimonials = [
    {
      name: 'Sarah Johnson',
      role: 'Computer Science Student',
      avatar: '👩‍💻',
      text: 'This AI tutor helped me ace my exams! The personalized learning approach is incredible.',
      rating: 5,
    },
    {
      name: 'Michael Chen',
      role: 'Professional Developer',
      avatar: '👨‍💼',
      text: 'Best investment in my career. The courses are top-notch and the AI guidance is spot-on.',
      rating: 5,
    },
    {
      name: 'Emily Rodriguez',
      role: 'High School Student',
      avatar: '👩‍🎓',
      text: 'Learning has never been this fun! I love the gamification and the AI tutor is like having a personal teacher.',
      rating: 5,
    },
  ];

  return (
    <Box sx={{ minHeight: '100vh', overflow: 'hidden' }}>
      {/* Floating Auth Buttons - Top Right Corner */}
      <Box
        sx={{
          position: 'fixed',
          top: 24,
          right: 24,
          zIndex: 1100,
          display: 'flex',
          gap: 2,
        }}
        className="scale-in"
      >
        <Button
          variant="outlined"
          onClick={() => navigate('/login')}
          sx={{
            borderRadius: '12px',
            px: 3,
            py: 1.5,
            border: '2px solid',
            borderColor: 'rgba(255, 255, 255, 0.3)',
            color: 'white',
            fontWeight: 600,
            background: 'rgba(255, 255, 255, 0.1)',
            backdropFilter: 'blur(10px)',
            '&:hover': {
              borderColor: 'white',
              background: 'rgba(255, 255, 255, 0.2)',
              transform: 'translateY(-2px)',
              boxShadow: '0 8px 24px rgba(0, 0, 0, 0.2)',
            },
            transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
          }}
        >
          Log In
        </Button>
        <Button
          variant="contained"
          onClick={() => navigate('/register')}
          sx={{
            borderRadius: '12px',
            px: 3,
            py: 1.5,
            background: 'white',
            color: '#667eea',
            fontWeight: 700,
            boxShadow: '0 8px 24px rgba(255, 255, 255, 0.3)',
            '&:hover': {
              background: 'white',
              transform: 'translateY(-2px) scale(1.05)',
              boxShadow: '0 12px 32px rgba(255, 255, 255, 0.4)',
            },
            transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
          }}
        >
          Sign Up Free
        </Button>
      </Box>

      {/* Hero Section */}
      <Box
        sx={{
          position: 'relative',
          minHeight: '100vh',
          display: 'flex',
          alignItems: 'center',
          pt: 8,
          pb: 12,
        }}
      >
        {/* Animated Background Orbs */}
        <Box
          sx={{
            position: 'absolute',
            top: '10%',
            left: '10%',
            width: '400px',
            height: '400px',
            borderRadius: '50%',
            background: 'radial-gradient(circle, rgba(102, 126, 234, 0.3) 0%, transparent 70%)',
            filter: 'blur(60px)',
            animation: 'float 8s ease-in-out infinite',
          }}
        />
        <Box
          sx={{
            position: 'absolute',
            top: '60%',
            right: '5%',
            width: '500px',
            height: '500px',
            borderRadius: '50%',
            background: 'radial-gradient(circle, rgba(240, 147, 251, 0.3) 0%, transparent 70%)',
            filter: 'blur(60px)',
            animation: 'float 10s ease-in-out infinite reverse',
          }}
        />

        <Container maxWidth="lg" sx={{ position: 'relative', zIndex: 1 }}>
          <Grid container spacing={6} alignItems="center">
            {/* Left: Hero Content */}
            <Grid item xs={12} md={6}>
              <Box className="slide-up">
                <Chip
                  icon={<Star />}
                  label="🎉 #1 AI Learning Platform"
                  sx={{
                    mb: 3,
                    px: 2,
                    py: 2.5,
                    fontSize: '0.9rem',
                    fontWeight: 600,
                    background: 'rgba(255, 255, 255, 0.15)',
                    backdropFilter: 'blur(10px)',
                    border: '1px solid rgba(255, 255, 255, 0.2)',
                    color: 'white',
                    '& .MuiChip-icon': { color: '#fee140' },
                  }}
                />

                <Typography
                  variant="h1"
                  sx={{
                    fontSize: { xs: '2.5rem', md: '4rem' },
                    fontWeight: 900,
                    lineHeight: 1.1,
                    mb: 3,
                    background: 'linear-gradient(135deg, #ffffff 0%, #f0f0f0 100%)',
                    WebkitBackgroundClip: 'text',
                    WebkitTextFillColor: 'transparent',
                    letterSpacing: '-0.02em',
                  }}
                >
                  Learn Smarter,
                  <br />
                  Not Harder
                </Typography>

                <Typography
                  variant="h5"
                  sx={{
                    mb: 4,
                    color: 'rgba(255, 255, 255, 0.9)',
                    lineHeight: 1.6,
                    fontSize: { xs: '1.1rem', md: '1.3rem' },
                  }}
                >
                  Experience the future of education with AI-powered personalized learning.
                  Master any subject 3x faster with our adaptive technology.
                </Typography>

                <Stack direction={{ xs: 'column', sm: 'row' }} spacing={2} sx={{ mb: 4 }}>
                  <Button
                    variant="contained"
                    size="large"
                    endIcon={<Rocket />}
                    onClick={() => navigate('/register')}
                    sx={{
                      px: 4,
                      py: 2,
                      fontSize: '1.1rem',
                      borderRadius: '16px',
                      background: 'white',
                      color: '#667eea',
                      fontWeight: 700,
                      boxShadow: '0 8px 32px rgba(255, 255, 255, 0.4)',
                      '&:hover': {
                        background: 'white',
                        transform: 'translateY(-4px)',
                        boxShadow: '0 12px 48px rgba(255, 255, 255, 0.5)',
                      },
                      transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
                    }}
                  >
                    Start Learning Free
                  </Button>

                  <Button
                    variant="outlined"
                    size="large"
                    endIcon={<PlayArrow />}
                    sx={{
                      px: 4,
                      py: 2,
                      fontSize: '1.1rem',
                      borderRadius: '16px',
                      border: '2px solid rgba(255, 255, 255, 0.3)',
                      color: 'white',
                      fontWeight: 600,
                      background: 'rgba(255, 255, 255, 0.1)',
                      backdropFilter: 'blur(10px)',
                      '&:hover': {
                        borderColor: 'white',
                        background: 'rgba(255, 255, 255, 0.2)',
                        transform: 'translateY(-4px)',
                      },
                      transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
                    }}
                  >
                    Watch Demo
                  </Button>
                </Stack>

                <Stack direction="row" spacing={3} alignItems="center">
                  {[1, 2, 3, 4, 5].map((i) => (
                    <Avatar
                      key={i}
                      sx={{
                        width: 40,
                        height: 40,
                        border: '3px solid rgba(255, 255, 255, 0.3)',
                        ml: i > 1 ? -2 : 0,
                        background: `linear-gradient(135deg, hsl(${i * 60}, 70%, 60%), hsl(${i * 60 + 30}, 70%, 50%))`,
                      }}
                    />
                  ))}
                  <Typography sx={{ color: 'rgba(255, 255, 255, 0.8)', fontWeight: 600 }}>
                    Join 50,000+ students
                  </Typography>
                </Stack>
              </Box>
            </Grid>

            {/* Right: 3D Illustration / Stats */}
            <Grid item xs={12} md={6}>
              <Box
                className="scale-in"
                sx={{
                  position: 'relative',
                  height: '500px',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                }}
              >
                {/* Floating Stats Cards */}
                {stats.map((stat, index) => (
                  <Paper
                    key={index}
                    className="glass hover-lift"
                    sx={{
                      position: 'absolute',
                      p: 3,
                      borderRadius: '20px',
                      textAlign: 'center',
                      minWidth: '140px',
                      animation: `float ${3 + index * 0.5}s ease-in-out infinite`,
                      animationDelay: `${index * 0.2}s`,
                      top: index === 0 ? '10%' : index === 1 ? '20%' : index === 2 ? '60%' : '70%',
                      left: index === 0 ? '60%' : index === 1 ? '10%' : index === 2 ? '65%' : '15%',
                      background: 'rgba(255, 255, 255, 0.15)',
                      backdropFilter: 'blur(20px)',
                      border: '1px solid rgba(255, 255, 255, 0.3)',
                    }}
                  >
                    <Typography
                      variant="h4"
                      sx={{
                        fontWeight: 900,
                        background: 'linear-gradient(135deg, #ffffff 0%, #f0f0f0 100%)',
                        WebkitBackgroundClip: 'text',
                        WebkitTextFillColor: 'transparent',
                      }}
                    >
                      {stat.value}
                    </Typography>
                    <Typography sx={{ color: 'rgba(255, 255, 255, 0.8)', fontWeight: 600, mt: 1 }}>
                      {stat.label}
                    </Typography>
                  </Paper>
                ))}

                {/* Central Glow */}
                <Box
                  sx={{
                    width: '250px',
                    height: '250px',
                    borderRadius: '50%',
                    background: 'radial-gradient(circle, rgba(255, 255, 255, 0.3) 0%, transparent 70%)',
                    filter: 'blur(40px)',
                    animation: 'pulse 3s ease-in-out infinite',
                  }}
                />
              </Box>
            </Grid>
          </Grid>
        </Container>
      </Box>

      {/* Features Section */}
      <Container maxWidth="lg" sx={{ py: 12, position: 'relative', zIndex: 1 }}>
        <Box sx={{ textAlign: 'center', mb: 8 }} className="fade-in">
          <Typography
            variant="h2"
            sx={{
              fontSize: { xs: '2rem', md: '3rem' },
              fontWeight: 800,
              mb: 2,
              color: 'white',
            }}
          >
            Why Choose AI Tutor?
          </Typography>
          <Typography variant="h6" sx={{ color: 'rgba(255, 255, 255, 0.8)', maxWidth: '700px', mx: 'auto' }}>
            Revolutionary learning experience powered by cutting-edge AI technology
          </Typography>
        </Box>

        <Grid container spacing={4}>
          {features.map((feature, index) => (
            <Grid item xs={12} sm={6} md={4} key={index}>
              <Card
                className="glass hover-lift scale-in"
                sx={{
                  height: '100%',
                  borderRadius: '24px',
                  background: 'rgba(255, 255, 255, 0.1)',
                  backdropFilter: 'blur(20px)',
                  border: '1px solid rgba(255, 255, 255, 0.2)',
                  transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
                  '&:hover': {
                    transform: 'translateY(-12px)',
                    boxShadow: '0 20px 60px rgba(0, 0, 0, 0.3)',
                  },
                  animationDelay: `${index * 0.1}s`,
                }}
              >
                <CardContent sx={{ p: 4 }}>
                  <Box
                    sx={{
                      width: 64,
                      height: 64,
                      borderRadius: '16px',
                      background: feature.gradient,
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      mb: 3,
                      color: 'white',
                      fontSize: 32,
                      boxShadow: '0 8px 24px rgba(0, 0, 0, 0.2)',
                    }}
                  >
                    {feature.icon}
                  </Box>
                  <Typography variant="h5" sx={{ fontWeight: 700, mb: 2, color: 'white' }}>
                    {feature.title}
                  </Typography>
                  <Typography sx={{ color: 'rgba(255, 255, 255, 0.8)', lineHeight: 1.7 }}>
                    {feature.description}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Container>

      {/* Testimonials Section */}
      <Container maxWidth="lg" sx={{ py: 12, position: 'relative', zIndex: 1 }}>
        <Box sx={{ textAlign: 'center', mb: 8 }}>
          <Typography
            variant="h2"
            sx={{
              fontSize: { xs: '2rem', md: '3rem' },
              fontWeight: 800,
              mb: 2,
              color: 'white',
            }}
          >
            Loved by Students Worldwide
          </Typography>
          <Typography variant="h6" sx={{ color: 'rgba(255, 255, 255, 0.8)' }}>
            See what our community has to say
          </Typography>
        </Box>

        <Grid container spacing={4}>
          {testimonials.map((testimonial, index) => (
            <Grid item xs={12} md={4} key={index}>
              <Card
                className="glass hover-lift"
                sx={{
                  height: '100%',
                  borderRadius: '24px',
                  background: 'rgba(255, 255, 255, 0.1)',
                  backdropFilter: 'blur(20px)',
                  border: '1px solid rgba(255, 255, 255, 0.2)',
                }}
              >
                <CardContent sx={{ p: 4 }}>
                  <Box sx={{ display: 'flex', mb: 2 }}>
                    {[...Array(testimonial.rating)].map((_, i) => (
                      <Star key={i} sx={{ color: '#fee140', fontSize: 20 }} />
                    ))}
                  </Box>
                  <Typography sx={{ color: 'rgba(255, 255, 255, 0.9)', mb: 3, lineHeight: 1.7, fontStyle: 'italic' }}>
                    "{testimonial.text}"
                  </Typography>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                    <Box
                      sx={{
                        fontSize: 40,
                        width: 56,
                        height: 56,
                        borderRadius: '50%',
                        background: 'rgba(255, 255, 255, 0.2)',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                      }}
                    >
                      {testimonial.avatar}
                    </Box>
                    <Box>
                      <Typography sx={{ fontWeight: 700, color: 'white' }}>
                        {testimonial.name}
                      </Typography>
                      <Typography sx={{ fontSize: '0.875rem', color: 'rgba(255, 255, 255, 0.7)' }}>
                        {testimonial.role}
                      </Typography>
                    </Box>
                  </Box>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Container>

      {/* CTA Section */}
      <Container maxWidth="md" sx={{ py: 12, position: 'relative', zIndex: 1 }}>
        <Paper
          className="glass glow"
          sx={{
            borderRadius: '32px',
            p: { xs: 4, md: 8 },
            textAlign: 'center',
            background: 'rgba(255, 255, 255, 0.15)',
            backdropFilter: 'blur(20px)',
            border: '1px solid rgba(255, 255, 255, 0.3)',
          }}
        >
          <Typography
            variant="h2"
            sx={{
              fontSize: { xs: '2rem', md: '3rem' },
              fontWeight: 900,
              mb: 3,
              color: 'white',
            }}
          >
            Ready to Transform Your Learning?
          </Typography>
          <Typography
            variant="h6"
            sx={{
              mb: 4,
              color: 'rgba(255, 255, 255, 0.9)',
              maxWidth: '600px',
              mx: 'auto',
            }}
          >
            Join thousands of students already learning smarter with AI-powered education
          </Typography>
          <Button
            variant="contained"
            size="large"
            endIcon={<ArrowForward />}
            onClick={() => navigate('/register')}
            sx={{
              px: 6,
              py: 2.5,
              fontSize: '1.2rem',
              borderRadius: '16px',
              background: 'white',
              color: '#667eea',
              fontWeight: 700,
              boxShadow: '0 12px 48px rgba(255, 255, 255, 0.4)',
              '&:hover': {
                background: 'white',
                transform: 'translateY(-4px) scale(1.05)',
                boxShadow: '0 16px 64px rgba(255, 255, 255, 0.5)',
              },
              transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
            }}
          >
            Get Started Free
          </Button>
          <Typography sx={{ mt: 3, color: 'rgba(255, 255, 255, 0.7)', fontSize: '0.9rem' }}>
            <CheckCircle sx={{ fontSize: 16, verticalAlign: 'middle', mr: 0.5 }} />
            No credit card required • 7-day free trial • Cancel anytime
          </Typography>
        </Paper>
      </Container>

      {/* Footer */}
      <Box
        sx={{
          py: 4,
          textAlign: 'center',
          borderTop: '1px solid rgba(255, 255, 255, 0.1)',
        }}
      >
        <Typography sx={{ color: 'rgba(255, 255, 255, 0.6)' }}>
          © 2024 AI Tutor. Powered by Excellence. All rights reserved.
        </Typography>
      </Box>
    </Box>
  );
};

export default Landing;
