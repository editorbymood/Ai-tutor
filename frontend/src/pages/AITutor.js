import React, { useState, useEffect, useRef } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import {
  Box,
  Paper,
  TextField,
  Button,
  Typography,
  List,
  ListItem,
  Avatar,
  CircularProgress,
  Alert,
  IconButton,
  Chip,
  Stack,
} from '@mui/material';
import { Send, SmartToy, Person, AutoAwesome, Psychology, Lightbulb, Code } from '@mui/icons-material';
import { sendMessage, createChatSession, setCurrentSession, clearError } from '../redux/slices/aiTutorSlice';

const AITutor = () => {
  const dispatch = useDispatch();
  const { currentSession, messages, loading, error } = useSelector((state) => state.aiTutor);
  const [inputMessage, setInputMessage] = useState('');
  const messagesEndRef = useRef(null);

  useEffect(() => {
    if (!currentSession) {
      console.log('Creating new chat session...');
      dispatch(createChatSession({ title: 'New Chat' }));
    }
  }, [dispatch, currentSession]);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSend = async () => {
    if (!inputMessage.trim() || !currentSession) return;

    console.log('Sending message:', inputMessage, 'to session:', currentSession.id);
    const result = await dispatch(sendMessage({
      sessionId: currentSession.id,
      message: inputMessage,
    }));
    
    if (result.error) {
      console.error('Failed to send message:', result.error);
    }
    setInputMessage('');
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <Box className="fade-in">
      {/* Header */}
      <Paper
        sx={{
          p: 4,
          mb: 3,
          borderRadius: '24px',
          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
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
          <Stack direction="row" spacing={2} alignItems="center" sx={{ mb: 2 }}>
            <Box
              sx={{
                width: 64,
                height: 64,
                borderRadius: '16px',
                background: 'rgba(255, 255, 255, 0.2)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
              }}
            >
              <Psychology sx={{ fontSize: 40 }} />
            </Box>
            <Box>
              <Typography variant="h4" sx={{ fontWeight: 800 }}>
                AI Tutor Chat 🤖
              </Typography>
              <Typography variant="body1" sx={{ opacity: 0.9 }}>
                Your personal AI learning assistant
              </Typography>
            </Box>
          </Stack>
          <Stack direction="row" spacing={1} sx={{ mt: 2 }}>
            <Chip
              icon={<AutoAwesome />}
              label="Powered by Advanced AI"
              sx={{
                background: 'rgba(255, 255, 255, 0.2)',
                color: 'white',
                '& .MuiChip-icon': { color: 'white' },
              }}
            />
            <Chip
              icon={<Lightbulb />}
              label="24/7 Available"
              sx={{
                background: 'rgba(255, 255, 255, 0.2)',
                color: 'white',
                '& .MuiChip-icon': { color: '#fee140' },
              }}
            />
          </Stack>
        </Box>
      </Paper>

      {error && (
        <Alert
          severity="error"
          onClose={() => dispatch(clearError())}
          sx={{ mb: 3, borderRadius: '16px' }}
        >
          {error}
        </Alert>
      )}

      {!currentSession && loading ? (
        <Paper
          sx={{
            height: '70vh',
            borderRadius: '24px',
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
            background: 'white',
          }}
        >
          <Box sx={{ textAlign: 'center' }}>
            <CircularProgress size={60} sx={{ color: '#667eea' }} />
            <Typography sx={{ mt: 2, color: 'text.secondary', fontWeight: 600 }}>
              Initializing AI Tutor...
            </Typography>
          </Box>
        </Paper>
      ) : (
        <Paper
          sx={{
            height: '70vh',
            display: 'flex',
            flexDirection: 'column',
            borderRadius: '24px',
            overflow: 'hidden',
            background: 'white',
            boxShadow: '0 4px 20px rgba(0, 0, 0, 0.08)',
          }}
        >
          {/* Messages Area */}
          <Box
            sx={{
              flexGrow: 1,
              overflow: 'auto',
              p: 3,
              background: 'linear-gradient(180deg, #f8f9ff 0%, #ffffff 100%)',
            }}
          >
            {messages && messages.length > 0 ? (
              <List sx={{ p: 0 }}>
                {messages.map((message, index) => (
                  <ListItem
                    key={index}
                    sx={{
                      flexDirection: message.role === 'user' ? 'row-reverse' : 'row',
                      alignItems: 'flex-start',
                      mb: 3,
                      gap: 2,
                    }}
                  >
                    <Avatar
                      sx={{
                        width: 48,
                        height: 48,
                        background:
                          message.role === 'user'
                            ? 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
                            : 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
                        boxShadow: '0 4px 12px rgba(0, 0, 0, 0.15)',
                      }}
                    >
                      {message.role === 'user' ? <Person /> : <SmartToy />}
                    </Avatar>
                    <Paper
                      elevation={0}
                      sx={{
                        p: 2.5,
                        maxWidth: '70%',
                        borderRadius: '16px',
                        background:
                          message.role === 'user'
                            ? 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
                            : 'white',
                        color: message.role === 'user' ? 'white' : 'text.primary',
                        border: message.role === 'user' ? 'none' : '1px solid rgba(0, 0, 0, 0.08)',
                        boxShadow: message.role === 'user' ? '0 4px 12px rgba(102, 126, 234, 0.3)' : '0 2px 8px rgba(0, 0, 0, 0.05)',
                      }}
                    >
                      <Typography
                        variant="body1"
                        sx={{
                          lineHeight: 1.7,
                          whiteSpace: 'pre-wrap',
                          wordBreak: 'break-word',
                        }}
                      >
                        {message.content}
                      </Typography>
                    </Paper>
                  </ListItem>
                ))}
                {loading && (
                  <ListItem sx={{ gap: 2 }}>
                    <Avatar
                      sx={{
                        width: 48,
                        height: 48,
                        background: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
                      }}
                    >
                      <SmartToy />
                    </Avatar>
                    <Paper
                      elevation={0}
                      sx={{
                        p: 2.5,
                        borderRadius: '16px',
                        border: '1px solid rgba(0, 0, 0, 0.08)',
                      }}
                    >
                      <Stack direction="row" spacing={1} alignItems="center">
                        <CircularProgress size={20} sx={{ color: '#667eea' }} />
                        <Typography color="text.secondary">AI is thinking...</Typography>
                      </Stack>
                    </Paper>
                  </ListItem>
                )}
                <div ref={messagesEndRef} />
              </List>
            ) : (
              <Box
                sx={{
                  textAlign: 'center',
                  py: 8,
                  display: 'flex',
                  flexDirection: 'column',
                  alignItems: 'center',
                  justifyContent: 'center',
                  height: '100%',
                }}
              >
                <Box
                  sx={{
                    width: 120,
                    height: 120,
                    borderRadius: '32px',
                    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    mb: 3,
                    boxShadow: '0 12px 32px rgba(102, 126, 234, 0.3)',
                  }}
                >
                  <SmartToy sx={{ fontSize: 64, color: 'white' }} />
                </Box>
                <Typography variant="h5" sx={{ fontWeight: 700, mb: 1 }}>
                  Welcome to AI Tutor! 👋
                </Typography>
                <Typography variant="body1" color="text.secondary" sx={{ mb: 4, maxWidth: 500 }}>
                  I'm your personal AI learning assistant. Ask me anything about your studies,
                  and I'll help you understand complex topics with clear explanations.
                </Typography>
                <Stack direction="row" spacing={2} flexWrap="wrap" justifyContent="center">
                  <Chip
                    icon={<Code />}
                    label="Explain a concept"
                    onClick={() => setInputMessage('Explain how recursion works in programming')}
                    sx={{ cursor: 'pointer' }}
                  />
                  <Chip
                    icon={<Lightbulb />}
                    label="Get study tips"
                    onClick={() => setInputMessage('How can I study more effectively?')}
                    sx={{ cursor: 'pointer' }}
                  />
                  <Chip
                    icon={<Psychology />}
                    label="Solve a problem"
                    onClick={() => setInputMessage('Help me solve this math problem')}
                    sx={{ cursor: 'pointer' }}
                  />
                </Stack>
              </Box>
            )}
          </Box>

          {/* Input Area */}
          <Box
            sx={{
              p: 3,
              borderTop: '1px solid',
              borderColor: 'divider',
              background: 'white',
            }}
          >
            <Box sx={{ display: 'flex', gap: 2, alignItems: 'flex-end' }}>
              <TextField
                fullWidth
                multiline
                maxRows={4}
                placeholder="Ask me anything... (Press Enter to send)"
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                onKeyPress={handleKeyPress}
                disabled={loading}
                sx={{
                  '& .MuiOutlinedInput-root': {
                    borderRadius: '16px',
                    background: 'rgba(102, 126, 234, 0.05)',
                    '&:hover fieldset': {
                      borderColor: '#667eea',
                    },
                    '&.Mui-focused fieldset': {
                      borderColor: '#667eea',
                      borderWidth: '2px',
                    },
                  },
                }}
              />
              <IconButton
                onClick={handleSend}
                disabled={loading || !inputMessage.trim() || !currentSession}
                sx={{
                  width: 56,
                  height: 56,
                  background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                  color: 'white',
                  borderRadius: '16px',
                  boxShadow: '0 4px 12px rgba(102, 126, 234, 0.4)',
                  '&:hover': {
                    background: 'linear-gradient(135deg, #5568d3 0%, #6a3f8f 100%)',
                    transform: 'translateY(-2px)',
                    boxShadow: '0 6px 16px rgba(102, 126, 234, 0.5)',
                  },
                  '&:disabled': {
                    background: '#ccc',
                    color: 'white',
                  },
                  transition: 'all 0.3s ease',
                }}
              >
                <Send />
              </IconButton>
            </Box>
            <Typography
              variant="caption"
              color="text.secondary"
              sx={{ display: 'block', mt: 1, textAlign: 'center' }}
            >
              AI Tutor is powered by advanced language models. Always verify important information.
            </Typography>
          </Box>
        </Paper>
      )}
    </Box>
  );
};

export default AITutor;