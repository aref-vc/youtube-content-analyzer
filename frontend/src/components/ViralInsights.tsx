import React from 'react';

interface ViralInsightsProps {
  data: any;
}

const ViralInsights: React.FC<ViralInsightsProps> = ({ data }) => {
  console.log('ViralInsights component rendered with data:', data);
  
  // Simple debug view first
  if (!data) {
    return (
      <div className="text-gray-400 p-6">
        <p>No data available for viral insights analysis.</p>
      </div>
    );
  }
  
  const { viral_insights, top_videos } = data;
  
  if (!viral_insights) {
    return (
      <div className="text-gray-400 p-6">
        <p>Viral insights data is not available yet. Please analyze a channel first.</p>
      </div>
    );
  }

  const { content_templates, viral_recipes } = viral_insights;

  // Get hook analysis from individual videos
  const videoInsights = top_videos?.slice(0, 5).map((video: any) => ({
    title: video.video?.title,
    hooks: video.viral_insights?.hooks,
    titleOptimization: video.viral_insights?.title_optimization
  })) || [];

  return (
    <div className="space-y-6">
      {/* Feature 1: Hook Analysis */}
      <div className="bg-[#202020] border border-white/10 rounded-lg p-6">
        <h3 className="text-xl font-bold text-white mb-4">🎯 Hook Analysis</h3>
        
        {videoInsights.length > 0 ? (
          <div className="space-y-4">
            {videoInsights.map((video: any, idx: number) => (
              <div key={idx} className="border-l-4 border-blue-500 pl-4">
                <p className="font-semibold text-sm mb-2 text-gray-300">
                  {video.title?.substring(0, 60) || 'Unknown video'}...
                </p>
                {video.hooks ? (
                  <div className="space-y-2">
                    <div className="flex items-center gap-2">
                      <span className="text-xs bg-blue-900/30 text-blue-400 px-2 py-1 rounded">
                        Hook Score: {video.hooks.hook_effectiveness_score || 0}/100
                      </span>
                    </div>
                  </div>
                ) : (
                  <p className="text-xs text-gray-500">No hook analysis available</p>
                )}
              </div>
            ))}
          </div>
        ) : (
          <p className="text-gray-400">No videos analyzed yet</p>
        )}
      </div>

      {/* Feature 2: Title Performance */}
      <div className="bg-[#202020] border border-white/10 rounded-lg p-6">
        <h3 className="text-xl font-bold text-white mb-4">📊 Title Performance Analysis</h3>
        
        {videoInsights.length > 0 ? (
          <div className="space-y-3">
            {videoInsights.slice(0, 3).map((video: any, idx: number) => (
              <div key={idx} className="bg-[#2a2a2a] p-3 rounded border border-white/5">
                <p className="font-semibold text-sm mb-2 text-gray-300">
                  {video.title?.substring(0, 50) || 'Unknown video'}...
                </p>
                {video.titleOptimization ? (
                  <div className="text-xs text-gray-400">
                    <p>Length Score: {video.titleOptimization.length_score || 0}%</p>
                    <p>Optimization Score: {video.titleOptimization.optimization_score || 0}%</p>
                  </div>
                ) : (
                  <p className="text-xs text-gray-500">No title analysis available</p>
                )}
              </div>
            ))}
          </div>
        ) : (
          <p className="text-gray-400">No videos to analyze</p>
        )}
      </div>

      {/* Feature 3: Content Templates */}
      <div className="bg-[#202020] border border-white/10 rounded-lg p-6">
        <h3 className="text-xl font-bold text-white mb-4">🔄 Content Templates</h3>
        
        {content_templates ? (
          <div className="space-y-4">
            {content_templates.power_words && content_templates.power_words.length > 0 && (
              <div>
                <h4 className="font-semibold text-sm text-gray-300 mb-2">Power Words Used</h4>
                <div className="flex flex-wrap gap-1">
                  {content_templates.power_words.slice(0, 10).map((word: string, idx: number) => (
                    <span key={idx} className="text-xs bg-yellow-900/30 text-yellow-400 px-2 py-1 rounded">
                      {word}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>
        ) : (
          <p className="text-gray-400">No content templates available</p>
        )}
      </div>

      {/* Feature 4: Viral Recipes */}
      <div className="bg-[#202020] border border-white/10 rounded-lg p-6">
        <h3 className="text-xl font-bold text-white mb-4">🚀 Viral Content Recipes</h3>
        
        {viral_recipes && viral_recipes.viral_recipes && viral_recipes.viral_recipes.length > 0 ? (
          <div className="space-y-3">
            {viral_recipes.viral_recipes.slice(0, 3).map((recipe: any, idx: number) => (
              <div key={idx} className="border-l-4 border-purple-500 pl-4 bg-purple-900/20 p-3 rounded">
                <h5 className="font-bold text-sm text-purple-400">{recipe.formula}</h5>
                <p className="text-xs text-gray-400 mt-1">{recipe.description}</p>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-gray-400">No viral recipes available</p>
        )}
      </div>
    </div>
  );
};

export default ViralInsights;