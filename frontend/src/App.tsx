import React, { useState } from 'react';
import SearchInterface from './components/SearchInterface';
import ChannelDashboard from './components/ChannelDashboard';

function App() {
  const [searchResults, setSearchResults] = useState<any>(null);
  const [selectedChannel, setSelectedChannel] = useState<string | null>(null);

  const handleSearchResults = (results: any) => {
    console.log('Search results received:', results);
    setSearchResults(results);
    setSelectedChannel(null);
  };

  const handleChannelSelect = (channelUrl: string) => {
    setSelectedChannel(channelUrl);
  };

  return (
    <div className="min-h-screen bg-[#191919] p-8">
      <div className="max-w-7xl mx-auto">
        <div className="mb-8">
          <SearchInterface onSearchResults={handleSearchResults} />
        </div>

        {searchResults?.data?.top_channels && searchResults.data.top_channels.length > 0 && !selectedChannel && (
          <div className="mt-8 p-6 glassmorphism rounded-xl">
            <h3 className="text-2xl font-normal text-[#FFF] mb-4">Top Channels for "{searchResults.data.query}"</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {searchResults.data.top_channels.map((channel: any, index: number) => (
                <div 
                  key={index}
                  className="p-4 bg-[#202020] border border-white/10 rounded-xl shadow-inner-soft hover:border-white/20 transition-all duration-200 cursor-pointer"
                  onClick={() => handleChannelSelect(channel.channel_url)}
                >
                  <h4 className="text-lg font-semibold text-[#FFF] mb-2">{channel.channel_name}</h4>
                  <p className="text-sm text-[#868686]">Click to analyze channel</p>
                </div>
              ))}
            </div>
          </div>
        )}

        {(searchResults || selectedChannel) && (
          <div className="mt-8">
            <ChannelDashboard 
              channelUrl={selectedChannel || undefined}
              searchResults={searchResults}
            />
          </div>
        )}
      </div>
    </div>
  );
}

export default App;