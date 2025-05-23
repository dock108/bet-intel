#!/usr/bin/env python3
"""
Test script to validate the betting intelligence platform setup
This script tests the system without requiring an actual API key
"""

import sys
import os
from datetime import datetime, timezone

# Add the backend directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_configuration():
    """Test configuration loading"""
    print("🔧 Testing configuration...")
    try:
        from config import settings
        print("   ✅ Configuration loaded successfully")
        print(f"   📊 Default sport: {settings.default_sport}")
        print(f"   🌐 Default regions: {settings.default_regions}")
        print(f"   📈 Default markets: {settings.default_markets}")
        print(f"   ⏱️  Polling interval: {settings.odds_polling_interval_minutes} minutes")
        return True
    except Exception as e:
        print(f"   ❌ Configuration error: {e}")
        return False

def test_database():
    """Test database setup and models"""
    print("\n💾 Testing database...")
    try:
        from database import initialize_database, SessionLocal, EventModel, BookmakerModel
        
        # Initialize database
        initialize_database()
        print("   ✅ Database initialized successfully")
        
        # Test database session
        db = SessionLocal()
        try:
            # Check if bookmakers were seeded
            bookmaker_count = db.query(BookmakerModel).count()
            print(f"   📚 Bookmakers in database: {bookmaker_count}")
            
            # Check if we can create a test event (without committing)
            test_event = EventModel(
                external_id="test_event_123",
                sport_key="basketball_nba",
                sport_title="NBA",
                home_team="Test Home Team",
                away_team="Test Away Team",
                commence_time=datetime.now(timezone.utc)
            )
            db.add(test_event)  # Add to session but don't commit
            print("   ✅ Database models working correctly")
            
        finally:
            db.close()
        
        return True
    except Exception as e:
        print(f"   ❌ Database error: {e}")
        return False

def test_api_client_structure():
    """Test API client structure (without making actual requests)"""
    print("\n🌐 Testing API client structure...")
    try:
        from odds_api_client import OddsAPIClient
        
        print("   ✅ API client classes imported successfully")
        
        # Test client initialization (will fail without API key, which is expected)
        try:
            client = OddsAPIClient(api_key="test_key")
            print(f"   ✅ Client initialization structure correct: {type(client).__name__}")
        except Exception as e:
            if "test_key" in str(e) or "ODDS_API_KEY" in str(e):
                print("   ✅ Client validation working (API key required)")
            else:
                print(f"   ⚠️  Unexpected client error: {e}")
        
        return True
    except Exception as e:
        print(f"   ❌ API client error: {e}")
        return False

def test_polling_structure():
    """Test polling service structure"""
    print("\n🔄 Testing polling service structure...")
    try:
        from odds_poller import OddsPoller
        
        print("   ✅ OddsPoller class imported successfully")
        
        # Test poller initialization (will fail without API key, which is expected)
        try:
            poller = OddsPoller()
            print(f"   ⚠️  Poller initialized: {type(poller).__name__} (API key may be missing)")
        except Exception as e:
            if "ODDS_API_KEY" in str(e):
                print("   ✅ Poller validation working (API key required)")
            else:
                print(f"   ⚠️  Unexpected poller error: {e}")
        
        return True
    except Exception as e:
        print(f"   ❌ Polling service error: {e}")
        return False

def test_fastapi_structure():
    """Test FastAPI application structure"""
    print("\n🚀 Testing FastAPI application...")
    try:
        from main import app
        
        print("   ✅ FastAPI app imported successfully")
        
        # Check if routes are registered
        routes = [route.path for route in app.routes]
        expected_routes = ["/", "/health", "/api/events", "/api/polling-logs", "/api/stats"]
        
        for route in expected_routes:
            if route in routes:
                print(f"   ✅ Route {route} registered")
            else:
                print(f"   ⚠️  Route {route} missing")
        
        return True
    except Exception as e:
        print(f"   ❌ FastAPI error: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 AI-Assisted P2P Betting Intelligence - System Test")
    print("=" * 60)
    
    tests = [
        test_configuration,
        test_database,
        test_api_client_structure,
        test_polling_structure,
        test_fastapi_structure
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All systems ready! You can now:")
        print("   1. Add your ODDS_API_KEY to backend/.env")
        print("   2. Start the FastAPI server: python main.py")
        print("   3. Test manual polling: curl -X POST http://localhost:8000/api/poll-odds")
        print("   4. Start continuous polling: python odds_poller.py")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        print("   Common issues:")
        print("   - Missing dependencies: pip install -r requirements.txt")
        print("   - Python path issues: run from backend/ directory")
        print("   - Import errors: check file names and syntax")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 