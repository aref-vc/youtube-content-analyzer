import React from 'react';

interface VideoCardProps {
  video: any;
  analysis?: any;
  engagement?: any;
  onClick?: () => void;
}

const VideoCard: React.FC<VideoCardProps> = ({ video, analysis, engagement, onClick }) => {
  const formatNumber = (num: number | undefined): string => {
    if (!num) return '0';
    if (num >= 1000000) return `${(num / 1000000).toFixed(1)}M`;
    if (num >= 1000) return `${(num / 1000).toFixed(1)}K`;
    return num.toString();
  };

  const formatDuration = (seconds: number | undefined): string => {
    if (!seconds) return 'N/A';
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;
    
    if (hours > 0) {
      return `${hours}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    }
    return `${minutes}:${secs.toString().padStart(2, '0')}`;
  };

  const getScoreColor = (score: number): string => {
    if (score >= 70) return '#2eb872';
    if (score >= 40) return '#EFB100';
    return '#e11d48';
  };

  return (
    <div 
      className="p-6 bg-[#202020] border border-white/10 rounded-xl shadow-inner-soft hover:border-white/20 transition-all duration-200 cursor-pointer"
      onClick={onClick}
    >
      <div className="space-y-3">
        <h4 className="text-lg font-semibold text-[#FFF] line-clamp-2 hover:text-[#ea580c] transition-colors">
          {video.title}
        </h4>
        
        <div className="flex items-center gap-4 text-sm text-[#868686]">
          <span className="flex items-center gap-1">
            <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
              <path d="M10 12a2 2 0 100-4 2 2 0 000 4z" />
              <path fillRule="evenodd" d="M.458 10C1.732 5.943 5.522 3 10 3s8.268 2.943 9.542 7c-1.274 4.057-5.064 7-9.542 7S1.732 14.057.458 10zM14 10a4 4 0 11-8 0 4 4 0 018 0z" clipRule="evenodd" />
            </svg>
            {formatNumber(video.view_count)}
          </span>
          
          {video.like_count !== undefined && (
            <span className="flex items-center gap-1">
              <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                <path d="M2 10.5a1.5 1.5 0 113 0v6a1.5 1.5 0 01-3 0v-6zM6 10.333v5.43a2 2 0 001.106 1.79l.05.025A4 4 0 008.943 18h5.416a2 2 0 001.962-1.608l1.2-6A2 2 0 0015.56 8H12V4a2 2 0 00-2-2 1 1 0 00-1 1v.667a4 4 0 01-.8 2.4L6.8 7.933a4 4 0 00-.8 2.4z" />
              </svg>
              {formatNumber(video.like_count)}
            </span>
          )}
          
          {video.duration !== undefined && (
            <span className="flex items-center gap-1">
              <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clipRule="evenodd" />
              </svg>
              {formatDuration(video.duration)}
            </span>
          )}
        </div>

        {video.channel && (
          <p className="text-sm text-[#868686]">
            Channel: <span className="text-[#FFF]">{video.channel}</span>
          </p>
        )}

        {(analysis || engagement) && (
          <div className="pt-3 border-t border-white/10 space-y-2">
            {analysis?.effectiveness_score !== undefined && (
              <div className="flex items-center justify-between">
                <span className="text-xs text-[#868686]">Title Effectiveness</span>
                <div className="flex items-center gap-2">
                  <div className="w-24 bg-[#404040] rounded-full h-1.5">
                    <div 
                      className="h-1.5 rounded-full transition-all duration-500"
                      style={{ 
                        width: `${analysis.effectiveness_score}%`,
                        backgroundColor: getScoreColor(analysis.effectiveness_score)
                      }}
                    />
                  </div>
                  <span className="text-xs font-bold number-display" style={{ color: getScoreColor(analysis.effectiveness_score) }}>
                    {analysis.effectiveness_score}
                  </span>
                </div>
              </div>
            )}

            {engagement?.engagement_score !== undefined && (
              <div className="flex items-center justify-between">
                <span className="text-xs text-[#868686]">Engagement Prediction</span>
                <div className="flex items-center gap-2">
                  <div className="w-24 bg-[#404040] rounded-full h-1.5">
                    <div 
                      className="h-1.5 rounded-full transition-all duration-500"
                      style={{ 
                        width: `${engagement.engagement_score}%`,
                        backgroundColor: getScoreColor(engagement.engagement_score)
                      }}
                    />
                  </div>
                  <span className="text-xs font-bold number-display" style={{ color: getScoreColor(engagement.engagement_score) }}>
                    {engagement.engagement_score}
                  </span>
                </div>
              </div>
            )}

            {analysis?.patterns && analysis.patterns.length > 0 && (
              <div className="flex flex-wrap gap-1 mt-2">
                {analysis.patterns.slice(0, 3).map((pattern: string, index: number) => (
                  <span 
                    key={index}
                    className="px-2 py-0.5 text-xs bg-[#ea580c]/20 text-[#ea580c] rounded-full"
                  >
                    {pattern}
                  </span>
                ))}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default VideoCard;