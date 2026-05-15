"""
Test Runner - Run all tests at once
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from test_unit import run_all_tests as run_unit_tests
from test_integration import run_integration_tests


def run_all_tests():
    print("\n" + "=" * 70)
    print(" MEDICARE HOSPITAL MANAGEMENT SYSTEM - COMPLETE TEST SUITE")
    print("=" * 70)
    
    print("\n" + "=" * 70)
    print(" PART 1: UNIT TESTS")
    print("=" * 70)
    unit_success = run_unit_tests()
    
    print("\n" + "=" * 70)
    print(" PART 2: INTEGRATION TESTS")
    print("=" * 70)
    integration_success = run_integration_tests()
    
    print("\n" + "=" * 70)
    print(" FINAL TEST SUMMARY")
    print("=" * 70)
    print(f"Unit Tests:        {'✅ PASSED' if unit_success else '❌ FAILED'}")
    print(f"Integration Tests: {'✅ PASSED' if integration_success else '❌ FAILED'}")
    
    if unit_success and integration_success:
        print("\n🎉 ALL TESTS PASSED! 🎉")
        return True
    else:
        print("\n❌ SOME TESTS FAILED!")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)