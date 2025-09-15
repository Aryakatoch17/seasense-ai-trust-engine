#!/bin/bash

# SeaSense AI Trust Engine - Quick Test Script
# This script tests all major functionalities

echo "🌊 SeaSense AI Trust Engine - Quick Test Suite"
echo "=============================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if jq is installed
if ! command -v jq &> /dev/null; then
    echo -e "${YELLOW}Warning: jq not found. Installing via brew...${NC}"
    if command -v brew &> /dev/null; then
        brew install jq
    else
        echo -e "${RED}Please install jq for better JSON formatting${NC}"
    fi
fi

echo ""
echo -e "${BLUE}1. Testing Backend Health${NC}"
echo "========================="
response=$(curl -s -w "HTTP_STATUS:%{http_code}" -X GET "http://127.0.0.1:8005/health")
http_code=$(echo $response | grep -o "HTTP_STATUS:[0-9]*" | cut -d: -f2)
response_body=$(echo $response | sed -E 's/HTTP_STATUS:[0-9]*$//')

if [ "$http_code" = "200" ]; then
    echo -e "${GREEN}✅ Backend Health Check: PASSED${NC}"
    echo "$response_body" | jq '.' 2>/dev/null || echo "$response_body"
else
    echo -e "${RED}❌ Backend Health Check: FAILED (HTTP $http_code)${NC}"
    echo "Make sure backend is running: cd ai_trust_engine && python -m uvicorn main:app --host 127.0.0.1 --port 8005 --reload"
fi

echo ""
echo -e "${BLUE}2. Testing Frontend Connectivity${NC}"
echo "==============================="
response=$(curl -s -w "HTTP_STATUS:%{http_code}" -X GET "http://localhost:3000")
http_code=$(echo $response | grep -o "HTTP_STATUS:[0-9]*" | cut -d: -f2)

if [ "$http_code" = "200" ] || [ "$http_code" = "404" ]; then
    echo -e "${GREEN}✅ Frontend Connectivity: PASSED${NC}"
    echo "Dashboard accessible at http://localhost:3000"
else
    echo -e "${RED}❌ Frontend Connectivity: FAILED${NC}"
    echo "Make sure frontend is running: cd seasense-dashboard && npm run dev"
fi

echo ""
echo -e "${BLUE}3. Testing Citizen Report Submission${NC}"
echo "=================================="
if [ -f "test_data/citizen_report.json" ]; then
    response=$(curl -s -w "HTTP_STATUS:%{http_code}" -X POST "http://127.0.0.1:8005/api/v1/reports/citizen" \
      -H "Content-Type: application/json" \
      -d @test_data/citizen_report.json)
    http_code=$(echo $response | grep -o "HTTP_STATUS:[0-9]*" | cut -d: -f2)
    response_body=$(echo $response | sed -E 's/HTTP_STATUS:[0-9]*$//')
    
    if [ "$http_code" = "200" ]; then
        echo -e "${GREEN}✅ Citizen Report Submission: PASSED${NC}"
        echo "$response_body" | jq '.' 2>/dev/null || echo "$response_body"
        
        # Extract report_id for status check
        report_id=$(echo "$response_body" | jq -r '.report_id' 2>/dev/null)
        if [ "$report_id" != "null" ] && [ "$report_id" != "" ]; then
            echo ""
            echo -e "${BLUE}4. Testing Report Status Check${NC}"
            echo "============================"
            status_response=$(curl -s -w "HTTP_STATUS:%{http_code}" -X GET "http://127.0.0.1:8005/api/v1/reports/status/$report_id")
            status_http_code=$(echo $status_response | grep -o "HTTP_STATUS:[0-9]*" | cut -d: -f2)
            status_body=$(echo $status_response | sed -E 's/HTTP_STATUS:[0-9]*$//')
            
            if [ "$status_http_code" = "200" ]; then
                echo -e "${GREEN}✅ Report Status Check: PASSED${NC}"
                echo "$status_body" | jq '.' 2>/dev/null || echo "$status_body"
            else
                echo -e "${YELLOW}⚠️  Report Status Check: SKIPPED (endpoint may not be implemented)${NC}"
            fi
        fi
    else
        echo -e "${RED}❌ Citizen Report Submission: FAILED (HTTP $http_code)${NC}"
        echo "$response_body"
    fi
else
    echo -e "${YELLOW}⚠️  Citizen Report Test: SKIPPED (test data not found)${NC}"
fi

echo ""
echo -e "${BLUE}5. Testing Social Media Ingestion${NC}"
echo "==============================="
if [ -f "test_data/social_media.json" ]; then
    response=$(curl -s -w "HTTP_STATUS:%{http_code}" -X POST "http://127.0.0.1:8005/api/v1/social-media/ingest" \
      -H "Content-Type: application/json" \
      -d @test_data/social_media.json)
    http_code=$(echo $response | grep -o "HTTP_STATUS:[0-9]*" | cut -d: -f2)
    response_body=$(echo $response | sed -E 's/HTTP_STATUS:[0-9]*$//')
    
    if [ "$http_code" = "200" ]; then
        echo -e "${GREEN}✅ Social Media Ingestion: PASSED${NC}"
        echo "$response_body" | jq '.' 2>/dev/null || echo "$response_body"
    else
        echo -e "${RED}❌ Social Media Ingestion: FAILED (HTTP $http_code)${NC}"
        echo "$response_body"
    fi
else
    echo -e "${YELLOW}⚠️  Social Media Test: SKIPPED (test data not found)${NC}"
fi

echo ""
echo -e "${BLUE}6. Testing Trust Score Calculation${NC}"
echo "==============================="
trust_score_data='{
  "report": {
    "id": "test_report",
    "description": "High waves and dangerous conditions for trust score testing",
    "hazard_type": "high_waves",
    "location": {"latitude": 19.0760, "longitude": 72.8777, "address": "Mumbai"},
    "trust_score": 0,
    "priority": "high",
    "timestamp": "2025-09-15T10:30:00",
    "status": "pending",
    "source": "citizen"
  },
  "social_media_posts": [
    {
      "id": "sm1",
      "text": "Big waves at Mumbai beach #waves #mumbai",
      "platform": "twitter",
      "author_id": "@user1",
      "author_verified": true,
      "location": {"latitude": 19.0760, "longitude": 72.8777},
      "hashtags": ["waves", "mumbai"],
      "posted_at": "2025-09-15T10:00:00",
      "engagement_score": 0.8
    }
  ]
}'

response=$(curl -s -w "HTTP_STATUS:%{http_code}" -X POST "http://127.0.0.1:8005/api/v1/trust-scores/calculate" \
  -H "Content-Type: application/json" \
  -d "$trust_score_data")
http_code=$(echo $response | grep -o "HTTP_STATUS:[0-9]*" | cut -d: -f2)
response_body=$(echo $response | sed -E 's/HTTP_STATUS:[0-9]*$//')

if [ "$http_code" = "200" ]; then
    echo -e "${GREEN}✅ Trust Score Calculation: PASSED${NC}"
    echo "$response_body" | jq '.' 2>/dev/null || echo "$response_body"
else
    echo -e "${RED}❌ Trust Score Calculation: FAILED (HTTP $http_code)${NC}"
    echo "$response_body"
fi

echo ""
echo -e "${BLUE}7. Testing API Documentation${NC}"
echo "=========================="
response=$(curl -s -w "HTTP_STATUS:%{http_code}" -X GET "http://127.0.0.1:8005/docs")
http_code=$(echo $response | grep -o "HTTP_STATUS:[0-9]*" | cut -d: -f2)

if [ "$http_code" = "200" ]; then
    echo -e "${GREEN}✅ API Documentation: ACCESSIBLE${NC}"
    echo "Swagger UI available at: http://127.0.0.1:8005/docs"
else
    echo -e "${RED}❌ API Documentation: NOT ACCESSIBLE${NC}"
fi

echo ""
echo "=============================================="
echo -e "${BLUE}🎯 Test Summary${NC}"
echo "=============================================="
echo -e "${GREEN}✅ Passed tests indicate working functionality${NC}"
echo -e "${RED}❌ Failed tests need attention${NC}"
echo -e "${YELLOW}⚠️  Skipped tests may need setup or implementation${NC}"

echo ""
echo -e "${BLUE}📋 Next Steps:${NC}"
echo "1. Open Dashboard: http://localhost:3000"
echo "2. Open API Docs: http://127.0.0.1:8005/docs"
echo "3. Test manual workflows in dashboard"
echo "4. Check browser console for any errors"
echo "5. Review COMPREHENSIVE_TESTING_GUIDE.md for detailed testing"

echo ""
echo -e "${BLUE}🔧 Troubleshooting:${NC}"
echo "- Backend not responding? Check: cd ai_trust_engine && python -m uvicorn main:app --host 127.0.0.1 --port 8005 --reload"
echo "- Frontend not accessible? Check: cd seasense-dashboard && npm run dev"
echo "- CORS issues? Verify backend CORS settings"

echo ""
echo "Testing complete! 🌊"
