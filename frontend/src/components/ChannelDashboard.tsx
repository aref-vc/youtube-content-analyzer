import React, { useState, useEffect } from 'react';
import { youtubeAPI } from '../services/api';
import VideoCard from './VideoCard';
import PatternAnalysis from './PatternAnalysis';
import ViralInsights from './ViralInsights';

interface ChannelDashboardProps {
  channelUrl?: string;
  searchResults?: any;
}

const ChannelDashboard: React.FC<ChannelDashboardProps> = ({ channelUrl, searchResults }) => {
  const [channelData, setChannelData] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [selectedVideo, setSelectedVideo] = useState<any>(null);
  const [activeTab, setActiveTab] = useState<'overview' | 'videos' | 'patterns' | 'viral'>('overview');

  useEffect(() => {
    if (channelUrl) {
      analyzeChannel(channelUrl);
    }
  }, [channelUrl]);

  const analyzeChannel = async (url: string) => {
    setIsLoading(true);
    console.log('Analyzing channel:', url);
    try {
      const response = await youtubeAPI.analyzeChannel({
        channel_url: url,
        max_videos: 50,
        deep_analysis: true,
      });
      console.log('Channel analysis response:', response);
      setChannelData(response.data);
    } catch (error) {
      console.error('Channel analysis error:', error);
      alert('Failed to analyze channel. Please check the console for details.');
    } finally {
      setIsLoading(false);
    }
  };

  const formatNumber = (num: number | undefined): string => {
    if (!num) return '0';
    if (num >= 1000000) return `${(num / 1000000).toFixed(1)}M`;
    if (num >= 1000) return `${(num / 1000).toFixed(1)}K`;
    return num.toString();
  };

  const renderOverview = () => {
    if (!channelData && !searchResults) return null;

    const data = channelData || searchResults?.data;
    const channel = data?.channel || data?.channels?.[0];
    const metrics = data?.channel_metrics;

    return (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {channel && (
          <div className="p-6 bg-[#202020] border border-white/10 rounded-xl shadow-inner-soft">
            <h3 className="text-xl font-normal mb-4 text-[#FFF]">Channel Info</h3>
            <div className="space-y-3">
              <div>
                <p className="text-[#868686] text-sm">Channel Name</p>
                <p className="text-[#FFF] text-lg font-semibold">{channel.channel_name}</p>
              </div>
              <div>
                <p className="text-[#868686] text-sm">Subscribers</p>
                <p className="text-[#FFF] text-2xl font-bold number-display">
                  {formatNumber(channel.subscriber_count)}
                </p>
              </div>
              <div>
                <p className="text-[#868686] text-sm">Total Videos</p>
                <p className="text-[#FFF] text-xl font-bold number-display">
                  {channel.video_count || data?.total_videos_found || 'N/A'}
                </p>
              </div>
            </div>
          </div>
        )}

        {metrics && metrics.videos_analyzed > 0 ? (
          <>
            <div className="p-6 bg-[#202020] border border-white/10 rounded-xl shadow-inner-soft">
              <h3 className="text-xl font-normal mb-4 text-[#FFF]">Engagement Metrics</h3>
              <div className="space-y-3">
                <div>
                  <p className="text-[#868686] text-sm">Avg Engagement Score</p>
                  <div className="flex items-center gap-2">
                    <div className="text-3xl font-bold number-display" style={{
                      color: (metrics.average_engagement_score || 0) > 70 ? '#2eb872' : 
                             (metrics.average_engagement_score || 0) > 40 ? '#EFB100' : '#e11d48'
                    }}>
                      {(metrics.average_engagement_score || 0).toFixed(0)}
                    </div>
                    <span className="text-[#868686]">/ 100</span>
                  </div>
                </div>
                <div>
                  <p className="text-[#868686] text-sm">Avg Views per Video</p>
                  <p className="text-[#FFF] text-xl font-bold number-display">
                    {formatNumber(metrics.average_views_per_video)}
                  </p>
                </div>
              </div>
            </div>

            <div className="p-6 bg-[#202020] border border-white/10 rounded-xl shadow-inner-soft">
              <h3 className="text-xl font-normal mb-4 text-[#FFF]">Content Quality</h3>
              <div className="space-y-3">
                <div>
                  <p className="text-[#868686] text-sm">Title Effectiveness</p>
                  <div className="w-full bg-[#404040] rounded-full h-2 mt-2">
                    <div 
                      className="bg-[#ea580c] h-2 rounded-full transition-all duration-500"
                      style={{ width: `${metrics.average_title_effectiveness || 0}%` }}
                    />
                  </div>
                  <p className="text-[#FFF] text-sm mt-1">{(metrics.average_title_effectiveness || 0).toFixed(0)}%</p>
                </div>
                <div>
                  <p className="text-[#868686] text-sm">SEO Optimization</p>
                  <div className="w-full bg-[#404040] rounded-full h-2 mt-2">
                    <div 
                      className="bg-[#2667e5] h-2 rounded-full transition-all duration-500"
                      style={{ width: `${metrics.average_seo_score || 0}%` }}
                    />
                  </div>
                  <p className="text-[#FFF] text-sm mt-1">{(metrics.average_seo_score || 0).toFixed(0)}%</p>
                </div>
              </div>
            </div>
          </>
        ) : channelData && (
          <div className="col-span-2 p-6 bg-[#202020] border border-white/10 rounded-xl shadow-inner-soft">
            <div className="text-center text-[#868686]">
              <p className="text-lg mb-2">⚠️ Limited Analysis Available</p>
              <p className="text-sm">This channel has very few or no accessible videos.</p>
              <p className="text-sm">Metrics cannot be calculated without sufficient video data.</p>
            </div>
          </div>
        )}
      </div>
    );
  };

  const renderVideos = () => {
    const videos = channelData?.top_videos || searchResults?.data?.videos || [];
    
    return (
      <div className="space-y-4">
        <h3 className="text-2xl font-normal text-[#FFF] mb-4">
          {channelData ? 'Top Analyzed Videos' : 'Search Results'}
        </h3>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
          {videos.map((item: any, index: number) => {
            const video = item.video || item;
            const analysis = item.title_analysis || item.analysis;
            const engagement = item.engagement_prediction;
            
            return (
              <VideoCard
                key={video.video_id || video.id || index}
                video={video}
                analysis={analysis}
                engagement={engagement}
                onClick={() => setSelectedVideo(item)}
              />
            );
          })}
        </div>
      </div>
    );
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="loader"></div>
      </div>
    );
  }

  if (!channelData && !searchResults) {
    return (
      <div className="text-center text-[#868686] py-12">
        <p>Search for content to see analysis results</p>
      </div>
    );
  }

  return (
    <div className="w-full max-w-7xl mx-auto space-y-6 fade-in">
      <div className="p-6 glassmorphism rounded-xl">
        <div className="flex gap-4 mb-6 overflow-x-auto">
          <button
            onClick={() => setActiveTab('overview')}
            className={`px-6 py-2 rounded-full font-semibold transition-all duration-200 whitespace-nowrap ${
              activeTab === 'overview'
                ? 'bg-[#ea580c] text-white'
                : 'border border-[#868686] text-[#868686] hover:border-[#FFF] hover:text-[#FFF]'
            }`}
          >
            Overview
          </button>
          <button
            onClick={() => setActiveTab('videos')}
            className={`px-6 py-2 rounded-full font-semibold transition-all duration-200 whitespace-nowrap ${
              activeTab === 'videos'
                ? 'bg-[#ea580c] text-white'
                : 'border border-[#868686] text-[#868686] hover:border-[#FFF] hover:text-[#FFF]'
            }`}
          >
            Videos
          </button>
          <button
            onClick={() => setActiveTab('patterns')}
            className={`px-6 py-2 rounded-full font-semibold transition-all duration-200 whitespace-nowrap ${
              activeTab === 'patterns'
                ? 'bg-[#ea580c] text-white'
                : 'border border-[#868686] text-[#868686] hover:border-[#FFF] hover:text-[#FFF]'
            }`}
          >
            Patterns
          </button>
          <button
            onClick={() => setActiveTab('viral')}
            className={`px-6 py-2 rounded-full font-semibold transition-all duration-200 whitespace-nowrap ${
              activeTab === 'viral'
                ? 'bg-[#ea580c] text-white'
                : 'border border-[#868686] text-[#868686] hover:border-[#FFF] hover:text-[#FFF]'
            }`}
          >
            Viral Insights
          </button>
        </div>

        <div className="min-h-[400px]">
          {activeTab === 'overview' && renderOverview()}
          {activeTab === 'videos' && renderVideos()}
          {activeTab === 'patterns' && (
            <PatternAnalysis 
              patterns={channelData?.content_patterns || searchResults?.data?.patterns}
            />
          )}
          {activeTab === 'viral' && (
            <ViralInsights 
              data={channelData || searchResults?.data}
            />
          )}
        </div>
      </div>

      {selectedVideo && (
        <div className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-[#202020] border border-white/10 rounded-xl p-6 max-w-4xl w-full max-h-[90vh] overflow-y-auto scrollbar-custom">
            <div className="flex justify-between items-start mb-4">
              <h3 className="text-2xl font-normal text-[#FFF] pr-4">Video Analysis</h3>
              <button
                onClick={() => setSelectedVideo(null)}
                className="text-[#868686] hover:text-[#FFF] transition-colors"
              >
                ✕
              </button>
            </div>
            
            <div className="space-y-4">
              <div>
                <h4 className="text-lg font-semibold text-[#FFF] mb-2">
                  {selectedVideo.video?.title || selectedVideo.title}
                </h4>
                <p className="text-[#868686]">
                  Views: {formatNumber(selectedVideo.video?.view_count || selectedVideo.view_count)}
                </p>
              </div>

              {selectedVideo.title_analysis && (
                <div className="p-4 bg-black/20 rounded-lg">
                  <h5 className="text-[#ea580c] font-semibold mb-2">Title Analysis</h5>
                  <div className="space-y-2 text-sm">
                    <p className="text-[#868686]">
                      Effectiveness Score: <span className="text-[#FFF] font-bold">
                        {selectedVideo.title_analysis.effectiveness_score}/100
                      </span>
                    </p>
                    <p className="text-[#868686]">
                      Patterns Found: <span className="text-[#FFF]">
                        {selectedVideo.title_analysis.patterns?.join(', ') || 'None'}
                      </span>
                    </p>
                    {selectedVideo.title_analysis.suggestions?.length > 0 && (
                      <div>
                        <p className="text-[#868686] mb-1">Suggestions:</p>
                        <ul className="list-disc list-inside text-[#FFF]">
                          {selectedVideo.title_analysis.suggestions.map((s: string, i: number) => (
                            <li key={i}>{s}</li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </div>
                </div>
              )}

              {selectedVideo.engagement_prediction && (
                <div className="p-4 bg-black/20 rounded-lg">
                  <h5 className="text-[#2667e5] font-semibold mb-2">Engagement Prediction</h5>
                  <div className="space-y-2 text-sm">
                    <p className="text-[#868686]">
                      Score: <span className="text-[#FFF] font-bold">
                        {selectedVideo.engagement_prediction.engagement_score}/100
                      </span>
                    </p>
                    <p className="text-[#868686]">
                      Tier: <span className="text-[#FFF]">
                        {selectedVideo.engagement_prediction.performance_tier}
                      </span>
                    </p>
                    {selectedVideo.engagement_prediction.positive_factors?.length > 0 && (
                      <div>
                        <p className="text-[#2eb872] mb-1">Positive Factors:</p>
                        <ul className="list-disc list-inside text-[#FFF]">
                          {selectedVideo.engagement_prediction.positive_factors.map((f: string, i: number) => (
                            <li key={i}>{f}</li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ChannelDashboard;