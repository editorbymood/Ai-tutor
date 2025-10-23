import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { useSelector } from 'react-redux';

// Pages
import Landing from './pages/Landing';
import Login from './pages/Login';
import Register from './pages/Register';
import StudentDashboard from './pages/StudentDashboard';
import TeacherDashboard from './pages/TeacherDashboard';
import Courses from './pages/Courses';
import CourseDetail from './pages/CourseDetail';
import AITutor from './pages/AITutor';
import Quiz from './pages/Quiz';
import Profile from './pages/Profile';

// Components
import Layout from './components/Layout';
import PrivateRoute from './components/PrivateRoute';

const theme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: '#667eea',
      light: '#8b9ff7',
      dark: '#4f5fcf',
      contrastText: '#ffffff',
    },
    secondary: {
      main: '#764ba2',
      light: '#9b6bc9',
      dark: '#5a3a7d',
      contrastText: '#ffffff',
    },
    success: {
      main: '#4facfe',
      light: '#7ec2fe',
      dark: '#3a8bd4',
    },
    warning: {
      main: '#fee140',
      light: '#fef166',
      dark: '#d4be36',
    },
    error: {
      main: '#f5576c',
      light: '#f87887',
      dark: '#d44454',
    },
    background: {
      default: 'transparent',
      paper: 'rgba(255, 255, 255, 0.9)',
    },
    text: {
      primary: '#2d3748',
      secondary: '#4a5568',
    },
  },
  typography: {
    fontFamily: '"Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif',
    h1: {
      fontFamily: '"Poppins", sans-serif',
      fontWeight: 800,
      letterSpacing: '-0.02em',
    },
    h2: {
      fontFamily: '"Poppins", sans-serif',
      fontWeight: 700,
      letterSpacing: '-0.01em',
    },
    h3: {
      fontFamily: '"Poppins", sans-serif',
      fontWeight: 600,
    },
    h4: {
      fontFamily: '"Poppins", sans-serif',
      fontWeight: 600,
    },
    h5: {
      fontFamily: '"Poppins", sans-serif',
      fontWeight: 600,
    },
    h6: {
      fontFamily: '"Poppins", sans-serif',
      fontWeight: 600,
    },
    button: {
      textTransform: 'none',
      fontWeight: 600,
      letterSpacing: '0.02em',
    },
  },
  shape: {
    borderRadius: 12,
  },
  shadows: [
    'none',
    '0 2px 8px rgba(0, 0, 0, 0.1)',
    '0 4px 16px rgba(0, 0, 0, 0.12)',
    '0 6px 20px rgba(0, 0, 0, 0.14)',
    '0 8px 24px rgba(0, 0, 0, 0.16)',
    '0 10px 28px rgba(0, 0, 0, 0.18)',
    '0 12px 32px rgba(0, 0, 0, 0.2)',
    '0 14px 36px rgba(0, 0, 0, 0.22)',
    '0 16px 40px rgba(0, 0, 0, 0.24)',
    '0 8px 32px 0 rgba(31, 38, 135, 0.37)',
    '0 12px 40px 0 rgba(31, 38, 135, 0.5)',
    '0 0 20px rgba(102, 126, 234, 0.3)',
    '0 0 40px rgba(102, 126, 234, 0.6)',
    ...Array(12).fill('0 8px 32px 0 rgba(31, 38, 135, 0.37)'),
  ],
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: '12px',
          padding: '10px 24px',
          fontSize: '0.95rem',
          fontWeight: 600,
          transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
          '&:hover': {
            transform: 'translateY(-2px)',
            boxShadow: '0 8px 24px rgba(0, 0, 0, 0.2)',
          },
        },
        contained: {
          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
          boxShadow: '0 4px 16px rgba(102, 126, 234, 0.4)',
          '&:hover': {
            background: 'linear-gradient(135deg, #5568d3 0%, #6a3f8f 100%)',
            boxShadow: '0 8px 24px rgba(102, 126, 234, 0.6)',
          },
        },
      },
    },
    MuiPaper: {
      styleOverrides: {
        root: {
          backgroundImage: 'none',
          backgroundColor: 'rgba(255, 255, 255, 0.9)',
          backdropFilter: 'blur(10px)',
          border: '1px solid rgba(255, 255, 255, 0.2)',
          transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
        },
        elevation1: {
          boxShadow: '0 8px 32px 0 rgba(31, 38, 135, 0.37)',
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          borderRadius: '16px',
          overflow: 'hidden',
          transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
          '&:hover': {
            transform: 'translateY(-5px)',
            boxShadow: '0 12px 40px 0 rgba(31, 38, 135, 0.5)',
          },
        },
      },
    },
    MuiTextField: {
      styleOverrides: {
        root: {
          '& .MuiOutlinedInput-root': {
            borderRadius: '12px',
            backgroundColor: 'rgba(255, 255, 255, 0.8)',
            transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
            '&:hover': {
              backgroundColor: 'rgba(255, 255, 255, 0.95)',
            },
            '&.Mui-focused': {
              backgroundColor: 'rgba(255, 255, 255, 1)',
              boxShadow: '0 0 0 3px rgba(102, 126, 234, 0.2)',
            },
          },
        },
      },
    },
    MuiChip: {
      styleOverrides: {
        root: {
          borderRadius: '8px',
          fontWeight: 500,
        },
      },
    },
    MuiAppBar: {
      styleOverrides: {
        root: {
          backgroundColor: 'rgba(255, 255, 255, 0.9)',
          backdropFilter: 'blur(10px)',
          boxShadow: '0 4px 16px rgba(0, 0, 0, 0.1)',
          color: '#2d3748',
        },
      },
    },
  },
});

function App() {
  const { isAuthenticated, user } = useSelector((state) => state.auth);

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <Routes>
          {/* Landing Page */}
          <Route path="/" element={
            isAuthenticated ? <Navigate to="/dashboard" /> : <Landing />
          } />

          {/* Public Routes */}
          <Route path="/login" element={
            isAuthenticated ? <Navigate to="/dashboard" /> : <Login />
          } />
          <Route path="/register" element={
            isAuthenticated ? <Navigate to="/dashboard" /> : <Register />
          } />

          {/* Protected Routes */}
          <Route element={<PrivateRoute><Layout /></PrivateRoute>}>
            <Route path="/dashboard" element={
              user?.role === 'teacher' ? <TeacherDashboard /> : <StudentDashboard />
            } />
            <Route path="/courses" element={<Courses />} />
            <Route path="/courses/:id" element={<CourseDetail />} />
            <Route path="/ai-tutor" element={<AITutor />} />
            <Route path="/quiz/:id" element={<Quiz />} />
            <Route path="/profile" element={<Profile />} />
          </Route>
        </Routes>
      </Router>
    </ThemeProvider>
  );
}

export default App;