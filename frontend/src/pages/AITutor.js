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
} from '@mui/material';
import { Send, SmartToy, Person } from '@mui/icons-material';
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
    <Box>
      <Typography variant="h4" gutterBottom>
        AI Tutor Chat
      </Typography>

      {error && (
        <Alert 
          severity="error" 
          onClose={() => dispatch(clearError())}
          sx={{ mb: 2 }}
        >
          {error}
        </Alert>
      )}

      {!currentSession && loading ? (
        <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '70vh' }}>
          <CircularProgress />
          <Typography sx={{ ml: 2 }}>Initializing chat session...</Typography>
        </Box>
      ) : (
        <Paper sx={{ height: '70vh', display: 'flex', flexDirection: 'column' }}>
        <Box sx={{ flexGrow: 1, overflow: 'auto', p: 2 }}>
          {messages && messages.length > 0 ? (
            <List>
              {messages.map((message, index) => (
                <ListItem
                  key={index}
                  sx={{
                    flexDirection: message.role === 'user' ? 'row-reverse' : 'row',
                    alignItems: 'flex-start',
                  }}
                >
                  <Avatar
                    sx={{
                      bgcolor: message.role === 'user' ? 'primary.main' : 'secondary.main',
                      mx: 1,
                    }}
                  >
                    {message.role === 'user' ? <Person /> : <SmartToy />}
                  </Avatar>
                  <Paper
                    sx={{
                      p: 2,
                      maxWidth: '70%',
                      bgcolor: message.role === 'user' ? 'primary.light' : 'grey.100',
                    }}
                  >
                    <Typography variant="body1">{message.content}</Typography>
                  </Paper>
                </ListItem>
              ))}
              {loading && (
                <ListItem>
                  <CircularProgress size={24} />
                  <Typography sx={{ ml: 2 }}>AI is thinking...</Typography>
                </ListItem>
              )}
              <div ref={messagesEndRef} />
            </List>
          ) : (
            <Box sx={{ textAlign: 'center', py: 8 }}>
              <SmartToy sx={{ fontSize: 80, color: 'text.secondary', mb: 2 }} />
              <Typography variant="h6" color="text.secondary" gutterBottom>
                Welcome to AI Tutor Chat!
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Ask me anything and I'll help you learn
              </Typography>
            </Box>
          )}
        </Box>

        <Box sx={{ p: 2, borderTop: 1, borderColor: 'divider' }}>
          <Box sx={{ display: 'flex', gap: 1 }}>
            <TextField
              fullWidth
              multiline
              maxRows={4}
              placeholder="Ask me anything..."
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              disabled={loading}
            />
            <Button
              variant="contained"
              endIcon={<Send />}
              onClick={handleSend}
              disabled={loading || !inputMessage.trim() || !currentSession}
            >
              Send
            </Button>
          </Box>
        </Box>
      </Paper>
      )}
    </Box>
  );
};

export default AITutor;