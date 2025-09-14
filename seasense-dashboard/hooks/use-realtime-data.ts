"use client"

import { useState, useEffect, useCallback } from "react"
import { seasenseAPI, seasenseWS, type Report, type SocialMediaPost, type SystemHealth } from "@/lib/api"

export interface RealtimeData {
  reports: Report[]
  socialPosts: SocialMediaPost[]
  systemHealth: SystemHealth | null
  metrics: {
    totalReports: number
    highTrustReports: number
    activeHazards: number
    systemHealthPercentage: number
  }
  isConnected: boolean
  lastUpdate: Date
}

export function useRealtimeData() {
  const [data, setData] = useState<RealtimeData>({
    reports: [],
    socialPosts: [],
    systemHealth: null,
    metrics: {
      totalReports: 0,
      highTrustReports: 0,
      activeHazards: 0,
      systemHealthPercentage: 0,
    },
    isConnected: false,
    lastUpdate: new Date(),
  })

  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  // Fetch initial data
  const fetchInitialData = useCallback(async () => {
    setIsLoading(true)
    setError(null)

    try {
      // Fetch reports for Mumbai area (example coordinates)
      const reportsResponse = await seasenseAPI.getNearbyReports(19.076, 72.877, 100)
      const socialResponse = await seasenseAPI.getSocialMediaPosts(20)
      const healthResponse = await seasenseAPI.getHealth()

      if (reportsResponse.status === "success") {
        const reports = reportsResponse.data || []
        const highTrustReports = reports.filter((r) => r.trust_score >= 0.8).length
        const activeHazards = reports.filter((r) => r.status === "verified" && r.priority === "critical").length

        setData((prev) => ({
          ...prev,
          reports,
          metrics: {
            ...prev.metrics,
            totalReports: reports.length,
            highTrustReports,
            activeHazards,
          },
          lastUpdate: new Date(),
        }))
      } else {
        // If API fails, use mock data
        const mockReports: Report[] = [
          {
            id: "RPT001",
            description: "High waves observed near Mumbai Beach",
            hazard_type: "high_waves",
            location: { latitude: 19.076, longitude: 72.877, address: "Mumbai Beach, Maharashtra" },
            trust_score: 0.85,
            priority: "critical",
            timestamp: "2024-12-13T14:30:00Z",
            status: "verified",
            source: "citizen",
            reported_by: "Rajesh Kumar",
            verified_by: "Coast Guard Mumbai",
          },
          {
            id: "RPT002",
            description: "Oil spill detected near Goa coast",
            hazard_type: "pollution",
            location: { latitude: 15.2993, longitude: 74.124, address: "Goa Coast, Goa" },
            trust_score: 0.72,
            priority: "high",
            timestamp: "2024-12-13T14:15:00Z",
            status: "pending",
            source: "social_media",
            reported_by: "Anonymous",
          },
        ]
        
        const highTrustReports = mockReports.filter((r) => r.trust_score >= 0.8).length
        const activeHazards = mockReports.filter((r) => r.status === "verified" && r.priority === "critical").length

        setData((prev) => ({
          ...prev,
          reports: mockReports,
          metrics: {
            ...prev.metrics,
            totalReports: mockReports.length,
            highTrustReports,
            activeHazards,
          },
          lastUpdate: new Date(),
        }))
      }

      if (socialResponse.status === "success") {
        setData((prev) => ({
          ...prev,
          socialPosts: socialResponse.data || [],
          lastUpdate: new Date(),
        }))
      } else {
        // Use mock social media data
        const mockSocialPosts: SocialMediaPost[] = [
          {
            id: "SM001",
            platform: "twitter",
            content: "Massive waves hitting Mumbai coastline! Stay safe everyone. #OceanAlert #Mumbai #Safety",
            author: "Rajesh Sharma",
            sentiment: "negative",
            engagement: { likes: 245, comments: 67, shares: 89, views: 1200 },
            timestamp: "2024-12-13T14:25:00Z",
            keywords: ["waves", "Mumbai", "safety", "coastline"],
            hazard_relevance: 0.92,
            trust_score: 0.78,
            location: "Mumbai, Maharashtra",
          },
        ]
        
        setData((prev) => ({
          ...prev,
          socialPosts: mockSocialPosts,
          lastUpdate: new Date(),
        }))
      }

      if (healthResponse.status === "success") {
        const health = healthResponse.data
        setData((prev) => ({
          ...prev,
          systemHealth: health,
          metrics: {
            ...prev.metrics,
            systemHealthPercentage: health?.uptime || 0,
          },
          lastUpdate: new Date(),
        }))
      } else {
        // Use mock health data
        const mockHealth: SystemHealth = {
          uptime: 99.8,
          status: "healthy",
          last_updated: new Date().toISOString(),
          services: {
            api: true,
            database: true,
            ai_engine: true,
            social_monitor: true,
          },
        }
        
        setData((prev) => ({
          ...prev,
          systemHealth: mockHealth,
          metrics: {
            ...prev.metrics,
            systemHealthPercentage: mockHealth.uptime,
          },
          lastUpdate: new Date(),
        }))
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to fetch data")
      console.error("Failed to fetch initial data:", err)
      
      // Set mock data on error
      const mockReports: Report[] = [
        {
          id: "RPT001",
          description: "High waves observed near Mumbai Beach",
          hazard_type: "high_waves",
          location: { latitude: 19.076, longitude: 72.877, address: "Mumbai Beach, Maharashtra" },
          trust_score: 0.85,
          priority: "critical",
          timestamp: "2024-12-13T14:30:00Z",
          status: "verified",
          source: "citizen",
          reported_by: "Rajesh Kumar",
          verified_by: "Coast Guard Mumbai",
        },
      ]
      
      setData((prev) => ({
        ...prev,
        reports: mockReports,
        metrics: {
          ...prev.metrics,
          totalReports: mockReports.length,
          highTrustReports: 1,
          activeHazards: 1,
          systemHealthPercentage: 99.8,
        },
        lastUpdate: new Date(),
      }))
    } finally {
      setIsLoading(false)
    }
  }, [])

  // Handle real-time updates
  const handleReportUpdate = useCallback((newReport: Report) => {
    setData((prev) => {
      const existingIndex = prev.reports.findIndex((r) => r.id === newReport.id)
      let updatedReports: Report[]

      if (existingIndex >= 0) {
        // Update existing report
        updatedReports = [...prev.reports]
        updatedReports[existingIndex] = newReport
      } else {
        // Add new report
        updatedReports = [newReport, ...prev.reports].slice(0, 100) // Keep only latest 100
      }

      const highTrustReports = updatedReports.filter((r) => r.trust_score >= 0.8).length
      const activeHazards = updatedReports.filter((r) => r.status === "verified" && r.priority === "critical").length

      return {
        ...prev,
        reports: updatedReports,
        metrics: {
          ...prev.metrics,
          totalReports: updatedReports.length,
          highTrustReports,
          activeHazards,
        },
        lastUpdate: new Date(),
      }
    })
  }, [])

  const handleSocialUpdate = useCallback((newPost: SocialMediaPost) => {
    setData((prev) => ({
      ...prev,
      socialPosts: [newPost, ...prev.socialPosts].slice(0, 50), // Keep only latest 50
      lastUpdate: new Date(),
    }))
  }, [])

  const handleSystemHealthUpdate = useCallback((health: SystemHealth) => {
    setData((prev) => ({
      ...prev,
      systemHealth: health,
      metrics: {
        ...prev.metrics,
        systemHealthPercentage: health.uptime,
      },
      lastUpdate: new Date(),
    }))
  }, [])

  // Setup WebSocket connection
  useEffect(() => {
    const connectWebSocket = async () => {
      try {
        await seasenseWS.connect()
        setData((prev) => ({ ...prev, isConnected: true }))

        // Subscribe to real-time events
        seasenseWS.subscribe("report_update", handleReportUpdate)
        seasenseWS.subscribe("new_report", handleReportUpdate)
        seasenseWS.subscribe("social_post", handleSocialUpdate)
        seasenseWS.subscribe("system_health", handleSystemHealthUpdate)
      } catch (err) {
        console.error("Failed to connect WebSocket:", err)
        setData((prev) => ({ ...prev, isConnected: false }))
      }
    }

    connectWebSocket()

    return () => {
      seasenseWS.unsubscribe("report_update", handleReportUpdate)
      seasenseWS.unsubscribe("new_report", handleReportUpdate)
      seasenseWS.unsubscribe("social_post", handleSocialUpdate)
      seasenseWS.unsubscribe("system_health", handleSystemHealthUpdate)
      seasenseWS.disconnect()
    }
  }, [handleReportUpdate, handleSocialUpdate, handleSystemHealthUpdate])

  // Fetch initial data on mount
  useEffect(() => {
    fetchInitialData()
  }, [fetchInitialData])

  // Periodic data refresh (fallback for when WebSocket is not available)
  useEffect(() => {
    const interval = setInterval(() => {
      if (!data.isConnected) {
        fetchInitialData()
      }
    }, 30000) // Refresh every 30 seconds if not connected

    return () => clearInterval(interval)
  }, [data.isConnected, fetchInitialData])

  const refreshData = useCallback(() => {
    fetchInitialData()
  }, [fetchInitialData])

  return {
    data,
    isLoading,
    error,
    refreshData,
  }
}
