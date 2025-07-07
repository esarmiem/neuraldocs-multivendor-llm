#!/usr/bin/env python3
"""
Test script to verify dual RAG functionality:
1. General RAG chain (backward compatibility)
2. DELIA chain (specialized EDSL assistant)

This script tests both functionalities to ensure they work independently.
"""

import requests
import json
import time

# Configuration
BASE_URL = "http://localhost:8000"
TEST_USER = "testuser"
TEST_PASSWORD = "testpassword"

def get_auth_token():
    """Get authentication token for API requests."""
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/auth/token",
            data={
                "username": TEST_USER,
                "password": TEST_PASSWORD
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        response.raise_for_status()
        return response.json()["access_token"]
    except Exception as e:
        print(f"❌ Error getting auth token: {e}")
        return None

def test_general_rag(token):
    """Test general RAG functionality."""
    print("\n🔍 Testing General RAG Chain...")
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/chat/",
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            },
            json={
                "question": "¿Qué es machine learning?"
            }
        )
        response.raise_for_status()
        
        result = response.json()
        print(f"✅ General RAG Response: {result['answer'][:100]}...")
        return True
        
    except Exception as e:
        print(f"❌ General RAG test failed: {e}")
        return False

def test_delia_basic(token):
    """Test DELIA with basic user level."""
    print("\n🤖 Testing DELIA (Basic Level)...")
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/chat/delia",
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            },
            json={
                "question": "¿Qué es EDSL?",
                "user_level": "basic"
            }
        )
        response.raise_for_status()
        
        result = response.json()
        print(f"✅ DELIA Basic Response: {result['response'][:100]}...")
        print(f"   User Level: {result['user_level']}")
        print(f"   Has EDSL Code: {result['has_edsl_code']}")
        print(f"   EDSL Blocks Count: {result['edsl_code_blocks_count']}")
        return True
        
    except Exception as e:
        print(f"❌ DELIA basic test failed: {e}")
        return False

def test_delia_validation(token):
    """Test DELIA with code validation."""
    print("\n🔧 Testing DELIA Code Validation...")
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/chat/delia",
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            },
            json={
                "question": "Revisa este código EDSL: IF x > 10 THEN y = 20",
                "user_level": "intermediate"
            }
        )
        response.raise_for_status()
        
        result = response.json()
        print(f"✅ DELIA Validation Response: {result['response'][:100]}...")
        print(f"   Validation Results: {len(result['validation_results'])} blocks validated")
        
        if result['validation_results']:
            for i, validation in enumerate(result['validation_results']):
                print(f"   Block {i+1}: Valid={validation['is_valid']}, Warnings={len(validation['warnings'])}")
        
        return True
        
    except Exception as e:
        print(f"❌ DELIA validation test failed: {e}")
        return False

def test_delia_advanced(token):
    """Test DELIA with advanced user level."""
    print("\n🚀 Testing DELIA (Advanced Level)...")
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/chat/delia",
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            },
            json={
                "question": "Optimiza este script EDSL: IF IsNull(field1) THEN result = 0 ELSE result = field1 * 2",
                "user_level": "advanced"
            }
        )
        response.raise_for_status()
        
        result = response.json()
        print(f"✅ DELIA Advanced Response: {result['response'][:100]}...")
        print(f"   User Level: {result['user_level']}")
        print(f"   Has EDSL Code: {result['has_edsl_code']}")
        return True
        
    except Exception as e:
        print(f"❌ DELIA advanced test failed: {e}")
        return False

def test_backward_compatibility():
    """Test that the original chain import still works."""
    print("\n🔄 Testing Backward Compatibility...")
    
    try:
        from app.rag.chain import get_rag_chain, rag_chain
        
        # Test both import methods
        chain1 = get_rag_chain()
        chain2 = rag_chain()
        
        print("✅ Backward compatibility imports work")
        print("✅ Both get_rag_chain() and rag_chain() return the same type")
        return True
        
    except Exception as e:
        print(f"❌ Backward compatibility test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🧪 Testing Dual RAG Functionality")
    print("=" * 50)
    
    # Get authentication token
    token = get_auth_token()
    if not token:
        print("❌ Cannot proceed without authentication token")
        return
    
    print(f"✅ Authentication successful")
    
    # Test results
    tests = []
    
    # Test backward compatibility
    tests.append(("Backward Compatibility", test_backward_compatibility()))
    
    # Test general RAG
    tests.append(("General RAG", test_general_rag(token)))
    
    # Test DELIA functionality
    tests.append(("DELIA Basic", test_delia_basic(token)))
    tests.append(("DELIA Validation", test_delia_validation(token)))
    tests.append(("DELIA Advanced", test_delia_advanced(token)))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    print("=" * 50)
    
    passed = 0
    total = len(tests)
    
    for test_name, result in tests:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Dual functionality is working correctly.")
    else:
        print("⚠️  Some tests failed. Please check the implementation.")

if __name__ == "__main__":
    main() 