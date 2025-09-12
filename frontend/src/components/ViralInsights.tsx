import React from 'react';

interface ViralInsightsProps {
  data: any;
}

const ViralInsights: React.FC<ViralInsightsProps> = ({ data }) => {
  console.log('ViralInsights component rendered with data:', data);
  
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
      {/* Feature 1: Hook Analysis with Takeaways */}
      <div className="bg-[#202020] border border-white/10 rounded-lg p-6">
        <h3 className="text-xl font-bold text-white mb-4">🎯 Hook Analysis</h3>
        
        {videoInsights.length > 0 ? (
          <div className="space-y-4">
            {videoInsights.map((video: any, idx: number) => (
              <div key={idx} className="border-l-4 border-blue-500 pl-4">
                <p className="font-semibold text-sm mb-2 text-gray-300 break-words">
                  {video.title || 'Unknown video'}
                </p>
                {video.hooks ? (
                  <div className="space-y-2">
                    <div className="flex items-center gap-2 mb-2">
                      <span className="text-xs bg-blue-900/30 text-blue-400 px-2 py-1 rounded">
                        Hook Score: {video.hooks.hook_effectiveness_score?.toFixed(2) || 0}/100
                      </span>
                      {video.hooks.has_power_hook && (
                        <span className="text-xs bg-green-900/30 text-green-400 px-2 py-1 rounded">
                          Power Hook ✓
                        </span>
                      )}
                    </div>
                    
                    {/* Hook Takeaways */}
                    {video.hooks.takeaways && video.hooks.takeaways.length > 0 && (
                      <div className="bg-[#1a1a1a] rounded p-3 space-y-1">
                        <p className="text-xs font-semibold text-gray-400 mb-1">Why this hook works:</p>
                        {video.hooks.takeaways.map((takeaway: string, tidx: number) => (
                          <p key={tidx} className="text-xs text-gray-300 leading-relaxed">
                            • {takeaway}
                          </p>
                        ))}
                      </div>
                    )}
                    
                    {/* Emotional Triggers */}
                    {video.hooks.emotions_triggered && video.hooks.emotions_triggered.length > 0 && (
                      <div className="flex gap-1 flex-wrap mt-2">
                        {video.hooks.emotions_triggered.map((emotion: any, eidx: number) => (
                          <span key={eidx} className="text-xs bg-purple-900/30 text-purple-400 px-2 py-1 rounded">
                            {emotion.emotion}: {emotion.trigger_word}
                          </span>
                        ))}
                      </div>
                    )}
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

      {/* Feature 2: Title Performance with Insights */}
      <div className="bg-[#202020] border border-white/10 rounded-lg p-6">
        <h3 className="text-xl font-bold text-white mb-4">📊 Title Performance Analysis</h3>
        
        {videoInsights.length > 0 ? (
          <div className="space-y-3">
            {videoInsights.slice(0, 3).map((video: any, idx: number) => (
              <div key={idx} className="bg-[#2a2a2a] p-4 rounded border border-white/5">
                <p className="font-semibold text-sm mb-3 text-gray-300 break-words">
                  {video.titleOptimization?.full_title || video.title || 'Unknown video'}
                </p>
                {video.titleOptimization ? (
                  <div className="space-y-2">
                    <div className="flex gap-2 flex-wrap">
                      <span className="text-xs bg-green-900/30 text-green-400 px-2 py-1 rounded">
                        Score: {video.titleOptimization.optimization_score?.toFixed(2) || 0}/100
                      </span>
                      <span className="text-xs bg-blue-900/30 text-blue-400 px-2 py-1 rounded">
                        {video.titleOptimization.length_analysis?.word_count || 0} words
                      </span>
                      <span className="text-xs bg-yellow-900/30 text-yellow-400 px-2 py-1 rounded">
                        {video.titleOptimization.length_analysis?.char_count || 0} chars
                      </span>
                    </div>
                    
                    {/* Performance Insights */}
                    {video.titleOptimization.performance_insights && video.titleOptimization.performance_insights.length > 0 && (
                      <div className="bg-[#1a1a1a] rounded p-3 space-y-1">
                        <p className="text-xs font-semibold text-gray-400 mb-1">Why this title performs:</p>
                        {video.titleOptimization.performance_insights.map((insight: string, iidx: number) => (
                          <p key={iidx} className="text-xs text-gray-300 leading-relaxed">
                            • {insight}
                          </p>
                        ))}
                      </div>
                    )}
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

      {/* Feature 3: Content Templates - Actual Templates */}
      <div className="bg-[#202020] border border-white/10 rounded-lg p-6">
        <h3 className="text-xl font-bold text-white mb-4">📝 Content Templates</h3>
        
        {content_templates ? (
          <div className="space-y-4">
            {/* Ready to Use Templates */}
            {content_templates.ready_to_use_templates && content_templates.ready_to_use_templates.length > 0 && (
              <div className="space-y-3">
                {content_templates.ready_to_use_templates.slice(0, 3).map((template: any, idx: number) => (
                  <div key={idx} className="bg-[#2a2a2a] p-4 rounded border border-white/5">
                    <h5 className="font-bold text-sm text-yellow-400 mb-2">{template.name}</h5>
                    <div className="bg-[#1a1a1a] p-2 rounded mb-2">
                      <code className="text-xs text-green-400">{template.fill_in}</code>
                    </div>
                    <p className="text-xs text-gray-400 mb-2">{template.instructions}</p>
                    <div className="space-y-1">
                      <p className="text-xs font-semibold text-gray-500">Examples:</p>
                      {template.examples?.map((example: string, eidx: number) => (
                        <p key={eidx} className="text-xs text-gray-300 pl-2">• {example}</p>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            )}
            
            {/* Copy-Paste Formulas */}
            {content_templates.copy_paste_formulas && content_templates.copy_paste_formulas.length > 0 && (
              <div>
                <h4 className="font-semibold text-sm text-gray-300 mb-2">Quick Copy Templates</h4>
                <div className="space-y-1">
                  {content_templates.copy_paste_formulas.slice(0, 5).map((formula: string, idx: number) => (
                    <div key={idx} className="bg-[#2a2a2a] p-2 rounded text-xs text-gray-300 font-mono">
                      {formula}
                    </div>
                  ))}
                </div>
              </div>
            )}
            
            {/* Title Starters */}
            {content_templates.title_starters && content_templates.title_starters.length > 0 && (
              <div>
                <h4 className="font-semibold text-sm text-gray-300 mb-2">Proven Title Starters</h4>
                <div className="flex flex-wrap gap-1">
                  {content_templates.title_starters.slice(0, 8).map((starter: string, idx: number) => (
                    <span key={idx} className="text-xs bg-blue-900/30 text-blue-400 px-2 py-1 rounded">
                      {starter}
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

      {/* Feature 4: Viral Recipes with Concrete Examples */}
      <div className="bg-[#202020] border border-white/10 rounded-lg p-6">
        <h3 className="text-xl font-bold text-white mb-4">🚀 Viral Content Recipes</h3>
        
        {viral_recipes && viral_recipes.viral_recipes && viral_recipes.viral_recipes.length > 0 ? (
          <div className="space-y-4">
            {viral_recipes.viral_recipes.slice(0, 3).map((recipe: any, idx: number) => (
              <div key={idx} className="bg-purple-900/10 border border-purple-500/30 rounded-lg p-4">
                <h5 className="font-bold text-purple-400 mb-2">{recipe.name}</h5>
                <p className="text-xs text-gray-400 mb-3">{recipe.formula}</p>
                
                {/* Concrete Example */}
                {recipe.concrete_example && (
                  <div className="bg-[#1a1a1a] rounded p-3 mb-3">
                    <p className="text-xs font-semibold text-gray-400 mb-2">Real Example:</p>
                    {Object.entries(recipe.concrete_example).map(([key, value]: [string, any]) => (
                      <p key={key} className="text-xs text-gray-300 mb-1">
                        <span className="text-purple-400">{key}:</span> {value}
                      </p>
                    ))}
                  </div>
                )}
                
                {/* Emotional Triggers */}
                {recipe.emotional_triggers && recipe.emotional_triggers.length > 0 && (
                  <div className="mb-3">
                    <p className="text-xs font-semibold text-gray-400 mb-2">Triggers:</p>
                    <div className="space-y-1">
                      {recipe.emotional_triggers.map((trigger: string, tidx: number) => (
                        <p key={tidx} className="text-xs text-gray-300">• {trigger}</p>
                      ))}
                    </div>
                  </div>
                )}
                
                {/* How to Apply */}
                {recipe.how_to_apply && (
                  <div className="mb-3">
                    <p className="text-xs font-semibold text-gray-400 mb-1">How to Apply:</p>
                    <p className="text-xs text-gray-300 whitespace-pre-line">{recipe.how_to_apply}</p>
                  </div>
                )}
                
                {/* Expected CTR */}
                {recipe.expected_ctr && (
                  <span className="text-xs bg-green-900/30 text-green-400 px-2 py-1 rounded">
                    Expected CTR: {recipe.expected_ctr}
                  </span>
                )}
              </div>
            ))}
            
            {/* Quick Wins */}
            {viral_recipes.quick_wins && viral_recipes.quick_wins.length > 0 && (
              <div className="mt-4">
                <h5 className="font-bold text-sm text-gray-300 mb-3">⚡ Quick Wins</h5>
                <div className="space-y-2">
                  {viral_recipes.quick_wins.map((win: any, idx: number) => (
                    <div key={idx} className="bg-[#2a2a2a] p-3 rounded">
                      <div className="flex justify-between items-start mb-1">
                        <p className="text-xs font-semibold text-yellow-400">{win.tip || win}</p>
                        {win.impact && (
                          <span className="text-xs bg-green-900/30 text-green-400 px-2 py-1 rounded">
                            {win.impact}
                          </span>
                        )}
                      </div>
                      {win.why && (
                        <p className="text-xs text-gray-400 mb-1">{win.why}</p>
                      )}
                      {win.example && (
                        <p className="text-xs text-gray-300 italic">Example: {win.example}</p>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        ) : (
          <p className="text-gray-400">No viral recipes available</p>
        )}
      </div>
    </div>
  );
};

export default ViralInsights;