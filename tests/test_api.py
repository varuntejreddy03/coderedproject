"""
PumpWatch API Test Suite
Tests all endpoints and reports results with nice formatting
"""
import requests
import json
from datetime import datetime
from typing import Dict, List
import time

BASE_URL = "http://localhost:8080"
TEST_TICKER = "YESBANK"  # Use a ticker that should have data

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text.center(70)}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.RESET}\n")

def print_success(text):
    print(f"{Colors.GREEN}[OK] {text}{Colors.RESET}")

def print_error(text):
    print(f"{Colors.RED}[ERROR] {text}{Colors.RESET}")

def print_warning(text):
    print(f"{Colors.YELLOW}[WARN] {text}{Colors.RESET}")

def print_info(text):
    print(f"{Colors.BLUE}[INFO] {text}{Colors.RESET}")

def test_endpoint(name: str, url: str, expected_keys: List[str] = None) -> Dict:
    """Test a single endpoint"""
    result = {
        "name": name,
        "url": url,
        "status": "PASS",
        "response_time": 0,
        "error": None,
        "data": None
    }
    
    try:
        start_time = time.time()
        response = requests.get(url, timeout=30)
        result["response_time"] = round((time.time() - start_time) * 1000, 2)  # ms
        
        if response.status_code == 200:
            data = response.json()
            result["data"] = data
            
            # Check expected keys
            if expected_keys:
                missing_keys = [key for key in expected_keys if key not in data]
                if missing_keys:
                    result["status"] = "WARNING"
                    result["error"] = f"Missing keys: {missing_keys}"
                    print_warning(f"{name}: Missing keys {missing_keys}")
                else:
                    print_success(f"{name}: {result['response_time']}ms")
            else:
                print_success(f"{name}: {result['response_time']}ms")
        
        elif response.status_code == 404:
            result["status"] = "WARNING"
            result["error"] = f"404 Not Found - {response.json().get('detail', 'No data')}"
            print_warning(f"{name}: {result['error']}")
        
        elif response.status_code == 503:
            result["status"] = "WARNING"
            result["error"] = f"503 Service Unavailable - {response.json().get('detail', 'Service not ready')}"
            print_warning(f"{name}: {result['error']}")
        
        else:
            result["status"] = "FAIL"
            result["error"] = f"HTTP {response.status_code}: {response.text[:100]}"
            print_error(f"{name}: {result['error']}")
    
    except requests.exceptions.ConnectionError:
        result["status"] = "FAIL"
        result["error"] = "Connection refused - Is the server running?"
        print_error(f"{name}: {result['error']}")
    
    except requests.exceptions.Timeout:
        result["status"] = "FAIL"
        result["error"] = "Request timeout (>30s)"
        print_error(f"{name}: {result['error']}")
    
    except Exception as e:
        result["status"] = "FAIL"
        result["error"] = str(e)
        print_error(f"{name}: {result['error']}")
    
    return result

def run_tests():
    """Run all API tests"""
    print_header("PUMPWATCH API TEST SUITE")
    print_info(f"Testing API at: {BASE_URL}")
    print_info(f"Test Ticker: {TEST_TICKER}")
    print_info(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    results = []
    
    # ========================================================================
    # UTILITY APIs
    # ========================================================================
    print_header("UTILITY APIs")
    
    # First, refresh messages from Telegram
    print_info("Refreshing Telegram messages...")
    results.append(test_endpoint(
        "Refresh Messages",
        f"{BASE_URL}/refresh",
        ["status", "messages_count", "tickers_found"]
    ))
    
    results.append(test_endpoint(
        "Health Check",
        f"{BASE_URL}/health",
        ["status", "uptime_seconds", "telegram_active"]
    ))
    
    # ========================================================================
    # CORE DETECTION APIs
    # ========================================================================
    print_header("CORE DETECTION APIs")
    
    results.append(test_endpoint(
        "Fraud Alerts",
        f"{BASE_URL}/fraud-alerts?min_risk=2",
        ["high_risk_messages", "total_alerts", "hinglish_examples"]
    ))
    
    results.append(test_endpoint(
        "Safety Dashboard",
        f"{BASE_URL}/safety-dashboard",
        ["red_alerts", "amber_alerts", "green_stocks", "summary"]
    ))
    
    results.append(test_endpoint(
        f"Reality Check ({TEST_TICKER})",
        f"{BASE_URL}/reality-check/{TEST_TICKER}",
        ["ticker", "safety_indicator", "risk_level"]
    ))
    
    results.append(test_endpoint(
        f"Hype Intensity ({TEST_TICKER})",
        f"{BASE_URL}/hype-intensity/{TEST_TICKER}",
        ["ticker", "hype_score", "risk_level"]
    ))
    
    # ========================================================================
    # NEW REQUIRED APIs
    # ========================================================================
    print_header("NEW REQUIRED APIs")
    
    results.append(test_endpoint(
        f"Risk Score ({TEST_TICKER})",
        f"{BASE_URL}/risk-score/{TEST_TICKER}",
        ["risk_score", "risk_level", "color_indicator", "components"]
    ))
    
    results.append(test_endpoint(
        "Anomaly Detection",
        f"{BASE_URL}/anomaly-detection",
        ["anomalies", "total_checked"]
    ))
    
    results.append(test_endpoint(
        f"Bot Activity ({TEST_TICKER})",
        f"{BASE_URL}/bot-activity/{TEST_TICKER}",
        ["bot_activity_detected", "confidence", "indicators"]
    ))
    
    results.append(test_endpoint(
        f"Why Risky ({TEST_TICKER})",
        f"{BASE_URL}/why-risky/{TEST_TICKER}",
        ["explanation", "risk_score", "color_indicator"]
    ))
    
    # ========================================================================
    # DATA SOURCE APIs
    # ========================================================================
    print_header("DATA SOURCE APIs")
    
    results.append(test_endpoint(
        "Reddit Hype",
        f"{BASE_URL}/reddit-hype?limit=5",
        ["top_hyped_stocks", "count"]
    ))
    
    results.append(test_endpoint(
        "All Tickers",
        f"{BASE_URL}/tickers"
    ))
    
    # ========================================================================
    # SUMMARY
    # ========================================================================
    print_header("TEST SUMMARY")
    
    passed = sum(1 for r in results if r["status"] == "PASS")
    warnings = sum(1 for r in results if r["status"] == "WARNING")
    failed = sum(1 for r in results if r["status"] == "FAIL")
    total = len(results)
    
    print(f"Total Tests: {total}")
    print_success(f"Passed: {passed}")
    print_warning(f"Warnings: {warnings}")
    print_error(f"Failed: {failed}")
    
    # Average response time
    response_times = [r["response_time"] for r in results if r["response_time"] > 0]
    if response_times:
        avg_time = sum(response_times) / len(response_times)
        print_info(f"Average Response Time: {avg_time:.2f}ms")
    
    # Failed tests details
    if failed > 0:
        print_header("FAILED TESTS DETAILS")
        for r in results:
            if r["status"] == "FAIL":
                print_error(f"{r['name']}")
                print(f"  URL: {r['url']}")
                print(f"  Error: {r['error']}\n")
    
    # Warnings details
    if warnings > 0:
        print_header("WARNINGS DETAILS")
        for r in results:
            if r["status"] == "WARNING":
                print_warning(f"{r['name']}")
                print(f"  URL: {r['url']}")
                print(f"  Issue: {r['error']}\n")
    
    # Save results to file
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    report_file = f"test_report_{timestamp}.json"
    
    with open(report_file, 'w') as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total": total,
                "passed": passed,
                "warnings": warnings,
                "failed": failed,
                "avg_response_time_ms": round(avg_time, 2) if response_times else 0
            },
            "results": results
        }, f, indent=2)
    
    print_info(f"Detailed report saved to: {report_file}")
    
    # Return exit code
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    try:
        exit_code = run_tests()
        print(f"\n{Colors.BOLD}Test completed with exit code: {exit_code}{Colors.RESET}\n")
        exit(exit_code)
    except KeyboardInterrupt:
        print_warning("\n\nTests interrupted by user")
        exit(1)
    except Exception as e:
        print_error(f"\n\nUnexpected error: {e}")
        exit(1)
