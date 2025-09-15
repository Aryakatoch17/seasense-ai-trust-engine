"use client"

import { useState, useEffect } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
  DropdownMenuSeparator,
} from "@/components/ui/dropdown-menu"
import {
  Users,
  Heart,
  MessageCircle,
  Share,
  ExternalLink,
  AlertTriangle,
  Eye,
  MoreHorizontal,
  Flag,
  Bookmark,
} from "lucide-react"

interface SocialPost {
  id: string
  platform: "Twitter" | "Facebook" | "Instagram" | "TikTok" | "YouTube"
  content: string
  author: string
  authorHandle: string
  authorAvatar?: string
  sentiment: "positive" | "negative" | "neutral"
  engagement: {
    likes: number
    comments: number
    shares: number
    views?: number
  }
  timestamp: string
  keywords: string[]
  hazardRelevance: number
  location?: string
  images?: string[]
  verified: boolean
  flagged: boolean
  trustScore: number
}

export default function SocialMediaFeed() {
  const [posts, setPosts] = useState<SocialPost[]>([])
  const [filteredPosts, setFilteredPosts] = useState<SocialPost[]>([])
  const [searchTerm, setSearchTerm] = useState("")
  const [platformFilter, setPlatformFilter] = useState("all")
  const [sentimentFilter, setSentimentFilter] = useState("all")
  const [sortBy, setSortBy] = useState("timestamp")
  const [isLive, setIsLive] = useState(true)

  // Mock social media posts
  const mockPosts: SocialPost[] = [
    {
      id: "SM001",
      platform: "Twitter",
      content:
        "Massive waves hitting Mumbai coastline! Stay safe everyone. The waves are easily 4-5 meters high. #OceanAlert #Mumbai #Safety",
      author: "Rajesh Sharma",
      authorHandle: "@rajesh_mumbai",
      sentiment: "negative",
      engagement: { likes: 245, comments: 67, shares: 89, views: 1200 },
      timestamp: "2024-12-13T14:25:00Z",
      keywords: ["waves", "Mumbai", "safety", "coastline"],
      hazardRelevance: 0.92,
      location: "Mumbai, Maharashtra",
      verified: false,
      flagged: false,
      trustScore: 0.78,
    },
    {
      id: "SM002",
      platform: "Facebook",
      content:
        "Beautiful calm waters at Goa today! Perfect weather for swimming and water sports. The beach is absolutely stunning.",
      author: "Maria D'Souza",
      authorHandle: "maria.dsouza",
      sentiment: "positive",
      engagement: { likes: 89, comments: 23, shares: 12, views: 456 },
      timestamp: "2024-12-13T14:12:00Z",
      keywords: ["calm", "Goa", "swimming", "beach"],
      hazardRelevance: 0.15,
      location: "Goa",
      verified: false,
      flagged: false,
      trustScore: 0.65,
    },
    {
      id: "SM003",
      platform: "Instagram",
      content:
        "Oil spill spotted near the coast! This is terrible for marine life. Authorities need to take immediate action! #Environment #OilSpill",
      author: "EcoWarrior",
      authorHandle: "@eco_warrior_india",
      sentiment: "negative",
      engagement: { likes: 156, comments: 45, shares: 78, views: 890 },
      timestamp: "2024-12-13T13:58:00Z",
      keywords: ["oil spill", "environment", "marine life", "authorities"],
      hazardRelevance: 0.88,
      location: "West Coast",
      verified: true,
      flagged: false,
      trustScore: 0.82,
    },
    {
      id: "SM004",
      platform: "Twitter",
      content:
        "Chennai Marina looks clean today! Great work by the cleanup crew. The water quality has improved significantly. #ChennaiMarina #CleanOcean",
      author: "Chennai Port Authority",
      authorHandle: "@chennai_port",
      sentiment: "positive",
      engagement: { likes: 67, comments: 12, shares: 34, views: 234 },
      timestamp: "2024-12-13T13:45:00Z",
      keywords: ["Chennai", "clean", "marina", "water quality"],
      hazardRelevance: 0.45,
      location: "Chennai, Tamil Nadu",
      verified: true,
      flagged: false,
      trustScore: 0.91,
    },
    {
      id: "SM005",
      platform: "Facebook",
      content:
        "Strange foam appearing on Kochi beach. Not sure what's causing it. Has anyone else noticed this? Should we be concerned?",
      author: "Local Fisherman",
      authorHandle: "kochi.fisher",
      sentiment: "neutral",
      engagement: { likes: 34, comments: 28, shares: 15, views: 167 },
      timestamp: "2024-12-13T13:30:00Z",
      keywords: ["foam", "Kochi", "beach", "concerned"],
      hazardRelevance: 0.67,
      location: "Kochi, Kerala",
      verified: false,
      flagged: false,
      trustScore: 0.58,
    },
    {
      id: "SM006",
      platform: "Instagram",
      content:
        "Incredible sunset at Visakhapatnam beach! The colors are amazing tonight. Perfect evening for a beach walk.",
      author: "Travel Blogger",
      authorHandle: "@travel_india_blog",
      sentiment: "positive",
      engagement: { likes: 234, comments: 56, shares: 23, views: 1100 },
      timestamp: "2024-12-13T13:15:00Z",
      keywords: ["sunset", "Visakhapatnam", "beach", "evening"],
      hazardRelevance: 0.12,
      location: "Visakhapatnam, Andhra Pradesh",
      verified: false,
      flagged: false,
      trustScore: 0.42,
    },
    {
      id: "SM007",
      platform: "Twitter",
      content:
        "URGENT: High tide warning for Mangalore coast. Fishermen advised to return to shore immediately. Coast Guard on alert.",
      author: "Karnataka Coast Guard",
      authorHandle: "@karnataka_cg",
      sentiment: "negative",
      engagement: { likes: 123, comments: 34, shares: 89, views: 567 },
      timestamp: "2024-12-13T13:00:00Z",
      keywords: ["urgent", "high tide", "Mangalore", "fishermen", "coast guard"],
      hazardRelevance: 0.95,
      location: "Mangalore, Karnataka",
      verified: true,
      flagged: false,
      trustScore: 0.96,
    },
    {
      id: "SM008",
      platform: "TikTok",
      content:
        "Beach cleanup drive at Puri! Join us this weekend to make our coastline beautiful again. Every small effort counts!",
      author: "Green Puri Initiative",
      authorHandle: "@green_puri",
      sentiment: "positive",
      engagement: { likes: 445, comments: 78, shares: 156, views: 2300 },
      timestamp: "2024-12-13T12:45:00Z",
      keywords: ["beach cleanup", "Puri", "weekend", "coastline"],
      hazardRelevance: 0.35,
      location: "Puri, Odisha",
      verified: false,
      flagged: false,
      trustScore: 0.73,
    },
  ]

  useEffect(() => {
    setPosts(mockPosts)
    setFilteredPosts(mockPosts)
  }, [])

  useEffect(() => {
    const filtered = posts.filter((post) => {
      const matchesSearch =
        post.content.toLowerCase().includes(searchTerm.toLowerCase()) ||
        post.keywords.some((keyword) => keyword.toLowerCase().includes(searchTerm.toLowerCase())) ||
        post.author.toLowerCase().includes(searchTerm.toLowerCase()) ||
        (post.location && post.location.toLowerCase().includes(searchTerm.toLowerCase()))

      const matchesPlatform = platformFilter === "all" || post.platform === platformFilter
      const matchesSentiment = sentimentFilter === "all" || post.sentiment === sentimentFilter

      return matchesSearch && matchesPlatform && matchesSentiment
    })

    // Sort posts
    filtered.sort((a, b) => {
      switch (sortBy) {
        case "timestamp":
          return new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime()
        case "engagement":
          const aEngagement = a.engagement.likes + a.engagement.comments + a.engagement.shares
          const bEngagement = b.engagement.likes + b.engagement.comments + b.engagement.shares
          return bEngagement - aEngagement
        case "relevance":
          return b.hazardRelevance - a.hazardRelevance
        case "trustScore":
          return b.trustScore - a.trustScore
        default:
          return 0
      }
    })

    setFilteredPosts(filtered)
  }, [posts, searchTerm, platformFilter, sentimentFilter, sortBy])

  // Simulate real-time updates
  useEffect(() => {
    if (!isLive) return

    const interval = setInterval(() => {
      // Simulate new posts or engagement updates
      setPosts((prevPosts) =>
        prevPosts.map((post) => ({
          ...post,
          engagement: {
            ...post.engagement,
            likes: post.engagement.likes + Math.floor(Math.random() * 3),
            comments: post.engagement.comments + Math.floor(Math.random() * 2),
          },
        })),
      )
    }, 30000)

    return () => clearInterval(interval)
  }, [isLive])

  const getPlatformColor = (platform: string) => {
    switch (platform) {
      case "Twitter":
        return "bg-blue-100 text-blue-800"
      case "Facebook":
        return "bg-blue-100 text-blue-800"
      case "Instagram":
        return "bg-pink-100 text-pink-800"
      case "TikTok":
        return "bg-gray-100 text-gray-800"
      case "YouTube":
        return "bg-red-100 text-red-800"
      default:
        return "bg-gray-100 text-gray-800"
    }
  }

  const getSentimentColor = (sentiment: string) => {
    switch (sentiment) {
      case "positive":
        return "bg-green-100 text-green-800"
      case "negative":
        return "bg-red-100 text-red-800"
      default:
        return "bg-gray-100 text-gray-800"
    }
  }

  const getRelevanceColor = (relevance: number) => {
    if (relevance >= 0.8) return "text-red-600 font-semibold"
    if (relevance >= 0.6) return "text-orange-600 font-semibold"
    if (relevance >= 0.4) return "text-yellow-600 font-semibold"
    return "text-gray-600"
  }

  const getTrustScoreColor = (score: number) => {
    if (score >= 0.8) return "text-green-600"
    if (score >= 0.6) return "text-yellow-600"
    return "text-red-600"
  }

  const formatEngagement = (engagement: SocialPost["engagement"]) => {
    const total = engagement.likes + engagement.comments + engagement.shares
    return total > 1000 ? `${(total / 1000).toFixed(1)}k` : total.toString()
  }

  const handlePostAction = (postId: string, action: string) => {
    console.log(`Performing ${action} on post ${postId}`)
    // Implement post actions here
  }

  return (
    <Card className="h-full">
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle className="flex items-center space-x-2">
            <Users className="h-5 w-5 text-purple-600" />
            <span>Social Media Monitor</span>
            <Badge variant="secondary">{filteredPosts.length} posts</Badge>
            {isLive && <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />}
          </CardTitle>
          <Button variant="outline" size="sm" onClick={() => setIsLive(!isLive)}>
            {isLive ? "Pause" : "Resume"} Live Feed
          </Button>
        </div>

        {/* Filters */}
        <div className="flex flex-wrap items-center gap-3 mt-4">
          <div className="flex items-center space-x-2">
            <Input
              placeholder="Search posts..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-48"
            />
          </div>

          <Select value={platformFilter} onValueChange={setPlatformFilter}>
            <SelectTrigger className="w-32">
              <SelectValue placeholder="Platform" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All Platforms</SelectItem>
              <SelectItem value="Twitter">Twitter</SelectItem>
              <SelectItem value="Facebook">Facebook</SelectItem>
              <SelectItem value="Instagram">Instagram</SelectItem>
              <SelectItem value="TikTok">TikTok</SelectItem>
              <SelectItem value="YouTube">YouTube</SelectItem>
            </SelectContent>
          </Select>

          <Select value={sentimentFilter} onValueChange={setSentimentFilter}>
            <SelectTrigger className="w-32">
              <SelectValue placeholder="Sentiment" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All Sentiment</SelectItem>
              <SelectItem value="positive">Positive</SelectItem>
              <SelectItem value="negative">Negative</SelectItem>
              <SelectItem value="neutral">Neutral</SelectItem>
            </SelectContent>
          </Select>

          <Select value={sortBy} onValueChange={setSortBy}>
            <SelectTrigger className="w-32">
              <SelectValue placeholder="Sort by" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="timestamp">Latest</SelectItem>
              <SelectItem value="engagement">Engagement</SelectItem>
              <SelectItem value="relevance">Relevance</SelectItem>
              <SelectItem value="trustScore">Trust Score</SelectItem>
            </SelectContent>
          </Select>
        </div>
      </CardHeader>

      <CardContent className="space-y-4 max-h-[600px] overflow-y-auto">
        {filteredPosts.map((post) => (
          <div
            key={post.id}
            className={`border rounded-lg p-4 hover:bg-gray-50 transition-colors ${
              post.hazardRelevance >= 0.8 ? "border-red-200 bg-red-50" : ""
            }`}
          >
            {/* Post Header */}
            <div className="flex items-center justify-between mb-3">
              <div className="flex items-center space-x-3">
                <div className="flex items-center space-x-2">
                  <Badge className={`text-xs ${getPlatformColor(post.platform)}`}>{post.platform}</Badge>
                  {post.verified && (
                    <Badge variant="default" className="text-xs bg-blue-500">
                      Verified
                    </Badge>
                  )}
                  {post.flagged && (
                    <Badge variant="destructive" className="text-xs">
                      Flagged
                    </Badge>
                  )}
                </div>
                <div>
                  <div className="text-sm font-medium">{post.author}</div>
                  <div className="text-xs text-gray-500">{post.authorHandle}</div>
                </div>
              </div>
              <div className="flex items-center space-x-2">
                <span className="text-xs text-gray-500">
                  {new Date(post.timestamp).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}
                </span>
                <DropdownMenu>
                  <DropdownMenuTrigger asChild>
                    <Button variant="ghost" size="sm">
                      <MoreHorizontal className="w-4 h-4" />
                    </Button>
                  </DropdownMenuTrigger>
                  <DropdownMenuContent>
                    <DropdownMenuItem onClick={() => handlePostAction(post.id, "view")}>
                      <Eye className="w-4 h-4 mr-2" />
                      View Details
                    </DropdownMenuItem>
                    <DropdownMenuItem onClick={() => handlePostAction(post.id, "bookmark")}>
                      <Bookmark className="w-4 h-4 mr-2" />
                      Bookmark
                    </DropdownMenuItem>
                    <DropdownMenuSeparator />
                    <DropdownMenuItem onClick={() => handlePostAction(post.id, "flag")}>
                      <Flag className="w-4 h-4 mr-2" />
                      Flag as Suspicious
                    </DropdownMenuItem>
                    <DropdownMenuItem onClick={() => handlePostAction(post.id, "external")}>
                      <ExternalLink className="w-4 h-4 mr-2" />
                      View Original
                    </DropdownMenuItem>
                  </DropdownMenuContent>
                </DropdownMenu>
              </div>
            </div>

            {/* Post Content */}
            <div className="mb-3">
              <p className="text-sm text-gray-800 leading-relaxed">{post.content}</p>
              {post.location && (
                <div className="text-xs text-gray-500 mt-1 flex items-center">
                  <span>📍 {post.location}</span>
                </div>
              )}
            </div>

            {/* Keywords */}
            <div className="flex flex-wrap gap-1 mb-3">
              {post.keywords.slice(0, 4).map((keyword, index) => (
                <Badge key={index} variant="secondary" className="text-xs">
                  {keyword}
                </Badge>
              ))}
              {post.keywords.length > 4 && (
                <Badge variant="secondary" className="text-xs">
                  +{post.keywords.length - 4} more
                </Badge>
              )}
            </div>

            {/* Post Metrics */}
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-4">
                <div className="flex items-center space-x-1 text-xs text-gray-600">
                  <Heart className="w-3 h-3" />
                  <span>{post.engagement.likes}</span>
                </div>
                <div className="flex items-center space-x-1 text-xs text-gray-600">
                  <MessageCircle className="w-3 h-3" />
                  <span>{post.engagement.comments}</span>
                </div>
                <div className="flex items-center space-x-1 text-xs text-gray-600">
                  <Share className="w-3 h-3" />
                  <span>{post.engagement.shares}</span>
                </div>
                {post.engagement.views && (
                  <div className="flex items-center space-x-1 text-xs text-gray-600">
                    <Eye className="w-3 h-3" />
                    <span>{post.engagement.views}</span>
                  </div>
                )}
              </div>

              <div className="flex items-center space-x-3">
                <Badge className={`text-xs ${getSentimentColor(post.sentiment)}`}>{post.sentiment}</Badge>
                <div className="text-xs">
                  <span className="text-gray-500">Relevance: </span>
                  <span className={getRelevanceColor(post.hazardRelevance)}>
                    {(post.hazardRelevance * 100).toFixed(0)}%
                  </span>
                </div>
                <div className="text-xs">
                  <span className="text-gray-500">Trust: </span>
                  <span className={getTrustScoreColor(post.trustScore)}>{(post.trustScore * 100).toFixed(0)}%</span>
                </div>
              </div>
            </div>

            {/* High Relevance Alert */}
            {post.hazardRelevance >= 0.8 && (
              <div className="mt-3 p-2 bg-red-100 border border-red-200 rounded-lg">
                <div className="flex items-center space-x-2 text-red-800">
                  <AlertTriangle className="w-4 h-4" />
                  <span className="text-xs font-medium">High Hazard Relevance - Requires Attention</span>
                </div>
              </div>
            )}
          </div>
        ))}

        {filteredPosts.length === 0 && (
          <div className="text-center py-8 text-gray-500">
            <Users className="w-12 h-12 mx-auto mb-4 opacity-50" />
            <p>No posts match your current filters</p>
          </div>
        )}
      </CardContent>
    </Card>
  )
}
