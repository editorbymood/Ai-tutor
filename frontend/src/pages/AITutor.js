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
} from '@mui/material';
import { Send, SmartToy, Person } from '@mui/icons-material';
import { sendMessage, createChatSession, setCurrentSession } from '../redux/slices/aiTutorSlice';

const AITutor = () => {
  const dispatch = useDispatch();
  const { currentSession, messages, loading } = useSelector((state) => state.aiTutor);
  const [inputMessage, setInputMessage] = useState('');
  const messagesEndRef = useRef(null);

  useEffect(() => {
    if (!currentSession) {
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

    await dispatch(sendMessage({
      sessionId: currentSession.id,
      message: inputMessage,
    }));
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

      <Paper sx={{ height: '70vh', display: 'flex', flexDirection: 'column' }}>
        <Box sx={{ flexGrow: 1, overflow: 'auto', p: 2 }}>
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
              </ListItem>
            )}
            <div ref={messagesEndRef} />
          </List>
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
              disabled={loading || !inputMessage.trim()}
            >
              Send
            </Button>
          </Box>
        </Box>
      </Paper>
    </Box>
  );
};

export default AITutor;