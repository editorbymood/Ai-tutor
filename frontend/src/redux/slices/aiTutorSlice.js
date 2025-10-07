import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import api from '../../services/api';

const initialState = {
  chatSessions: [],
  currentSession: null,
  messages: [],
  loading: false,
  error: null,
};

// Async thunks
export const fetchChatSessions = createAsyncThunk(
  'aiTutor/fetchChatSessions',
  async (_, { rejectWithValue }) => {
    try {
      const response = await api.get('/ai-tutor/chat/');
      return response.data.data;
    } catch (error) {
      return rejectWithValue(error.response?.data?.error?.message || 'Failed to fetch sessions');
    }
  }
);

export const createChatSession = createAsyncThunk(
  'aiTutor/createChatSession',
  async (sessionData, { rejectWithValue }) => {
    try {
      const response = await api.post('/ai-tutor/chat/', sessionData);
      return response.data.data;
    } catch (error) {
      return rejectWithValue(error.response?.data?.error?.message || 'Failed to create session');
    }
  }
);

export const sendMessage = createAsyncThunk(
  'aiTutor/sendMessage',
  async ({ sessionId, message }, { rejectWithValue }) => {
    try {
      const response = await api.post(`/ai-tutor/chat/${sessionId}/message/`, { message });
      return response.data.data;
    } catch (error) {
      return rejectWithValue(error.response?.data?.error?.message || 'Failed to send message');
    }
  }
);

export const generateLesson = createAsyncThunk(
  'aiTutor/generateLesson',
  async (lessonData, { rejectWithValue }) => {
    try {
      const response = await api.post('/ai-tutor/generate/lesson/', lessonData);
      return response.data.data;
    } catch (error) {
      return rejectWithValue(error.response?.data?.error?.message || 'Failed to generate lesson');
    }
  }
);

const aiTutorSlice = createSlice({
  name: 'aiTutor',
  initialState,
  reducers: {
    setCurrentSession: (state, action) => {
      state.currentSession = action.payload;
      state.messages = action.payload?.messages || [];
    },
    clearError: (state) => {
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    builder
      // Fetch Sessions
      .addCase(fetchChatSessions.pending, (state) => {
        state.loading = true;
      })
      .addCase(fetchChatSessions.fulfilled, (state, action) => {
        state.loading = false;
        state.chatSessions = action.payload;
      })
      .addCase(fetchChatSessions.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      // Create Session
      .addCase(createChatSession.fulfilled, (state, action) => {
        state.chatSessions.unshift(action.payload);
        state.currentSession = action.payload;
      })
      // Send Message
      .addCase(sendMessage.pending, (state) => {
        state.loading = true;
      })
      .addCase(sendMessage.fulfilled, (state, action) => {
        state.loading = false;
        state.messages.push(action.payload.user_message);
        state.messages.push(action.payload.ai_response);
      })
      .addCase(sendMessage.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      });
  },
});

export const { setCurrentSession, clearError } = aiTutorSlice.actions;
export default aiTutorSlice.reducer;