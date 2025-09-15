"use client"

import { useState, useMemo } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Checkbox } from "@/components/ui/checkbox"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
  DropdownMenuSeparator,
} from "@/components/ui/dropdown-menu"
import {
  Filter,
  Search,
  Download,
  Eye,
  CheckCircle,
  Flag,
  MoreHorizontal,
  ArrowUpDown,
  MapPin,
  Clock,
} from "lucide-react"

interface Report {
  id: string
  timestamp: string
  location: string
  coordinates: { lat: number; lng: number }
  hazardType: string
  trustScore: number
  status: "Verified" | "Pending" | "Flagged" | "Rejected"
  priority: "critical" | "high" | "medium" | "low"
  source: string
  description: string
  images?: string[]
  reportedBy: string
  verifiedBy?: string
}

export default function ReportsTable() {
  const [selectedReports, setSelectedReports] = useState<string[]>([])
  const [searchTerm, setSearchTerm] = useState("")
  const [statusFilter, setStatusFilter] = useState("all")
  const [hazardFilter, setHazardFilter] = useState("all")
  const [priorityFilter, setPriorityFilter] = useState("all")
  const [sortBy, setSortBy] = useState("timestamp")
  const [sortOrder, setSortOrder] = useState<"asc" | "desc">("desc")
  const [currentPage, setCurrentPage] = useState(1)
  const itemsPerPage = 10

  const mockReports: Report[] = [
    {
      id: "RPT001",
      timestamp: "2024-12-13T14:30:00Z",
      location: "Mumbai Beach, Maharashtra",
      coordinates: { lat: 19.076, lng: 72.877 },
      hazardType: "High Waves",
      trustScore: 0.85,
      status: "Verified",
      priority: "critical",
      source: "Citizen Report",
      description: "Massive waves hitting Mumbai coastline, 4-5 meter height observed",
      reportedBy: "Rajesh Kumar",
      verifiedBy: "Coast Guard Mumbai",
    },
    {
      id: "RPT002",
      timestamp: "2024-12-13T14:15:00Z",
      location: "Goa Coast, Goa",
      coordinates: { lat: 15.2993, lng: 74.124 },
      hazardType: "Pollution",
      trustScore: 0.72,
      status: "Pending",
      priority: "high",
      source: "Social Media",
      description: "Oil spill detected near Goa coast, affecting marine life",
      reportedBy: "Anonymous",
    },
    {
      id: "RPT003",
      timestamp: "2024-12-13T14:00:00Z",
      location: "Chennai Marina, Tamil Nadu",
      coordinates: { lat: 13.0827, lng: 80.2707 },
      hazardType: "Debris",
      trustScore: 0.91,
      status: "Verified",
      priority: "medium",
      source: "Official Sensor",
      description: "Large debris field observed near Chennai Marina",
      reportedBy: "Chennai Port Authority",
      verifiedBy: "Marine Police",
    },
    {
      id: "RPT004",
      timestamp: "2024-12-13T13:45:00Z",
      location: "Kochi Port, Kerala",
      coordinates: { lat: 9.9312, lng: 76.2673 },
      hazardType: "High Waves",
      trustScore: 0.89,
      status: "Verified",
      priority: "high",
      source: "Coast Guard",
      description: "High waves near Kochi, affecting fishing activities",
      reportedBy: "Coast Guard Kochi",
      verifiedBy: "Harbor Master",
    },
    {
      id: "RPT005",
      timestamp: "2024-12-13T13:30:00Z",
      location: "Visakhapatnam, Andhra Pradesh",
      coordinates: { lat: 17.6868, lng: 83.2185 },
      hazardType: "Temperature Anomaly",
      trustScore: 0.64,
      status: "Flagged",
      priority: "low",
      source: "Citizen Report",
      description: "Unusual water temperature spike reported by fishermen",
      reportedBy: "Local Fishermen",
    },
    {
      id: "RPT006",
      timestamp: "2024-12-13T13:15:00Z",
      location: "Puri Beach, Odisha",
      coordinates: { lat: 19.8135, lng: 85.8312 },
      hazardType: "Strong Currents",
      trustScore: 0.78,
      status: "Pending",
      priority: "medium",
      source: "Lifeguard Report",
      description: "Dangerous rip currents observed, swimmers advised to stay away",
      reportedBy: "Beach Lifeguard",
    },
    {
      id: "RPT007",
      timestamp: "2024-12-13T13:00:00Z",
      location: "Mangalore Coast, Karnataka",
      coordinates: { lat: 12.9141, lng: 74.856 },
      hazardType: "Pollution",
      trustScore: 0.83,
      status: "Verified",
      priority: "high",
      source: "Environmental Agency",
      description: "Chemical discharge detected in coastal waters",
      reportedBy: "Karnataka Pollution Board",
      verifiedBy: "Environmental Inspector",
    },
    {
      id: "RPT008",
      timestamp: "2024-12-13T12:45:00Z",
      location: "Paradip Port, Odisha",
      coordinates: { lat: 20.2648, lng: 86.6947 },
      hazardType: "Debris",
      trustScore: 0.76,
      status: "Pending",
      priority: "low",
      source: "Port Authority",
      description: "Floating debris affecting port operations",
      reportedBy: "Port Operations",
    },
  ]

  const filteredReports = useMemo(() => {
    const filtered = mockReports.filter((report) => {
      const matchesSearch =
        report.location.toLowerCase().includes(searchTerm.toLowerCase()) ||
        report.hazardType.toLowerCase().includes(searchTerm.toLowerCase()) ||
        report.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
        report.reportedBy.toLowerCase().includes(searchTerm.toLowerCase())

      const matchesStatus = statusFilter === "all" || report.status === statusFilter
      const matchesHazard = hazardFilter === "all" || report.hazardType === hazardFilter
      const matchesPriority = priorityFilter === "all" || report.priority === priorityFilter

      return matchesSearch && matchesStatus && matchesHazard && matchesPriority
    })

    // Sort reports
    filtered.sort((a, b) => {
      let aValue: any = a[sortBy as keyof Report]
      let bValue: any = b[sortBy as keyof Report]

      if (sortBy === "timestamp") {
        aValue = new Date(aValue).getTime()
        bValue = new Date(bValue).getTime()
      } else if (sortBy === "trustScore") {
        aValue = Number(aValue)
        bValue = Number(bValue)
      }

      if (sortOrder === "asc") {
        return aValue > bValue ? 1 : -1
      } else {
        return aValue < bValue ? 1 : -1
      }
    })

    return filtered
  }, [mockReports, searchTerm, statusFilter, hazardFilter, priorityFilter, sortBy, sortOrder])

  const paginatedReports = useMemo(() => {
    const startIndex = (currentPage - 1) * itemsPerPage
    return filteredReports.slice(startIndex, startIndex + itemsPerPage)
  }, [filteredReports, currentPage, itemsPerPage])

  const totalPages = Math.ceil(filteredReports.length / itemsPerPage)

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case "critical":
        return "bg-red-600 text-white"
      case "high":
        return "bg-red-500 text-white"
      case "medium":
        return "bg-orange-500 text-white"
      case "low":
        return "bg-yellow-500 text-white"
      default:
        return "bg-gray-500 text-white"
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case "Verified":
        return "bg-green-100 text-green-800"
      case "Pending":
        return "bg-yellow-100 text-yellow-800"
      case "Flagged":
        return "bg-red-100 text-red-800"
      case "Rejected":
        return "bg-gray-100 text-gray-800"
      default:
        return "bg-gray-100 text-gray-800"
    }
  }

  const getTrustScoreColor = (score: number) => {
    if (score >= 0.8) return "text-green-600 font-semibold"
    if (score >= 0.6) return "text-yellow-600 font-semibold"
    return "text-red-600 font-semibold"
  }

  const handleSelectAll = (checked: boolean) => {
    if (checked) {
      setSelectedReports(paginatedReports.map((report) => report.id))
    } else {
      setSelectedReports([])
    }
  }

  const handleSelectReport = (reportId: string, checked: boolean) => {
    if (checked) {
      setSelectedReports([...selectedReports, reportId])
    } else {
      setSelectedReports(selectedReports.filter((id) => id !== reportId))
    }
  }

  const handleBulkAction = (action: string) => {
    console.log(`Performing ${action} on reports:`, selectedReports)
    // Implement bulk actions here
    setSelectedReports([])
  }

  const handleSort = (field: string) => {
    if (sortBy === field) {
      setSortOrder(sortOrder === "asc" ? "desc" : "asc")
    } else {
      setSortBy(field)
      setSortOrder("desc")
    }
  }

  return (
    <Card>
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle className="flex items-center space-x-2">
            <Filter className="h-5 w-5 text-blue-600" />
            <span>Reports Management</span>
            <Badge variant="secondary">{filteredReports.length} reports</Badge>
          </CardTitle>
          <div className="flex items-center space-x-2">
            {selectedReports.length > 0 && (
              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <Button variant="outline" size="sm">
                    Bulk Actions ({selectedReports.length})
                  </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent>
                  <DropdownMenuItem onClick={() => handleBulkAction("verify")}>
                    <CheckCircle className="w-4 h-4 mr-2" />
                    Verify Selected
                  </DropdownMenuItem>
                  <DropdownMenuItem onClick={() => handleBulkAction("flag")}>
                    <Flag className="w-4 h-4 mr-2" />
                    Flag Selected
                  </DropdownMenuItem>
                  <DropdownMenuSeparator />
                  <DropdownMenuItem onClick={() => handleBulkAction("export")}>
                    <Download className="w-4 h-4 mr-2" />
                    Export Selected
                  </DropdownMenuItem>
                </DropdownMenuContent>
              </DropdownMenu>
            )}
            <Button variant="outline" size="sm">
              <Download className="w-4 h-4 mr-2" />
              Export All
            </Button>
          </div>
        </div>

        {/* Filters */}
        <div className="flex flex-wrap items-center gap-4 mt-4">
          <div className="flex items-center space-x-2">
            <Search className="w-4 h-4 text-gray-500" />
            <Input
              placeholder="Search reports..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-64"
            />
          </div>

          <Select value={statusFilter} onValueChange={setStatusFilter}>
            <SelectTrigger className="w-32">
              <SelectValue placeholder="Status" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All Status</SelectItem>
              <SelectItem value="Verified">Verified</SelectItem>
              <SelectItem value="Pending">Pending</SelectItem>
              <SelectItem value="Flagged">Flagged</SelectItem>
              <SelectItem value="Rejected">Rejected</SelectItem>
            </SelectContent>
          </Select>

          <Select value={hazardFilter} onValueChange={setHazardFilter}>
            <SelectTrigger className="w-40">
              <SelectValue placeholder="Hazard Type" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All Types</SelectItem>
              <SelectItem value="High Waves">High Waves</SelectItem>
              <SelectItem value="Pollution">Pollution</SelectItem>
              <SelectItem value="Debris">Debris</SelectItem>
              <SelectItem value="Temperature Anomaly">Temperature</SelectItem>
              <SelectItem value="Strong Currents">Currents</SelectItem>
            </SelectContent>
          </Select>

          <Select value={priorityFilter} onValueChange={setPriorityFilter}>
            <SelectTrigger className="w-32">
              <SelectValue placeholder="Priority" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All Priority</SelectItem>
              <SelectItem value="critical">Critical</SelectItem>
              <SelectItem value="high">High</SelectItem>
              <SelectItem value="medium">Medium</SelectItem>
              <SelectItem value="low">Low</SelectItem>
            </SelectContent>
          </Select>

          <Button
            variant="outline"
            size="sm"
            onClick={() => {
              setSearchTerm("")
              setStatusFilter("all")
              setHazardFilter("all")
              setPriorityFilter("all")
            }}
          >
            Clear Filters
          </Button>
        </div>
      </CardHeader>

      <CardContent>
        {/* Table Header */}
        <div className="border rounded-lg">
          <div className="grid grid-cols-12 gap-4 p-3 bg-gray-50 border-b font-medium text-sm">
            <div className="col-span-1 flex items-center">
              <Checkbox
                checked={selectedReports.length === paginatedReports.length && paginatedReports.length > 0}
                onCheckedChange={handleSelectAll}
              />
            </div>
            <div className="col-span-2 flex items-center space-x-1">
              <button
                onClick={() => handleSort("timestamp")}
                className="flex items-center space-x-1 hover:text-blue-600"
              >
                <Clock className="w-4 h-4" />
                <span>Time</span>
                <ArrowUpDown className="w-3 h-3" />
              </button>
            </div>
            <div className="col-span-2 flex items-center space-x-1">
              <button
                onClick={() => handleSort("location")}
                className="flex items-center space-x-1 hover:text-blue-600"
              >
                <MapPin className="w-4 h-4" />
                <span>Location</span>
                <ArrowUpDown className="w-3 h-3" />
              </button>
            </div>
            <div className="col-span-2">Hazard Type</div>
            <div className="col-span-1 flex items-center space-x-1">
              <button
                onClick={() => handleSort("trustScore")}
                className="flex items-center space-x-1 hover:text-blue-600"
              >
                <span>Trust</span>
                <ArrowUpDown className="w-3 h-3" />
              </button>
            </div>
            <div className="col-span-1">Status</div>
            <div className="col-span-1">Priority</div>
            <div className="col-span-2">Actions</div>
          </div>

          {/* Table Body */}
          <div className="divide-y">
            {paginatedReports.map((report) => (
              <div key={report.id} className="grid grid-cols-12 gap-4 p-3 hover:bg-gray-50 transition-colors">
                <div className="col-span-1 flex items-center">
                  <Checkbox
                    checked={selectedReports.includes(report.id)}
                    onCheckedChange={(checked) => handleSelectReport(report.id, checked as boolean)}
                  />
                </div>
                <div className="col-span-2">
                  <div className="text-sm font-medium">{new Date(report.timestamp).toLocaleDateString()}</div>
                  <div className="text-xs text-gray-500">{new Date(report.timestamp).toLocaleTimeString()}</div>
                </div>
                <div className="col-span-2">
                  <div className="text-sm font-medium">{report.location.split(",")[0]}</div>
                  <div className="text-xs text-gray-500">{report.source}</div>
                </div>
                <div className="col-span-2">
                  <Badge variant="outline" className="text-xs">
                    {report.hazardType}
                  </Badge>
                </div>
                <div className="col-span-1">
                  <span className={`text-sm ${getTrustScoreColor(report.trustScore)}`}>
                    {(report.trustScore * 100).toFixed(0)}%
                  </span>
                </div>
                <div className="col-span-1">
                  <Badge className={`text-xs ${getStatusColor(report.status)}`}>{report.status}</Badge>
                </div>
                <div className="col-span-1">
                  <Badge className={`text-xs ${getPriorityColor(report.priority)}`}>{report.priority}</Badge>
                </div>
                <div className="col-span-2 flex items-center space-x-1">
                  <Button variant="outline" size="sm">
                    <Eye className="w-3 h-3" />
                  </Button>
                  <Button variant="outline" size="sm">
                    <CheckCircle className="w-3 h-3" />
                  </Button>
                  <DropdownMenu>
                    <DropdownMenuTrigger asChild>
                      <Button variant="outline" size="sm">
                        <MoreHorizontal className="w-3 h-3" />
                      </Button>
                    </DropdownMenuTrigger>
                    <DropdownMenuContent>
                      <DropdownMenuItem>View Details</DropdownMenuItem>
                      <DropdownMenuItem>Edit Report</DropdownMenuItem>
                      <DropdownMenuItem>Flag as Suspicious</DropdownMenuItem>
                      <DropdownMenuSeparator />
                      <DropdownMenuItem className="text-red-600">Delete Report</DropdownMenuItem>
                    </DropdownMenuContent>
                  </DropdownMenu>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Pagination */}
        <div className="flex items-center justify-between mt-4">
          <div className="text-sm text-gray-500">
            Showing {(currentPage - 1) * itemsPerPage + 1} to{" "}
            {Math.min(currentPage * itemsPerPage, filteredReports.length)} of {filteredReports.length} reports
          </div>
          <div className="flex items-center space-x-2">
            <Button
              variant="outline"
              size="sm"
              onClick={() => setCurrentPage(Math.max(1, currentPage - 1))}
              disabled={currentPage === 1}
            >
              Previous
            </Button>
            <div className="flex items-center space-x-1">
              {Array.from({ length: Math.min(5, totalPages) }, (_, i) => {
                const page = i + 1
                return (
                  <Button
                    key={page}
                    variant={currentPage === page ? "default" : "outline"}
                    size="sm"
                    onClick={() => setCurrentPage(page)}
                    className="w-8 h-8 p-0"
                  >
                    {page}
                  </Button>
                )
              })}
            </div>
            <Button
              variant="outline"
              size="sm"
              onClick={() => setCurrentPage(Math.min(totalPages, currentPage + 1))}
              disabled={currentPage === totalPages}
            >
              Next
            </Button>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
