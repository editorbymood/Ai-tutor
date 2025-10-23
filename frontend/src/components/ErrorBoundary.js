import React, { Component } from 'react';
import { Box, Typography, Button, Container } from '@mui/material';
import ErrorOutlineIcon from '@mui/icons-material/ErrorOutline';

/**
 * Error Boundary component - catches JavaScript errors anywhere in the child component tree
 */
class ErrorBoundary extends Component {
  constructor(props) {
    super(props);
    this.state = {
      hasError: false,
      error: null,
      errorInfo: null
    };
  }

  static getDerivedStateFromError(error) {
    // Update state so the next render will show the fallback UI
    return { hasError: true };
  }

  componentDidCatch(error, errorInfo) {
    // Log the error to an error reporting service
    console.error('Error caught by boundary:', error, errorInfo);
    this.setState({
      error,
      errorInfo
    });
  }

  handleReset = () => {
    this.setState({
      hasError: false,
      error: null,
      errorInfo: null
    });
  };

  render() {
    if (this.state.hasError) {
      return (
        <Container maxWidth="md">
          <Box
            display="flex"
            flexDirection="column"
            justifyContent="center"
            alignItems="center"
            minHeight="100vh"
            textAlign="center"
            gap={3}
          >
            <ErrorOutlineIcon color="error" sx={{ fontSize: 80 }} />
            
            <Typography variant="h4" color="error" gutterBottom>
              Oops! Something went wrong
            </Typography>
            
            <Typography variant="body1" color="textSecondary" paragraph>
              We're sorry for the inconvenience. The application encountered an unexpected error.
            </Typography>

            {process.env.NODE_ENV === 'development' && this.state.error && (
              <Box
                bgcolor="#f5f5f5"
                p={2}
                borderRadius={1}
                textAlign="left"
                width="100%"
                maxWidth={600}
              >
                <Typography variant="h6" gutterBottom>
                  Error Details:
                </Typography>
                <Typography variant="body2" component="pre" style={{ whiteSpace: 'pre-wrap' }}>
                  {this.state.error.toString()}
                </Typography>
                {this.state.errorInfo && (
                  <Typography variant="body2" component="pre" style={{ whiteSpace: 'pre-wrap' }}>
                    {this.state.errorInfo.componentStack}
                  </Typography>
                )}
              </Box>
            )}

            <Box display="flex" gap={2}>
              <Button
                variant="contained"
                color="primary"
                onClick={this.handleReset}
              >
                Try Again
              </Button>
              
              <Button
                variant="outlined"
                color="primary"
                onClick={() => window.location.href = '/'}
              >
                Go to Home
              </Button>
            </Box>
          </Box>
        </Container>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;
