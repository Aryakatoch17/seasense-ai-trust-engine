"use client"

import { useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from "@/components/ui/dropdown-menu"
import { Alert, AlertDescription } from "@/components/ui/alert"
import {
  Waves,
  AlertTriangle,
  Shield,
  Activity,
  TrendingUp,
  Pause,
  Play,
  RefreshCw,
  Download,
  Wifi,
  WifiOff,
} from "lucide-react"
import InteractiveMap from "@/components/interactive-map"
import AnalyticsCharts from "@/components/analytics-charts"
import ReportsTable from "@/components/reports-table"
import SocialMediaFeed from "@/components/social-media-feed"
import { useRealtimeData } from "@/hooks/use-realtime-data"

export default function SeaSenseDashboard() {
  const { data, isLoading, error, refreshData } = useRealtimeData()
  const [isRealTimeActive, setIsRealTimeActive] = useState(true)

  const handleToggleRealTime = () => {
    setIsRealTimeActive(!isRealTimeActive)
    // In a real implementation, this would pause/resume WebSocket subscriptions
  }

  const handleRefresh = () => {
    refreshData()
  }

  const handleExport = async () => {
    // In a real implementation, this would trigger data export
    console.log("Exporting dashboard data...")
  }

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-teal-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-blue-600 font-medium">Loading SeaSense Dashboard...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-teal-50">
      {/* Header */}
      <header className="bg-white border-b border-blue-100 shadow-sm">
        <div className="px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="flex items-center space-x-2">
                <Waves className="h-8 w-8 text-blue-600" />
                <div>
                  <h1 className="text-2xl font-bold text-blue-900">SeaSense AI</h1>
                  <p className="text-sm text-blue-600">Ocean Hazard Management System</p>
                </div>
              </div>
              <div className="flex items-center space-x-2 ml-8">
                <div
                  className={`w-3 h-3 rounded-full ${
                    data.isConnected && isRealTimeActive ? "bg-green-500" : "bg-red-500"
                  } animate-pulse`}
                />
                <span className="text-sm text-gray-600">
                  {data.isConnected && isRealTimeActive ? "Live" : "Offline"}
                </span>
                {data.isConnected ? (
                  <Wifi className="w-4 h-4 text-green-600" />
                ) : (
                  <WifiOff className="w-4 h-4 text-red-600" />
                )}
              </div>
            </div>

            <div className="flex items-center space-x-4">
              <div className="text-right">
                <div className="text-sm font-medium text-gray-900">{data.lastUpdate.toLocaleTimeString()}</div>
                <div className="text-xs text-gray-500">{data.lastUpdate.toLocaleDateString()}</div>
              </div>

              <Badge variant="destructive" className="bg-red-500">
                <AlertTriangle className="w-3 h-3 mr-1" />
                {data.metrics.activeHazards} Alerts
              </Badge>

              <div className="flex items-center space-x-2">
                <Button variant="outline" size="sm" onClick={handleToggleRealTime}>
                  {isRealTimeActive ? <Pause className="w-4 h-4" /> : <Play className="w-4 h-4" />}
                </Button>
                <Button variant="outline" size="sm" onClick={handleRefresh}>
                  <RefreshCw className="w-4 h-4" />
                </Button>
                <Button variant="outline" size="sm" onClick={handleExport}>
                  <Download className="w-4 h-4" />
                </Button>
              </div>

              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <Button variant="ghost" className="relative h-8 w-8 rounded-full">
                    <Avatar className="h-8 w-8">
                      <AvatarImage src="/emergency-manager-avatar.jpg" alt="User" />
                      <AvatarFallback>EM</AvatarFallback>
                    </Avatar>
                  </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent className="w-56" align="end" forceMount>
                  <DropdownMenuItem>Profile</DropdownMenuItem>
                  <DropdownMenuItem>Settings</DropdownMenuItem>
                  <DropdownMenuItem>Export Data</DropdownMenuItem>
                  <DropdownMenuItem>Sign out</DropdownMenuItem>
                </DropdownMenuContent>
              </DropdownMenu>
            </div>
          </div>
        </div>
      </header>

      {/* Error Alert */}
      {error && (
        <div className="px-6 pt-4">
          <Alert variant="destructive">
            <AlertTriangle className="h-4 w-4" />
            <AlertDescription>{error} - Some features may not work properly. Try refreshing the page.</AlertDescription>
          </Alert>
        </div>
      )}

      {/* Main Content */}
      <main className="p-6 space-y-6">
        {/* Key Metrics Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <Card className="border-blue-200 hover:shadow-lg transition-shadow">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium text-blue-700">Total Reports Today</CardTitle>
              <Activity className="h-4 w-4 text-blue-600" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-blue-900">{data.metrics.totalReports.toLocaleString()}</div>
              <p className="text-xs text-green-600 flex items-center mt-1">
                <TrendingUp className="w-3 h-3 mr-1" />
                Real-time data
              </p>
            </CardContent>
          </Card>

          <Card className="border-teal-200 hover:shadow-lg transition-shadow">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium text-teal-700">High Trust Reports</CardTitle>
              <Shield className="h-4 w-4 text-teal-600" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-teal-900">{data.metrics.highTrustReports.toLocaleString()}</div>
              <p className="text-xs text-teal-600 mt-1">
                {data.metrics.totalReports > 0
                  ? Math.round((data.metrics.highTrustReports / data.metrics.totalReports) * 100)
                  : 0}
                % of total
              </p>
            </CardContent>
          </Card>

          <Card className="border-red-200 hover:shadow-lg transition-shadow">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium text-red-700">Active Hazards</CardTitle>
              <AlertTriangle className="h-4 w-4 text-red-600" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-red-900">{data.metrics.activeHazards}</div>
              <p className="text-xs text-red-600 mt-1">Requires immediate attention</p>
            </CardContent>
          </Card>

          <Card className="border-green-200 hover:shadow-lg transition-shadow">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium text-green-700">System Health</CardTitle>
              <Activity className="h-4 w-4 text-green-600" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-green-900">{data.metrics.systemHealthPercentage.toFixed(1)}%</div>
              <p className="text-xs text-green-600 mt-1">
                {data.systemHealth?.status === "healthy" ? "All systems operational" : "Some issues detected"}
              </p>
            </CardContent>
          </Card>
        </div>

        {/* Main Dashboard Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-5 gap-6">
          {/* Map Section - Left Side (60% width) */}
          <div className="lg:col-span-3">
            <InteractiveMap />
          </div>

          {/* Analytics Section - Right Side (40% width) */}
          <div className="lg:col-span-2">
            <AnalyticsCharts />
          </div>
        </div>

        {/* Bottom Section */}
        <div className="grid grid-cols-1 lg:grid-cols-5 gap-6">
          {/* Reports Table - Left Side (60% width) */}
          <div className="lg:col-span-3">
            <ReportsTable />
          </div>

          {/* Social Media Feed - Right Side (40% width) */}
          <div className="lg:col-span-2">
            <SocialMediaFeed />
          </div>
        </div>
      </main>
    </div>
  )
}
