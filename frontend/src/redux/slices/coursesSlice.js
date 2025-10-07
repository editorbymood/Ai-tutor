import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import api from '../../services/api';

const initialState = {
  courses: [],
  currentCourse: null,
  enrollments: [],
  loading: false,
  error: null,
};

// Async thunks
export const fetchCourses = createAsyncThunk(
  'courses/fetchCourses',
  async (filters = {}, { rejectWithValue }) => {
    try {
      const params = new URLSearchParams(filters);
      const response = await api.get(`/courses/?${params}`);
      return response.data.data;
    } catch (error) {
      return rejectWithValue(error.response?.data?.error?.message || 'Failed to fetch courses');
    }
  }
);

export const fetchCourseDetail = createAsyncThunk(
  'courses/fetchCourseDetail',
  async (courseId, { rejectWithValue }) => {
    try {
      const response = await api.get(`/courses/${courseId}/`);
      return response.data.data;
    } catch (error) {
      return rejectWithValue(error.response?.data?.error?.message || 'Failed to fetch course');
    }
  }
);

export const enrollCourse = createAsyncThunk(
  'courses/enrollCourse',
  async (courseId, { rejectWithValue }) => {
    try {
      const response = await api.post(`/courses/${courseId}/enroll/`);
      return response.data.data;
    } catch (error) {
      return rejectWithValue(error.response?.data?.error?.message || 'Enrollment failed');
    }
  }
);

export const fetchMyEnrollments = createAsyncThunk(
  'courses/fetchMyEnrollments',
  async (_, { rejectWithValue }) => {
    try {
      const response = await api.get('/courses/my-enrollments/');
      return response.data.data;
    } catch (error) {
      return rejectWithValue(error.response?.data?.error?.message || 'Failed to fetch enrollments');
    }
  }
);

const coursesSlice = createSlice({
  name: 'courses',
  initialState,
  reducers: {
    clearError: (state) => {
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    builder
      // Fetch Courses
      .addCase(fetchCourses.pending, (state) => {
        state.loading = true;
      })
      .addCase(fetchCourses.fulfilled, (state, action) => {
        state.loading = false;
        state.courses = action.payload;
      })
      .addCase(fetchCourses.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      // Fetch Course Detail
      .addCase(fetchCourseDetail.pending, (state) => {
        state.loading = true;
      })
      .addCase(fetchCourseDetail.fulfilled, (state, action) => {
        state.loading = false;
        state.currentCourse = action.payload;
      })
      .addCase(fetchCourseDetail.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      // Enroll Course
      .addCase(enrollCourse.fulfilled, (state, action) => {
        state.enrollments.push(action.payload);
      })
      // Fetch Enrollments
      .addCase(fetchMyEnrollments.fulfilled, (state, action) => {
        state.enrollments = action.payload;
      });
  },
});

export const { clearError } = coursesSlice.actions;
export default coursesSlice.reducer;