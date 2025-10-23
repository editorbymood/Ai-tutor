import React, { useState } from 'react';
import { Outlet, useNavigate, useLocation } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import {
  AppBar,
  Box,
  Toolbar,
  IconButton,
  Typography,
  Menu,
  Container,
  Avatar,
  Button,
  Tooltip,
  MenuItem,
  Drawer,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Chip,
  Divider,
  Badge,
  Fade,
  Zoom,
} from '@mui/material';
import {
  Menu as MenuIcon,
  Dashboard,
  School,
  Chat,
  Assessment,
  Person,
  Logout,
  EmojiEvents,
  Notifications,
  Settings,
  Star,
  TrendingUp,
} from '@mui/icons-material';
import { logout } from '../redux/slices/authSlice';

const Layout = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const dispatch = useDispatch();
  const { user } = useSelector((state) => state.auth);
  
  const [anchorElUser, setAnchorElUser] = useState(null);
  const [drawerOpen, setDrawerOpen] = useState(false);
  const [anchorElNotif, setAnchorElNotif] = useState(null);

  const handleOpenUserMenu = (event) => {
    setAnchorElUser(event.currentTarget);
  };

  const handleCloseUserMenu = () => {
    setAnchorElUser(null);
  };

  const handleLogout = () => {
    dispatch(logout());
    navigate('/login');
  };

  const menuItems = [
    { text: 'Dashboard', icon: <Dashboard />, path: '/dashboard', gradient: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' },
    { text: 'Courses', icon: <School />, path: '/courses', gradient: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)' },
    { text: 'AI Tutor', icon: <Chat />, path: '/ai-tutor', gradient: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)' },
    { text: 'Achievements', icon: <EmojiEvents />, path: '/achievements', gradient: 'linear-gradient(135deg, #fa709a 0%, #fee140 100%)' },
    { text: 'Profile', icon: <Person />, path: '/profile', gradient: 'linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)' },
  ];

  const isActiveRoute = (path) => location.pathname === path;

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      {/* Premium Glass AppBar */}
      <AppBar 
        position="sticky" 
        elevation={0}
        sx={{
          background: 'rgba(255, 255, 255, 0.95)',
          backdropFilter: 'blur(20px)',
          borderBottom: '1px solid rgba(255, 255, 255, 0.3)',
          boxShadow: '0 4px 30px rgba(0, 0, 0, 0.1)',
        }}
      >
        <Container maxWidth="xl">
          <Toolbar disableGutters sx={{ minHeight: '70px !important' }}>
            <IconButton
              size="large"
              edge="start"
              aria-label="menu"
              onClick={() => setDrawerOpen(true)}
              sx={{
                mr: 2,
                background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                color: 'white',
                '&:hover': {
                  background: 'linear-gradient(135deg, #5568d3 0%, #6a3f8f 100%)',
                  transform: 'rotate(90deg)',
                },
                transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
              }}
            >
              <MenuIcon />
            </IconButton>
            
            {/* Logo with Gradient */}
            <Box
              sx={{
                display: 'flex',
                alignItems: 'center',
                cursor: 'pointer',
                '&:hover': { transform: 'scale(1.05)' },
                transition: 'transform 0.3s ease',
              }}
              onClick={() => navigate('/dashboard')}
            >
              <Star sx={{ 
                fontSize: 32, 
                mr: 1,
                background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                WebkitBackgroundClip: 'text',
                WebkitTextFillColor: 'transparent',
                animation: 'spin 20s linear infinite',
                '@keyframes spin': {
                  '0%': { transform: 'rotate(0deg)' },
                  '100%': { transform: 'rotate(360deg)' },
                },
              }} />
              <Typography
                variant="h5"
                noWrap
                sx={{
                  fontFamily: 'Poppins',
                  fontWeight: 800,
                  background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                  WebkitBackgroundClip: 'text',
                  WebkitTextFillColor: 'transparent',
                  letterSpacing: '-0.02em',
                }}
              >
                AI Tutor
              </Typography>
            </Box>

            {/* User Badge */}
            <Chip
              label={user?.role === 'teacher' ? '👨‍🏫 Teacher' : '🎓 Student'}
              size="small"
              sx={{
                ml: 2,
                background: user?.role === 'teacher' 
                  ? 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)'
                  : 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
                color: 'white',
                fontWeight: 600,
                px: 1,
              }}
            />

            <Box sx={{ flexGrow: 1 }} />

            {/* Notifications */}
            <Tooltip title="Notifications" TransitionComponent={Zoom}>
              <IconButton 
                onClick={(e) => setAnchorElNotif(e.currentTarget)}
                sx={{
                  mr: 2,
                  '&:hover': {
                    background: 'rgba(102, 126, 234, 0.1)',
                    transform: 'scale(1.1)',
                  },
                  transition: 'all 0.3s',
                }}
              >
                <Badge badgeContent={3} color="error">
                  <Notifications sx={{ color: '#667eea' }} />
                </Badge>
              </IconButton>
            </Tooltip>

            {/* User Menu */}
            <Box sx={{ flexGrow: 0 }}>
              <Tooltip title="Open settings" TransitionComponent={Zoom}>
                <IconButton 
                  onClick={handleOpenUserMenu} 
                  sx={{ 
                    p: 0.5,
                    '&:hover': {
                      transform: 'scale(1.1)',
                    },
                    transition: 'transform 0.3s',
                  }}
                >
                  <Avatar 
                    alt={user?.full_name} 
                    src={user?.avatar}
                    sx={{
                      width: 45,
                      height: 45,
                      border: '3px solid',
                      borderImageSlice: 1,
                      borderImageSource: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                      boxShadow: '0 4px 15px rgba(102, 126, 234, 0.4)',
                    }}
                  >
                    {user?.full_name?.charAt(0)}
                  </Avatar>
                </IconButton>
              </Tooltip>
              <Menu
                sx={{ mt: '50px' }}
                id="menu-appbar"
                anchorEl={anchorElUser}
                anchorOrigin={{ vertical: 'top', horizontal: 'right' }}
                keepMounted
                transformOrigin={{ vertical: 'top', horizontal: 'right' }}
                open={Boolean(anchorElUser)}
                onClose={handleCloseUserMenu}
                TransitionComponent={Fade}
                PaperProps={{
                  sx: {
                    mt: 1,
                    borderRadius: '16px',
                    background: 'rgba(255, 255, 255, 0.95)',
                    backdropFilter: 'blur(20px)',
                    border: '1px solid rgba(255, 255, 255, 0.3)',
                    boxShadow: '0 8px 32px rgba(0, 0, 0, 0.1)',
                  },
                }}
              >
                <MenuItem onClick={() => { navigate('/profile'); handleCloseUserMenu(); }}>
                  <Person sx={{ mr: 1, color: '#667eea' }} />
                  <Typography>Profile</Typography>
                </MenuItem>
                <MenuItem onClick={() => { navigate('/settings'); handleCloseUserMenu(); }}>
                  <Settings sx={{ mr: 1, color: '#764ba2' }} />
                  <Typography>Settings</Typography>
                </MenuItem>
                <Divider sx={{ my: 1 }} />
                <MenuItem onClick={handleLogout} sx={{ color: '#f5576c' }}>
                  <Logout sx={{ mr: 1 }} />
                  <Typography>Logout</Typography>
                </MenuItem>
              </Menu>
            </Box>
          </Toolbar>
        </Container>
      </AppBar>

      {/* Premium Glass Drawer */}
      <Drawer
        anchor="left"
        open={drawerOpen}
        onClose={() => setDrawerOpen(false)}
        PaperProps={{
          sx: {
            width: 280,
            background: 'rgba(255, 255, 255, 0.95)',
            backdropFilter: 'blur(20px)',
            borderRight: '1px solid rgba(255, 255, 255, 0.3)',
          },
        }}
      >
        <Box sx={{ p: 3 }}>
          {/* User Info Card */}
          <Box
            sx={{
              mb: 3,
              p: 2,
              borderRadius: '16px',
              background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
              color: 'white',
              boxShadow: '0 8px 24px rgba(102, 126, 234, 0.4)',
            }}
          >
            <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
              <Avatar
                alt={user?.full_name}
                src={user?.avatar}
                sx={{ 
                  width: 50, 
                  height: 50, 
                  mr: 2,
                  border: '3px solid white',
                }}
              >
                {user?.full_name?.charAt(0)}
              </Avatar>
              <Box>
                <Typography variant="h6" sx={{ fontWeight: 700, fontSize: '1rem' }}>
                  {user?.full_name || 'User'}
                </Typography>
                <Typography variant="caption" sx={{ opacity: 0.9 }}>
                  {user?.email}
                </Typography>
              </Box>
            </Box>
            <Box sx={{ display: 'flex', gap: 1 }}>
              <Chip
                icon={<TrendingUp />}
                label="Level 5"
                size="small"
                sx={{ background: 'rgba(255,255,255,0.2)', color: 'white' }}
              />
              <Chip
                icon={<Star />}
                label="850 XP"
                size="small"
                sx={{ background: 'rgba(255,255,255,0.2)', color: 'white' }}
              />
            </Box>
          </Box>

          {/* Menu Items */}
          <List sx={{ px: 0 }}>
            {menuItems.map((item, index) => (
              <Zoom in={drawerOpen} style={{ transitionDelay: `${index * 50}ms` }} key={item.text}>
                <ListItem
                  button
                  onClick={() => { navigate(item.path); setDrawerOpen(false); }}
                  sx={{
                    mb: 1,
                    borderRadius: '12px',
                    background: isActiveRoute(item.path)
                      ? item.gradient
                      : 'transparent',
                    color: isActiveRoute(item.path) ? 'white' : '#2d3748',
                    '&:hover': {
                      background: item.gradient,
                      color: 'white',
                      transform: 'translateX(8px)',
                      boxShadow: '0 4px 15px rgba(102, 126, 234, 0.3)',
                    },
                    transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
                  }}
                >
                  <ListItemIcon
                    sx={{
                      color: isActiveRoute(item.path) ? 'white' : '#667eea',
                      minWidth: 40,
                    }}
                  >
                    {item.icon}
                  </ListItemIcon>
                  <ListItemText 
                    primary={item.text}
                    primaryTypographyProps={{
                      fontWeight: isActiveRoute(item.path) ? 600 : 500,
                    }}
                  />
                </ListItem>
              </Zoom>
            ))}            
            <Divider sx={{ my: 2 }} />
            <ListItem
              button
              onClick={handleLogout}
              sx={{
                borderRadius: '12px',
                '&:hover': {
                  background: 'linear-gradient(135deg, #f5576c 0%, #d44454 100%)',
                  color: 'white',
                  transform: 'translateX(8px)',
                },
                transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
              }}
            >
              <ListItemIcon sx={{ minWidth: 40 }}>
                <Logout sx={{ color: '#f5576c' }} />
              </ListItemIcon>
              <ListItemText primary="Logout" />
            </ListItem>
          </List>
        </Box>
      </Drawer>

      {/* Main Content with Animation */}
      <Container 
        component="main" 
        maxWidth="xl"
        sx={{ 
          flexGrow: 1, 
          py: 4,
          minHeight: 'calc(100vh - 200px)',
        }}
        className="fade-in"
      >
        <Outlet />
      </Container>

      {/* Premium Footer */}
      <Box 
        component="footer" 
        sx={{ 
          py: 4, 
          px: 2, 
          mt: 'auto',
          background: 'rgba(255, 255, 255, 0.9)',
          backdropFilter: 'blur(20px)',
          borderTop: '1px solid rgba(255, 255, 255, 0.3)',
        }}
      >
        <Container maxWidth="lg">
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: 2 }}>
            <Typography variant="body2" sx={{ color: '#4a5568', fontWeight: 500 }}>
              © 2024 AI Tutor. Powered by{' '}
              <span className="gradient-text">AI Excellence</span>
            </Typography>
            <Box sx={{ display: 'flex', gap: 2 }}>
              <Typography 
                variant="body2" 
                sx={{ 
                  color: '#667eea', 
                  cursor: 'pointer',
                  '&:hover': { textDecoration: 'underline' },
                }}
              >
                Privacy Policy
              </Typography>
              <Typography 
                variant="body2" 
                sx={{ 
                  color: '#667eea', 
                  cursor: 'pointer',
                  '&:hover': { textDecoration: 'underline' },
                }}
              >
                Terms of Service
              </Typography>
              <Typography 
                variant="body2" 
                sx={{ 
                  color: '#667eea', 
                  cursor: 'pointer',
                  '&:hover': { textDecoration: 'underline' },
                }}
              >
                Help
              </Typography>
            </Box>
          </Box>
        </Container>
      </Box>
    </Box>
  );
};

export default Layout;