"use client"

import { useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { BarChart3, PieChart, TrendingUp, Activity, Clock, Users } from "lucide-react"

interface AnalyticsData {
  trustScoreDistribution: { range: string; percentage: number; count: number; color: string }[]
  hazardTypes: { type: string; percentage: number; count: number; trend: number }[]
  sourceReliability: { source: string; reliability: number; reports: number }[]
  trendingTopics: { topic: string; mentions: number; sentiment: "positive" | "negative" | "neutral"; change: number }[]
  timeSeriesData: { hour: string; reports: number; trustScore: number }[]
}

export default function AnalyticsCharts() {
  const [timeRange, setTimeRange] = useState("24h")

  const analyticsData: AnalyticsData = {
    trustScoreDistribution: [
      { range: "High (0.8-1.0)", percentage: 71, count: 892, color: "bg-green-500" },
      { range: "Medium (0.6-0.8)", percentage: 22, count: 275, color: "bg-yellow-500" },
      { range: "Low (0.0-0.6)", percentage: 7, count: 80, color: "bg-red-500" },
    ],
    hazardTypes: [
      { type: "High Waves", percentage: 34, count: 425, trend: 12 },
      { type: "Pollution", percentage: 28, count: 349, trend: -5 },
      { type: "Debris", percentage: 19, count: 237, trend: 8 },
      { type: "Temperature", percentage: 12, count: 150, trend: 15 },
      { type: "Other", percentage: 7, count: 86, trend: -2 },
    ],
    sourceReliability: [
      { source: "Citizen Reports", reliability: 0.78, reports: 847 },
      { source: "Social Media", reliability: 0.65, reports: 623 },
      { source: "Official Sensors", reliability: 0.95, reports: 156 },
      { source: "Coast Guard", reliability: 0.92, reports: 89 },
    ],
    trendingTopics: [
      { topic: "Mumbai Waves", mentions: 245, sentiment: "negative", change: 35 },
      { topic: "Goa Pollution", mentions: 189, sentiment: "negative", change: 12 },
      { topic: "Chennai Safety", mentions: 156, sentiment: "neutral", change: -8 },
      { topic: "Kochi Weather", mentions: 134, sentiment: "positive", change: 22 },
      { topic: "Ocean Temperature", mentions: 98, sentiment: "neutral", change: 45 },
    ],
    timeSeriesData: [
      { hour: "00:00", reports: 12, trustScore: 0.82 },
      { hour: "04:00", reports: 8, trustScore: 0.79 },
      { hour: "08:00", reports: 45, trustScore: 0.85 },
      { hour: "12:00", reports: 78, trustScore: 0.81 },
      { hour: "16:00", reports: 92, trustScore: 0.77 },
      { hour: "20:00", reports: 67, trustScore: 0.83 },
    ],
  }

  const getSentimentColor = (sentiment: string) => {
    switch (sentiment) {
      case "positive":
        return "text-green-600 bg-green-50"
      case "negative":
        return "text-red-600 bg-red-50"
      default:
        return "text-gray-600 bg-gray-50"
    }
  }

  const getTrendIcon = (trend: number) => {
    if (trend > 0) return <TrendingUp className="w-3 h-3 text-green-600" />
    if (trend < 0) return <TrendingUp className="w-3 h-3 text-red-600 rotate-180" />
    return <Activity className="w-3 h-3 text-gray-600" />
  }

  return (
    <div className="space-y-6">
      {/* Trust Score Distribution */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <CardTitle className="flex items-center space-x-2">
              <BarChart3 className="h-5 w-5 text-blue-600" />
              <span>Trust Score Distribution</span>
            </CardTitle>
            <Select value={timeRange} onValueChange={setTimeRange}>
              <SelectTrigger className="w-24">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="1h">1H</SelectItem>
                <SelectItem value="24h">24H</SelectItem>
                <SelectItem value="7d">7D</SelectItem>
                <SelectItem value="30d">30D</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {analyticsData.trustScoreDistribution.map((item, index) => (
              <div key={index} className="space-y-2">
                <div className="flex justify-between items-center">
                  <span className="text-sm text-gray-600">{item.range}</span>
                  <div className="flex items-center space-x-2">
                    <span className="text-sm font-medium">{item.percentage}%</span>
                    <span className="text-xs text-gray-500">({item.count})</span>
                  </div>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-3">
                  <div
                    className={`${item.color} h-3 rounded-full transition-all duration-500`}
                    style={{ width: `${item.percentage}%` }}
                  ></div>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Hazard Types Breakdown */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <PieChart className="h-5 w-5 text-teal-600" />
            <span>Hazard Types</span>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {analyticsData.hazardTypes.map((item, index) => (
              <div key={index} className="flex justify-between items-center p-2 rounded-lg hover:bg-gray-50">
                <div className="flex items-center space-x-3">
                  <div className="w-3 h-3 bg-blue-500 rounded-full"></div>
                  <span className="text-sm font-medium">{item.type}</span>
                </div>
                <div className="flex items-center space-x-3">
                  <div className="text-right">
                    <div className="flex items-center space-x-1">
                      <Badge variant="secondary">{item.percentage}%</Badge>
                      {getTrendIcon(item.trend)}
                      <span
                        className={`text-xs ${item.trend > 0 ? "text-green-600" : item.trend < 0 ? "text-red-600" : "text-gray-600"}`}
                      >
                        {item.trend > 0 ? "+" : ""}
                        {item.trend}%
                      </span>
                    </div>
                    <div className="text-xs text-gray-500">{item.count} reports</div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Source Reliability */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Users className="h-5 w-5 text-purple-600" />
            <span>Source Reliability</span>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {analyticsData.sourceReliability.map((item, index) => (
              <div key={index} className="space-y-2">
                <div className="flex justify-between items-center">
                  <span className="text-sm font-medium">{item.source}</span>
                  <div className="flex items-center space-x-2">
                    <span
                      className={`text-sm font-medium ${item.reliability >= 0.8 ? "text-green-600" : item.reliability >= 0.6 ? "text-yellow-600" : "text-red-600"}`}
                    >
                      {(item.reliability * 100).toFixed(0)}%
                    </span>
                    <span className="text-xs text-gray-500">({item.reports})</span>
                  </div>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div
                    className={`h-2 rounded-full transition-all duration-500 ${
                      item.reliability >= 0.8
                        ? "bg-green-500"
                        : item.reliability >= 0.6
                          ? "bg-yellow-500"
                          : "bg-red-500"
                    }`}
                    style={{ width: `${item.reliability * 100}%` }}
                  ></div>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Trending Topics */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <TrendingUp className="h-5 w-5 text-orange-600" />
            <span>Trending Topics</span>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {analyticsData.trendingTopics.map((item, index) => (
              <div key={index} className="flex justify-between items-center p-2 rounded-lg hover:bg-gray-50">
                <div className="flex items-center space-x-3">
                  <div className="text-sm font-medium">{item.topic}</div>
                  <Badge variant="outline" className={`text-xs ${getSentimentColor(item.sentiment)}`}>
                    {item.sentiment}
                  </Badge>
                </div>
                <div className="flex items-center space-x-2">
                  <span className="text-sm text-gray-600">{item.mentions}</span>
                  <div className="flex items-center space-x-1">
                    {getTrendIcon(item.change)}
                    <span
                      className={`text-xs ${item.change > 0 ? "text-green-600" : item.change < 0 ? "text-red-600" : "text-gray-600"}`}
                    >
                      {item.change > 0 ? "+" : ""}
                      {item.change}%
                    </span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Time Series Chart */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Clock className="h-5 w-5 text-indigo-600" />
            <span>Reports Over Time</span>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="flex justify-between text-sm text-gray-600">
              <span>Time</span>
              <span>Reports</span>
              <span>Avg Trust Score</span>
            </div>
            {analyticsData.timeSeriesData.map((item, index) => (
              <div key={index} className="flex justify-between items-center p-2 rounded-lg hover:bg-gray-50">
                <span className="text-sm font-medium">{item.hour}</span>
                <div className="flex items-center space-x-4">
                  <div className="flex items-center space-x-2">
                    <div className="w-16 bg-gray-200 rounded-full h-2">
                      <div
                        className="bg-blue-500 h-2 rounded-full"
                        style={{ width: `${(item.reports / 100) * 100}%` }}
                      ></div>
                    </div>
                    <span className="text-sm text-gray-600 w-8">{item.reports}</span>
                  </div>
                  <span
                    className={`text-sm font-medium w-12 ${item.trustScore >= 0.8 ? "text-green-600" : item.trustScore >= 0.6 ? "text-yellow-600" : "text-red-600"}`}
                  >
                    {(item.trustScore * 100).toFixed(0)}%
                  </span>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
