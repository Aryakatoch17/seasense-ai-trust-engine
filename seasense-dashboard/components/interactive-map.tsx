"use client"

import { useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { MapPin, Waves, AlertTriangle, Trash2, Thermometer, Layers, ZoomIn, ZoomOut } from "lucide-react"

interface HazardMarker {
  id: string
  latitude: number
  longitude: number
  hazardType: "tsunami" | "high_waves" | "pollution" | "debris" | "temperature"
  priority: "critical" | "high" | "medium" | "low"
  trustScore: number
  description: string
  timestamp: string
  status: "verified" | "pending" | "flagged"
}

export default function InteractiveMap() {
  const [selectedMarker, setSelectedMarker] = useState<HazardMarker | null>(null)
  const [zoomLevel, setZoomLevel] = useState(6)
  const [showLayers, setShowLayers] = useState({
    critical: true,
    high: true,
    medium: true,
    low: true,
  })

  // Mock hazard data for Indian coastline
  const hazardMarkers: HazardMarker[] = [
    {
      id: "HAZ001",
      latitude: 19.076,
      longitude: 72.877,
      hazardType: "high_waves",
      priority: "critical",
      trustScore: 0.92,
      description: "Massive waves hitting Mumbai coastline, 4-5 meter height",
      timestamp: "2024-12-13T14:30:00Z",
      status: "verified",
    },
    {
      id: "HAZ002",
      latitude: 15.2993,
      longitude: 74.124,
      hazardType: "pollution",
      priority: "high",
      trustScore: 0.78,
      description: "Oil spill detected near Goa coast",
      timestamp: "2024-12-13T13:45:00Z",
      status: "pending",
    },
    {
      id: "HAZ003",
      latitude: 13.0827,
      longitude: 80.2707,
      hazardType: "debris",
      priority: "medium",
      trustScore: 0.85,
      description: "Large debris field observed near Chennai Marina",
      timestamp: "2024-12-13T12:15:00Z",
      status: "verified",
    },
    {
      id: "HAZ004",
      latitude: 11.9416,
      longitude: 79.8083,
      hazardType: "temperature",
      priority: "low",
      trustScore: 0.67,
      description: "Unusual water temperature spike reported",
      timestamp: "2024-12-13T11:30:00Z",
      status: "flagged",
    },
    {
      id: "HAZ005",
      latitude: 8.5241,
      longitude: 76.9366,
      hazardType: "high_waves",
      priority: "high",
      trustScore: 0.89,
      description: "High waves near Kochi, affecting fishing activities",
      timestamp: "2024-12-13T10:45:00Z",
      status: "verified",
    },
  ]

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case "critical":
        return "bg-red-600 border-red-700"
      case "high":
        return "bg-orange-500 border-orange-600"
      case "medium":
        return "bg-yellow-500 border-yellow-600"
      case "low":
        return "bg-green-500 border-green-600"
      default:
        return "bg-gray-500 border-gray-600"
    }
  }

  const getHazardIcon = (hazardType: string) => {
    switch (hazardType) {
      case "tsunami":
      case "high_waves":
        return <Waves className="w-3 h-3 text-white" />
      case "pollution":
        return <AlertTriangle className="w-3 h-3 text-white" />
      case "debris":
        return <Trash2 className="w-3 h-3 text-white" />
      case "temperature":
        return <Thermometer className="w-3 h-3 text-white" />
      default:
        return <MapPin className="w-3 h-3 text-white" />
    }
  }

  const filteredMarkers = hazardMarkers.filter((marker) => showLayers[marker.priority])

  // Convert lat/lng to pixel coordinates for the mock map
  const getMarkerPosition = (lat: number, lng: number) => {
    // Simple projection for Indian coastline (approximate)
    const mapBounds = {
      north: 25,
      south: 8,
      east: 85,
      west: 68,
    }

    const x = ((lng - mapBounds.west) / (mapBounds.east - mapBounds.west)) * 100
    const y = ((mapBounds.north - lat) / (mapBounds.north - mapBounds.south)) * 100

    return { x: Math.max(0, Math.min(100, x)), y: Math.max(0, Math.min(100, y)) }
  }

  return (
    <Card className="h-[500px]">
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle className="flex items-center space-x-2">
            <MapPin className="h-5 w-5 text-blue-600" />
            <span>Real-time Hazard Map</span>
          </CardTitle>
          <div className="flex items-center space-x-2">
            <Button variant="outline" size="sm" onClick={() => setZoomLevel(Math.min(10, zoomLevel + 1))}>
              <ZoomIn className="w-4 h-4" />
            </Button>
            <Button variant="outline" size="sm" onClick={() => setZoomLevel(Math.max(1, zoomLevel - 1))}>
              <ZoomOut className="w-4 h-4" />
            </Button>
            <Button
              variant="outline"
              size="sm"
              onClick={() => setShowLayers({ critical: true, high: true, medium: true, low: true })}
            >
              <Layers className="w-4 h-4" />
            </Button>
          </div>
        </div>
        <div className="flex items-center space-x-4 text-sm">
          <label className="flex items-center space-x-1">
            <input
              type="checkbox"
              checked={showLayers.critical}
              onChange={(e) => setShowLayers({ ...showLayers, critical: e.target.checked })}
              className="rounded"
            />
            <span className="w-3 h-3 bg-red-600 rounded-full"></span>
            <span>Critical</span>
          </label>
          <label className="flex items-center space-x-1">
            <input
              type="checkbox"
              checked={showLayers.high}
              onChange={(e) => setShowLayers({ ...showLayers, high: e.target.checked })}
              className="rounded"
            />
            <span className="w-3 h-3 bg-orange-500 rounded-full"></span>
            <span>High</span>
          </label>
          <label className="flex items-center space-x-1">
            <input
              type="checkbox"
              checked={showLayers.medium}
              onChange={(e) => setShowLayers({ ...showLayers, medium: e.target.checked })}
              className="rounded"
            />
            <span className="w-3 h-3 bg-yellow-500 rounded-full"></span>
            <span>Medium</span>
          </label>
          <label className="flex items-center space-x-1">
            <input
              type="checkbox"
              checked={showLayers.low}
              onChange={(e) => setShowLayers({ ...showLayers, low: e.target.checked })}
              className="rounded"
            />
            <span className="w-3 h-3 bg-green-500 rounded-full"></span>
            <span>Low</span>
          </label>
        </div>
      </CardHeader>
      <CardContent className="h-full p-0">
        <div className="relative w-full h-full bg-gradient-to-br from-blue-100 to-blue-200 rounded-lg overflow-hidden">
          {/* Mock Indian coastline background */}
          <div className="absolute inset-0">
            <svg viewBox="0 0 400 300" className="w-full h-full">
              {/* Simplified Indian coastline path */}
              <path
                d="M50 50 Q80 40 120 60 Q160 80 200 70 Q240 60 280 80 Q320 100 350 120 L350 250 Q320 240 280 230 Q240 220 200 210 Q160 200 120 190 Q80 180 50 170 Z"
                fill="#e0f2fe"
                stroke="#0369a1"
                strokeWidth="2"
              />
              {/* Water areas */}
              <circle cx="100" cy="150" r="20" fill="#0ea5e9" opacity="0.3" />
              <circle cx="200" cy="180" r="25" fill="#0ea5e9" opacity="0.3" />
              <circle cx="300" cy="160" r="18" fill="#0ea5e9" opacity="0.3" />
            </svg>
          </div>

          {/* Hazard markers */}
          {filteredMarkers.map((marker) => {
            const position = getMarkerPosition(marker.latitude, marker.longitude)
            return (
              <div
                key={marker.id}
                className={`absolute transform -translate-x-1/2 -translate-y-1/2 cursor-pointer transition-all duration-200 hover:scale-110 ${
                  selectedMarker?.id === marker.id ? "scale-125 z-20" : "z-10"
                }`}
                style={{
                  left: `${position.x}%`,
                  top: `${position.y}%`,
                }}
                onClick={() => setSelectedMarker(marker)}
              >
                <div
                  className={`w-8 h-8 rounded-full border-2 flex items-center justify-center shadow-lg ${getPriorityColor(
                    marker.priority,
                  )} ${selectedMarker?.id === marker.id ? "ring-2 ring-white" : ""}`}
                >
                  {getHazardIcon(marker.hazardType)}
                </div>
                {marker.priority === "critical" && (
                  <div className="absolute -top-1 -right-1 w-3 h-3 bg-red-600 rounded-full animate-pulse"></div>
                )}
              </div>
            )
          })}

          {/* Selected marker details popup */}
          {selectedMarker && (
            <div className="absolute top-4 right-4 w-80 bg-white rounded-lg shadow-xl border p-4 z-30">
              <div className="flex items-center justify-between mb-3">
                <div className="flex items-center space-x-2">
                  <div className={`w-4 h-4 rounded-full ${getPriorityColor(selectedMarker.priority)}`}></div>
                  <h3 className="font-semibold text-gray-900">
                    {selectedMarker.hazardType.replace("_", " ").toUpperCase()}
                  </h3>
                </div>
                <Button variant="ghost" size="sm" onClick={() => setSelectedMarker(null)}>
                  ×
                </Button>
              </div>

              <div className="space-y-2 text-sm">
                <div>
                  <span className="font-medium text-gray-600">Location:</span>
                  <span className="ml-2">
                    {selectedMarker.latitude.toFixed(4)}, {selectedMarker.longitude.toFixed(4)}
                  </span>
                </div>
                <div>
                  <span className="font-medium text-gray-600">Trust Score:</span>
                  <span
                    className={`ml-2 font-medium ${selectedMarker.trustScore >= 0.8 ? "text-green-600" : selectedMarker.trustScore >= 0.6 ? "text-yellow-600" : "text-red-600"}`}
                  >
                    {(selectedMarker.trustScore * 100).toFixed(0)}%
                  </span>
                </div>
                <div>
                  <span className="font-medium text-gray-600">Status:</span>
                  <Badge
                    variant={
                      selectedMarker.status === "verified"
                        ? "default"
                        : selectedMarker.status === "pending"
                          ? "secondary"
                          : "destructive"
                    }
                    className="ml-2"
                  >
                    {selectedMarker.status}
                  </Badge>
                </div>
                <div>
                  <span className="font-medium text-gray-600">Time:</span>
                  <span className="ml-2">{new Date(selectedMarker.timestamp).toLocaleString()}</span>
                </div>
                <div className="pt-2">
                  <span className="font-medium text-gray-600">Description:</span>
                  <p className="mt-1 text-gray-800">{selectedMarker.description}</p>
                </div>
              </div>

              <div className="flex space-x-2 mt-4">
                <Button size="sm" variant="outline">
                  Verify
                </Button>
                <Button size="sm" variant="outline">
                  Flag
                </Button>
                <Button size="sm" variant="outline">
                  Details
                </Button>
              </div>
            </div>
          )}

          {/* Map legend */}
          <div className="absolute bottom-4 left-4 bg-white rounded-lg shadow-lg p-3">
            <h4 className="font-semibold text-sm mb-2">Hazard Types</h4>
            <div className="space-y-1 text-xs">
              <div className="flex items-center space-x-2">
                <Waves className="w-3 h-3 text-blue-600" />
                <span>High Waves</span>
              </div>
              <div className="flex items-center space-x-2">
                <AlertTriangle className="w-3 h-3 text-orange-600" />
                <span>Pollution</span>
              </div>
              <div className="flex items-center space-x-2">
                <Trash2 className="w-3 h-3 text-gray-600" />
                <span>Debris</span>
              </div>
              <div className="flex items-center space-x-2">
                <Thermometer className="w-3 h-3 text-red-600" />
                <span>Temperature</span>
              </div>
            </div>
          </div>

          {/* Zoom level indicator */}
          <div className="absolute top-4 left-4 bg-white rounded-lg shadow-lg px-3 py-1">
            <span className="text-sm font-medium">Zoom: {zoomLevel}x</span>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
