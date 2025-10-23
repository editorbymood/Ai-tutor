import React, { useState } from 'react';
import { useNavigate, Link as RouterLink } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import {
  Container,
  Box,
  Typography,
  TextField,
  Button,
  Link,
  Alert,
  Paper,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  InputAdornment,
  IconButton,
  Divider,
  Stack,
  Chip,
  LinearProgress,
} from '@mui/material';
import {
  Person,
  Email,
  Lock,
  Visibility,
  VisibilityOff,
  PersonAdd,
  School,
  MenuBook,
  ArrowBack,
} from '@mui/icons-material';
import { register, clearError } from '../redux/slices/authSlice';

const Register = () => {
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const { loading, error } = useSelector((state) => state.auth);
  
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    password_confirm: '',
    full_name: '',
    role: 'student',
  });
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [passwordStrength, setPasswordStrength] = useState(0);

  const calculatePasswordStrength = (password) => {
    let strength = 0;
    if (password.length >= 8) strength += 25;
    if (password.match(/[a-z]/) && password.match(/[A-Z]/)) strength += 25;
    if (password.match(/[0-9]/)) strength += 25;
    if (password.match(/[^a-zA-Z0-9]/)) strength += 25;
    return strength;
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
    if (name === 'password') {
      setPasswordStrength(calculatePasswordStrength(value));
    }
    if (error) dispatch(clearError());
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const result = await dispatch(register(formData));
    if (register.fulfilled.match(result)) {
      navigate('/dashboard');
    }
  };

  return (
    <Box
      sx={{
        minHeight: '100vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        position: 'relative',
        overflow: 'hidden',
        py: 4,
      }}
    >
      {/* Animated Background Orbs */}
      <Box
        sx={{
          position: 'absolute',
          top: '-10%',
          right: '-5%',
          width: '500px',
          height: '500px',
          borderRadius: '50%',
          background: 'radial-gradient(circle, rgba(245, 87, 108, 0.2) 0%, transparent 70%)',
          filter: 'blur(60px)',
          animation: 'float 8s ease-in-out infinite',
        }}
      />
      <Box
        sx={{
          position: 'absolute',
          bottom: '-10%',
          left: '-5%',
          width: '500px',
          height: '500px',
          borderRadius: '50%',
          background: 'radial-gradient(circle, rgba(102, 126, 234, 0.2) 0%, transparent 70%)',
          filter: 'blur(60px)',
          animation: 'float 10s ease-in-out infinite reverse',
        }}
      />

      {/* Back to Home Button */}
      <Button
        startIcon={<ArrowBack />}
        onClick={() => navigate('/')}
        sx={{
          position: 'absolute',
          top: 24,
          left: 24,
          color: 'white',
          background: 'rgba(255, 255, 255, 0.1)',
          backdropFilter: 'blur(10px)',
          border: '1px solid rgba(255, 255, 255, 0.2)',
          px: 3,
          py: 1,
          borderRadius: '12px',
          '&:hover': {
            background: 'rgba(255, 255, 255, 0.2)',
          },
        }}
      >
        Home
      </Button>

      <Container component="main" maxWidth="md" sx={{ position: 'relative', zIndex: 1 }}>
        <Paper
          className="glass scale-in"
          elevation={24}
          sx={{
            p: { xs: 3, md: 5 },
            borderRadius: '32px',
            background: 'rgba(255, 255, 255, 0.95)',
            backdropFilter: 'blur(20px)',
            border: '1px solid rgba(255, 255, 255, 0.3)',
            boxShadow: '0 20px 60px rgba(0, 0, 0, 0.3)',
          }}
        >
          {/* Logo/Header */}
          <Box sx={{ textAlign: 'center', mb: 4 }}>
            <Box
              sx={{
                width: 80,
                height: 80,
                mx: 'auto',
                mb: 2,
                borderRadius: '24px',
                background: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                boxShadow: '0 12px 32px rgba(240, 147, 251, 0.4)',
              }}
            >
              <PersonAdd sx={{ fontSize: 40, color: 'white' }} />
            </Box>
            <Typography
              variant="h3"
              sx={{
                fontWeight: 800,
                mb: 1,
                background: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
                WebkitBackgroundClip: 'text',
                WebkitTextFillColor: 'transparent',
                fontFamily: 'Poppins, sans-serif',
              }}
            >
              Join AI Tutor
            </Typography>
            <Typography variant="body1" color="text.secondary">
              Start your personalized learning journey today
            </Typography>
          </Box>

          {error && (
            <Alert
              severity="error"
              sx={{
                mb: 3,
                borderRadius: '16px',
                animation: 'slideUp 0.3s ease-out',
              }}
            >
              {error}
            </Alert>
          )}

          <Box component="form" onSubmit={handleSubmit}>
            <Box sx={{ display: 'grid', gap: 2, gridTemplateColumns: { xs: '1fr', md: '1fr 1fr' } }}>
              {/* Full Name */}
              <TextField
                required
                fullWidth
                id="full_name"
                label="Full Name"
                name="full_name"
                autoFocus
                value={formData.full_name}
                onChange={handleChange}
                InputProps={{
                  startAdornment: (
                    <InputAdornment position="start">
                      <Person color="action" />
                    </InputAdornment>
                  ),
                }}
                sx={{
                  '& .MuiOutlinedInput-root': {
                    borderRadius: '16px',
                    background: 'rgba(255, 255, 255, 0.8)',
                    '&:hover fieldset': {
                      borderColor: '#f093fb',
                    },
                    '&.Mui-focused fieldset': {
                      borderColor: '#f093fb',
                      borderWidth: '2px',
                    },
                  },
                }}
              />

              {/* Email */}
              <TextField
                required
                fullWidth
                id="email"
                label="Email Address"
                name="email"
                autoComplete="email"
                value={formData.email}
                onChange={handleChange}
                InputProps={{
                  startAdornment: (
                    <InputAdornment position="start">
                      <Email color="action" />
                    </InputAdornment>
                  ),
                }}
                sx={{
                  '& .MuiOutlinedInput-root': {
                    borderRadius: '16px',
                    background: 'rgba(255, 255, 255, 0.8)',
                    '&:hover fieldset': {
                      borderColor: '#f093fb',
                    },
                    '&.Mui-focused fieldset': {
                      borderColor: '#f093fb',
                      borderWidth: '2px',
                    },
                  },
                }}
              />
            </Box>

            {/* Role Selection with Cards */}
            <Box sx={{ mt: 3, mb: 2 }}>
              <Typography variant="subtitle2" sx={{ mb: 2, fontWeight: 600 }}>
                I am a:
              </Typography>
              <Stack direction="row" spacing={2}>
                <Paper
                  onClick={() => setFormData({ ...formData, role: 'student' })}
                  sx={{
                    flex: 1,
                    p: 3,
                    borderRadius: '20px',
                    cursor: 'pointer',
                    border: '2px solid',
                    borderColor: formData.role === 'student' ? '#667eea' : 'transparent',
                    background: formData.role === 'student' 
                      ? 'linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%)'
                      : 'rgba(255, 255, 255, 0.5)',
                    transition: 'all 0.3s ease',
                    '&:hover': {
                      transform: 'translateY(-4px)',
                      boxShadow: '0 8px 24px rgba(0, 0, 0, 0.1)',
                    },
                  }}
                >
                  <School
                    sx={{
                      fontSize: 48,
                      color: formData.role === 'student' ? '#667eea' : '#999',
                      mb: 1,
                    }}
                  />
                  <Typography
                    variant="h6"
                    sx={{
                      fontWeight: 700,
                      color: formData.role === 'student' ? '#667eea' : '#666',
                    }}
                  >
                    Student
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Learn with AI
                  </Typography>
                </Paper>

                <Paper
                  onClick={() => setFormData({ ...formData, role: 'teacher' })}
                  sx={{
                    flex: 1,
                    p: 3,
                    borderRadius: '20px',
                    cursor: 'pointer',
                    border: '2px solid',
                    borderColor: formData.role === 'teacher' ? '#f093fb' : 'transparent',
                    background: formData.role === 'teacher'
                      ? 'linear-gradient(135deg, rgba(240, 147, 251, 0.1) 0%, rgba(245, 87, 108, 0.1) 100%)'
                      : 'rgba(255, 255, 255, 0.5)',
                    transition: 'all 0.3s ease',
                    '&:hover': {
                      transform: 'translateY(-4px)',
                      boxShadow: '0 8px 24px rgba(0, 0, 0, 0.1)',
                    },
                  }}
                >
                  <MenuBook
                    sx={{
                      fontSize: 48,
                      color: formData.role === 'teacher' ? '#f093fb' : '#999',
                      mb: 1,
                    }}
                  />
                  <Typography
                    variant="h6"
                    sx={{
                      fontWeight: 700,
                      color: formData.role === 'teacher' ? '#f093fb' : '#666',
                    }}
                  >
                    Teacher
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Teach with AI
                  </Typography>
                </Paper>
              </Stack>
            </Box>

            <Box sx={{ display: 'grid', gap: 2, gridTemplateColumns: { xs: '1fr', md: '1fr 1fr' }, mt: 2 }}>
              {/* Password */}
              <Box>
                <TextField
                  required
                  fullWidth
                  name="password"
                  label="Password"
                  type={showPassword ? 'text' : 'password'}
                  id="password"
                  value={formData.password}
                  onChange={handleChange}
                  InputProps={{
                    startAdornment: (
                      <InputAdornment position="start">
                        <Lock color="action" />
                      </InputAdornment>
                    ),
                    endAdornment: (
                      <InputAdornment position="end">
                        <IconButton
                          onClick={() => setShowPassword(!showPassword)}
                          edge="end"
                        >
                          {showPassword ? <VisibilityOff /> : <Visibility />}
                        </IconButton>
                      </InputAdornment>
                    ),
                  }}
                  sx={{
                    '& .MuiOutlinedInput-root': {
                      borderRadius: '16px',
                      background: 'rgba(255, 255, 255, 0.8)',
                      '&:hover fieldset': {
                        borderColor: '#f093fb',
                      },
                      '&.Mui-focused fieldset': {
                        borderColor: '#f093fb',
                        borderWidth: '2px',
                      },
                    },
                  }}
                />
                {formData.password && (
                  <Box sx={{ mt: 1 }}>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 0.5 }}>
                      <Typography variant="caption" color="text.secondary">
                        Password Strength
                      </Typography>
                      <Typography
                        variant="caption"
                        sx={{
                          color:
                            passwordStrength < 50
                              ? '#f44336'
                              : passwordStrength < 75
                              ? '#ff9800'
                              : '#4caf50',
                          fontWeight: 600,
                        }}
                      >
                        {passwordStrength < 50 ? 'Weak' : passwordStrength < 75 ? 'Medium' : 'Strong'}
                      </Typography>
                    </Box>
                    <LinearProgress
                      variant="determinate"
                      value={passwordStrength}
                      sx={{
                        height: 6,
                        borderRadius: '3px',
                        backgroundColor: 'rgba(0, 0, 0, 0.1)',
                        '& .MuiLinearProgress-bar': {
                          backgroundColor:
                            passwordStrength < 50
                              ? '#f44336'
                              : passwordStrength < 75
                              ? '#ff9800'
                              : '#4caf50',
                          borderRadius: '3px',
                        },
                      }}
                    />
                  </Box>
                )}
              </Box>

              {/* Confirm Password */}
              <TextField
                required
                fullWidth
                name="password_confirm"
                label="Confirm Password"
                type={showConfirmPassword ? 'text' : 'password'}
                id="password_confirm"
                value={formData.password_confirm}
                onChange={handleChange}
                InputProps={{
                  startAdornment: (
                    <InputAdornment position="start">
                      <Lock color="action" />
                    </InputAdornment>
                  ),
                  endAdornment: (
                    <InputAdornment position="end">
                      <IconButton
                        onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                        edge="end"
                      >
                        {showConfirmPassword ? <VisibilityOff /> : <Visibility />}
                      </IconButton>
                    </InputAdornment>
                  ),
                }}
                sx={{
                  '& .MuiOutlinedInput-root': {
                    borderRadius: '16px',
                    background: 'rgba(255, 255, 255, 0.8)',
                    '&:hover fieldset': {
                      borderColor: '#f093fb',
                    },
                    '&.Mui-focused fieldset': {
                      borderColor: '#f093fb',
                      borderWidth: '2px',
                    },
                  },
                }}
              />
            </Box>

            {/* Sign Up Button */}
            <Button
              type="submit"
              fullWidth
              variant="contained"
              size="large"
              disabled={loading}
              sx={{
                mt: 4,
                mb: 2,
                py: 1.5,
                borderRadius: '16px',
                fontSize: '1.1rem',
                fontWeight: 700,
                background: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
                boxShadow: '0 8px 24px rgba(240, 147, 251, 0.4)',
                textTransform: 'none',
                '&:hover': {
                  background: 'linear-gradient(135deg, #e082ea 0%, #e4465b 100%)',
                  boxShadow: '0 12px 32px rgba(240, 147, 251, 0.5)',
                  transform: 'translateY(-2px)',
                },
                '&:disabled': {
                  background: 'linear-gradient(135deg, #ccc 0%, #999 100%)',
                },
                transition: 'all 0.3s ease',
              }}
            >
              {loading ? 'Creating Account...' : 'Create Account'}
            </Button>

            {/* Sign In Link */}
            <Box sx={{ textAlign: 'center' }}>
              <Typography variant="body2" color="text.secondary">
                Already have an account?{' '}
                <Link
                  component={RouterLink}
                  to="/login"
                  sx={{
                    color: '#f093fb',
                    textDecoration: 'none',
                    fontWeight: 700,
                    '&:hover': {
                      textDecoration: 'underline',
                    },
                  }}
                >
                  Sign In
                </Link>
              </Typography>
            </Box>

            {/* Terms */}
            <Typography
              variant="caption"
              color="text.secondary"
              sx={{ display: 'block', textAlign: 'center', mt: 3 }}
            >
              By signing up, you agree to our{' '}
              <Link href="#" sx={{ color: '#f093fb', textDecoration: 'none' }}>
                Terms of Service
              </Link>{' '}
              and{' '}
              <Link href="#" sx={{ color: '#f093fb', textDecoration: 'none' }}>
                Privacy Policy
              </Link>
            </Typography>
          </Box>
        </Paper>
      </Container>
    </Box>
  );
};

export default Register;