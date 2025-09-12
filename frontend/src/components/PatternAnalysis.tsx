import React, { useEffect, useRef } from 'react';
import * as d3 from 'd3';

interface PatternAnalysisProps {
  patterns: any;
}

const PatternAnalysis: React.FC<PatternAnalysisProps> = ({ patterns }) => {
  const barChartRef = useRef<SVGSVGElement>(null);
  const topicsChartRef = useRef<SVGSVGElement>(null);

  useEffect(() => {
    if (patterns?.common_patterns) {
      drawPatternChart();
    }
    if (patterns?.main_topics) {
      drawTopicsChart();
    }
  }, [patterns]);

  const drawPatternChart = () => {
    if (!barChartRef.current || !patterns?.common_patterns) return;

    const data = Object.entries(patterns.common_patterns).map(([pattern, count]) => ({
      pattern,
      count: count as number
    }));

    const svg = d3.select(barChartRef.current);
    svg.selectAll("*").remove();

    const width = 600;
    const height = 300;
    const margin = { top: 20, right: 30, bottom: 60, left: 60 };
    const innerWidth = width - margin.left - margin.right;
    const innerHeight = height - margin.top - margin.bottom;

    svg.attr("viewBox", `0 0 ${width} ${height}`);

    const g = svg.append("g")
      .attr("transform", `translate(${margin.left},${margin.top})`);

    const x = d3.scaleBand()
      .domain(data.map(d => d.pattern))
      .range([0, innerWidth])
      .padding(0.2);

    const y = d3.scaleLinear()
      .domain([0, d3.max(data, d => d.count) || 0])
      .range([innerHeight, 0]);

    // Bars
    g.selectAll(".bar")
      .data(data)
      .enter().append("rect")
      .attr("class", "bar")
      .attr("x", d => x(d.pattern) || 0)
      .attr("y", d => y(d.count))
      .attr("width", x.bandwidth())
      .attr("height", d => innerHeight - y(d.count))
      .attr("fill", "#ea580c");

    // X axis
    g.append("g")
      .attr("transform", `translate(0,${innerHeight})`)
      .call(d3.axisBottom(x))
      .selectAll("text")
      .style("text-anchor", "end")
      .attr("dx", "-.8em")
      .attr("dy", ".15em")
      .attr("transform", "rotate(-45)")
      .style("fill", "#868686")
      .style("font-family", "JetBrains Mono")
      .style("font-size", "12px");

    // Y axis
    g.append("g")
      .call(d3.axisLeft(y).ticks(5))
      .selectAll("text")
      .style("fill", "#868686")
      .style("font-family", "JetBrains Mono")
      .style("font-size", "12px");

    g.selectAll(".domain, .tick line")
      .style("stroke", "#404040");
  };

  const drawTopicsChart = () => {
    if (!topicsChartRef.current || !patterns?.main_topics) return;

    const data = patterns.main_topics.slice(0, 10).map(([topic, count]: [string, number]) => ({
      topic,
      count
    }));

    const svg = d3.select(topicsChartRef.current);
    svg.selectAll("*").remove();

    const width = 600;
    const height = 300;
    const margin = { top: 20, right: 150, bottom: 20, left: 60 };
    const innerWidth = width - margin.left - margin.right;
    const innerHeight = height - margin.top - margin.bottom;

    svg.attr("viewBox", `0 0 ${width} ${height}`);

    const g = svg.append("g")
      .attr("transform", `translate(${margin.left},${margin.top})`);

    const x = d3.scaleLinear()
      .domain([0, d3.max(data, d => d.count) || 0])
      .range([0, innerWidth]);

    const y = d3.scaleBand()
      .domain(data.map(d => d.topic))
      .range([0, innerHeight])
      .padding(0.2);

    // Bars
    g.selectAll(".bar")
      .data(data)
      .enter().append("rect")
      .attr("class", "bar")
      .attr("x", 0)
      .attr("y", d => y(d.topic) || 0)
      .attr("width", d => x(d.count))
      .attr("height", y.bandwidth())
      .attr("fill", "#2667e5");

    // Labels
    g.selectAll(".label")
      .data(data)
      .enter().append("text")
      .attr("x", d => x(d.count) + 5)
      .attr("y", d => (y(d.topic) || 0) + y.bandwidth() / 2)
      .attr("dy", "0.35em")
      .text(d => d.count)
      .style("fill", "#FFF")
      .style("font-family", "JetBrains Mono")
      .style("font-size", "12px");

    // Y axis
    g.append("g")
      .call(d3.axisLeft(y))
      .selectAll("text")
      .style("fill", "#868686")
      .style("font-family", "JetBrains Mono")
      .style("font-size", "12px");

    g.selectAll(".domain, .tick line")
      .style("stroke", "#404040");
  };

  if (!patterns) {
    return (
      <div className="text-center text-[#868686] py-12">
        <p>No pattern data available</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {patterns.common_patterns && (
          <div className="p-6 bg-[#202020] border border-white/10 rounded-xl shadow-inner-soft">
            <h3 className="text-xl font-normal text-[#FFF] mb-4">Common Title Patterns</h3>
            <svg ref={barChartRef} className="w-full"></svg>
          </div>
        )}

        {patterns.main_topics && (
          <div className="p-6 bg-[#202020] border border-white/10 rounded-xl shadow-inner-soft">
            <h3 className="text-xl font-normal text-[#FFF] mb-4">Top Topics</h3>
            <svg ref={topicsChartRef} className="w-full"></svg>
          </div>
        )}
      </div>

      {patterns.performance_patterns && patterns.performance_patterns.length > 0 && (
        <div className="p-6 bg-[#202020] border border-white/10 rounded-xl shadow-inner-soft">
          <h3 className="text-xl font-normal text-[#FFF] mb-4">Performance Patterns</h3>
          <div className="space-y-3">
            {patterns.performance_patterns.map((pattern: any, index: number) => (
              <div key={index} className="flex items-center justify-between p-3 bg-black/20 rounded-lg">
                <div>
                  <p className="text-[#FFF] font-semibold capitalize">{pattern.pattern}</p>
                  <p className="text-sm text-[#868686]">Used in {pattern.video_count} videos</p>
                </div>
                <div className="text-right">
                  <p className="text-2xl font-bold number-display text-[#2eb872]">
                    {(pattern.avg_views / 1000).toFixed(0)}K
                  </p>
                  <p className="text-xs text-[#868686]">avg views</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {patterns.average_title_length !== undefined && (
          <div className="p-4 bg-[#202020] border border-white/10 rounded-xl shadow-inner-soft">
            <p className="text-[#868686] text-sm mb-2">Avg Title Length</p>
            <p className="text-3xl font-bold number-display text-[#FFF]">
              {patterns.average_title_length.toFixed(1)}
            </p>
            <p className="text-xs text-[#868686] mt-1">words per title</p>
          </div>
        )}

        {patterns.content_consistency !== undefined && (
          <div className="p-4 bg-[#202020] border border-white/10 rounded-xl shadow-inner-soft">
            <p className="text-[#868686] text-sm mb-2">Content Consistency</p>
            <p className="text-3xl font-bold number-display" style={{
              color: patterns.content_consistency > 70 ? '#2eb872' : 
                     patterns.content_consistency > 40 ? '#EFB100' : '#e11d48'
            }}>
              {patterns.content_consistency.toFixed(0)}%
            </p>
            <p className="text-xs text-[#868686] mt-1">topic alignment</p>
          </div>
        )}

        {patterns.videos_analyzed && (
          <div className="p-4 bg-[#202020] border border-white/10 rounded-xl shadow-inner-soft">
            <p className="text-[#868686] text-sm mb-2">Videos Analyzed</p>
            <p className="text-3xl font-bold number-display text-[#FFF]">
              {patterns.videos_analyzed}
            </p>
            <p className="text-xs text-[#868686] mt-1">for patterns</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default PatternAnalysis;