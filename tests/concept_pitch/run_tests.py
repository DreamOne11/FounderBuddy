#!/usr/bin/env python3
"""
Test Runner for Concept Pitch Agent E2E Tests

This script demonstrates how to run the Concept Pitch agent tests
and provides a simple way to execute them without pytest.
"""

import sys
import os
from pathlib import Path

# Add src to path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root / "src"))

def run_concept_pitch_tests():
    """Run the Concept Pitch agent tests"""
    print("🚀 Running Concept Pitch Agent E2E Tests")
    print("=" * 60)
    
    try:
        # Import pytest
        import pytest
        
        # Run the tests
        test_file = project_root / "tests" / "concept_pitch" / "test_concept_pitch_agent_e2e.py"
        
        print(f"📁 Test file: {test_file}")
        print(f"🔧 Running tests with pytest...")
        
        # Run pytest with verbose output
        result = pytest.main([
            str(test_file),
            "-v",
            "--tb=short",
            "--color=yes"
        ])
        
        if result == 0:
            print("\n✅ All tests passed!")
        else:
            print(f"\n❌ Tests failed with exit code: {result}")
            
        return result == 0
        
    except ImportError:
        print("❌ pytest not available. Please install it with: pip install pytest")
        return False
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return False


def run_simple_test():
    """Run a simple test without pytest to verify basic functionality"""
    print("\n🧪 Running Simple Concept Pitch Test")
    print("-" * 40)
    
    try:
        # Test basic imports
        from agents.concept_pitch.agent import AgentState, run_concept_pitch_agent
        from agents.concept_pitch.sync import save_pitch_to_project
        from agents.concept_pitch.refine import refine_pitch
        
        print("✅ All imports successful")
        
        # Test AgentState creation
        test_state = AgentState(
            icp="test founders",
            pain="test pain",
            gain="test gain",
            prize="test prize",
            signature_method="test method"
        )
        
        assert test_state.icp == "test founders"
        print("✅ AgentState creation successful")
        
        # Test sync functionality (with mocked directory)
        import tempfile
        with tempfile.TemporaryDirectory() as temp_dir:
            from unittest.mock import patch
            
            with patch('agents.concept_pitch.sync.get_save_directory') as mock_get_dir:
                mock_get_dir.return_value = Path(temp_dir)
                
                test_data = {
                    "pain_pitch": "Test pain pitch",
                    "gain_pitch": "Test gain pitch",
                    "prize_pitch": "Test prize pitch"
                }
                
                save_result = save_pitch_to_project(
                    project_id="simple_test",
                    concept_pitch_data=test_data
                )
                
                assert save_result["success"] is True
                print("✅ Sync functionality successful")
        
        print("\n🎉 Simple test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Simple test failed: {e}")
        return False


if __name__ == "__main__":
    print("Concept Pitch Agent Test Runner")
    print("=" * 60)
    
    # Check if pytest is available
    try:
        import pytest
        print("✅ pytest is available")
        
        # Ask user which test to run
        print("\nChoose test mode:")
        print("1. Run full E2E tests with pytest")
        print("2. Run simple functionality test")
        print("3. Run both")
        
        choice = input("\nEnter choice (1-3): ").strip()
        
        if choice == "1":
            success = run_concept_pitch_tests()
        elif choice == "2":
            success = run_simple_test()
        elif choice == "3":
            print("\n" + "="*60)
            success1 = run_concept_pitch_tests()
            print("\n" + "="*60)
            success2 = run_simple_test()
            success = success1 and success2
        else:
            print("Invalid choice. Running simple test...")
            success = run_simple_test()
        
        if success:
            print("\n🎯 All tests completed successfully!")
            sys.exit(0)
        else:
            print("\n💥 Some tests failed!")
            sys.exit(1)
            
    except ImportError:
        print("⚠️ pytest not available. Running simple test only...")
        success = run_simple_test()
        
        if success:
            print("\n🎯 Simple test completed successfully!")
            print("💡 Install pytest for full test suite: pip install pytest")
            sys.exit(0)
        else:
            print("\n💥 Simple test failed!")
            sys.exit(1)
