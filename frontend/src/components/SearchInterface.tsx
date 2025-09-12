import React, { useState } from 'react';
import { youtubeAPI, SearchRequest } from '../services/api';

interface SearchInterfaceProps {
  onSearchResults: (results: any) => void;
}

const SearchInterface: React.FC<SearchInterfaceProps> = ({ onSearchResults }) => {
  const [query, setQuery] = useState('');
  const [searchType, setSearchType] = useState<'topic' | 'channel'>('topic');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;

    setIsLoading(true);
    setError(null);

    try {
      const request: SearchRequest = {
        query: query.trim(),
        search_type: searchType,
        max_results: 20,
        analyze_content: true,
      };

      const response = await youtubeAPI.search(request);
      onSearchResults(response);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Search failed. Please try again.');
      console.error('Search error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="w-full max-w-4xl mx-auto p-8 glassmorphism rounded-xl shadow-inner-soft fade-in">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-3xl font-medium uppercase text-[#FFF]">YouTube Content Analyzer</h2>
        <span className="text-xs font-mono text-[#404040] opacity-40">FalconHQ</span>
      </div>

      <form onSubmit={handleSearch} className="space-y-6">
        <div className="space-y-4">
          <div className="flex gap-4">
            <button
              type="button"
              onClick={() => setSearchType('topic')}
              className={`px-6 py-2 rounded-full font-semibold transition-all duration-200 ${
                searchType === 'topic'
                  ? 'bg-[#ea580c] text-white'
                  : 'border border-[#ea580c] text-[#ea580c] hover:bg-[#ea580c] hover:text-white'
              } focus:outline-none focus:ring-2 focus:ring-[#ea580c] focus:ring-opacity-50`}
            >
              Search by Topic
            </button>
            <button
              type="button"
              onClick={() => setSearchType('channel')}
              className={`px-6 py-2 rounded-full font-semibold transition-all duration-200 ${
                searchType === 'channel'
                  ? 'bg-[#ea580c] text-white'
                  : 'border border-[#ea580c] text-[#ea580c] hover:bg-[#ea580c] hover:text-white'
              } focus:outline-none focus:ring-2 focus:ring-[#ea580c] focus:ring-opacity-50`}
            >
              Search by Channel
            </button>
          </div>

          <div className="relative">
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder={
                searchType === 'topic'
                  ? 'Enter a topic (e.g., "React tutorials", "cooking tips")'
                  : 'Enter channel name or URL'
              }
              className="w-full px-6 py-4 bg-[#202020] border border-white/10 rounded-xl text-[#FFF] placeholder-[#868686] 
                         transition-all duration-200 hover:border-white/20 shadow-inner-soft
                         focus:border-[#ea580c] focus:outline-none focus:ring-2 focus:ring-[#ea580c] focus:ring-opacity-30"
              disabled={isLoading}
            />
            {isLoading && (
              <div className="absolute right-4 top-1/2 transform -translate-y-1/2">
                <div className="loader w-6 h-6"></div>
              </div>
            )}
          </div>

          {error && (
            <div className="p-4 bg-[#e11d48]/10 border border-[#e11d48] rounded-lg text-[#e11d48] fade-in">
              {error}
            </div>
          )}

          <button
            type="submit"
            disabled={isLoading || !query.trim()}
            className={`w-full px-8 py-4 rounded-xl font-semibold text-lg transition-all duration-200 ${
              isLoading || !query.trim()
                ? 'bg-[#404040] text-[#868686] cursor-not-allowed'
                : 'bg-[#ea580c] text-white hover:bg-[#c2410c] hover:shadow-glow-primary focus:outline-none focus:ring-2 focus:ring-[#ea580c] focus:ring-opacity-50'
            }`}
          >
            {isLoading ? 'Analyzing...' : 'Analyze Content'}
          </button>
        </div>
      </form>

      <div className="mt-8 p-4 bg-black/20 backdrop-blur-sm border border-white/10 rounded-xl">
        <h3 className="text-xl font-normal mb-3 text-[#FFF]">What this analyzes:</h3>
        <ul className="space-y-2 text-[#868686]">
          {searchType === 'topic' ? (
            <>
              <li className="flex items-start gap-2">
                <span className="text-[#2eb872] mt-1">•</span>
                <span>Top performing videos on this topic</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-[#2eb872] mt-1">•</span>
                <span>Leading channels in this niche</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-[#2eb872] mt-1">•</span>
                <span>Title patterns that drive engagement</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-[#2eb872] mt-1">•</span>
                <span>Content strategies that work</span>
              </li>
            </>
          ) : (
            <>
              <li className="flex items-start gap-2">
                <span className="text-[#2667e5] mt-1">•</span>
                <span>Channel performance metrics</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-[#2667e5] mt-1">•</span>
                <span>Most engaging video patterns</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-[#2667e5] mt-1">•</span>
                <span>Title and description optimization</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-[#2667e5] mt-1">•</span>
                <span>Content consistency analysis</span>
              </li>
            </>
          )}
        </ul>
      </div>
    </div>
  );
};

export default SearchInterface;