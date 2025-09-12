import axios from 'axios';

const API_BASE_URL = 'http://localhost:8012';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface SearchRequest {
  query: string;
  search_type: 'topic' | 'channel';
  max_results?: number;
  analyze_content?: boolean;
}

export interface ChannelAnalysisRequest {
  channel_url: string;
  max_videos?: number;
  include_comments?: boolean;
  deep_analysis?: boolean;
}

export interface VideoAnalysisRequest {
  video_url: string;
  include_comments?: boolean;
  max_comments?: number;
}

export const youtubeAPI = {
  search: async (request: SearchRequest) => {
    const response = await api.post('/api/search', request);
    return response.data;
  },

  analyzeChannel: async (request: ChannelAnalysisRequest) => {
    const response = await api.post('/api/channel/analyze', request);
    return response.data;
  },

  analyzeVideo: async (request: VideoAnalysisRequest) => {
    const response = await api.post('/api/video/analyze', request);
    return response.data;
  },

  detectPatterns: async (videoUrls: string[]) => {
    const response = await api.post('/api/patterns/detect', videoUrls);
    return response.data;
  },

  getChannelVideos: async (channelId: string, limit: number = 50) => {
    const response = await api.get(`/api/channel/${channelId}/videos`, { params: { limit } });
    return response.data;
  },

  compareChannels: async (channelUrls: string[]) => {
    const response = await api.post('/api/compare/channels', channelUrls);
    return response.data;
  },
};

export default api;