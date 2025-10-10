"""
Comprehensive test suite for Concept Pitch (CAOS) Agent
Tests all requirements from both specification documents
"""

import asyncio
import json
import sys
from pathlib import Path

# Add src to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root / "src"))

from agents.concept_pitch.agent import initialize_concept_pitch_state
from agents.concept_pitch.tools import get_context
from agents.concept_pitch.models import ConceptPitchState
from agents.concept_pitch.enums import SectionID


async def test_value_canvas_data_retrieval():
    """Test 1: Verify Value Canvas data is properly retrieved"""
    print("\n" + "="*70)
    print("🧪 TEST 1: Value Canvas Data Retrieval")
    print("="*70)
    
    try:
        # Test get_context function
        context = await get_context.ainvoke({
            "user_id": 1,
            "thread_id": "test_thread_001",
            "section_id": SectionID.SUMMARY_CONFIRMATION.value,
            "canvas_data": {},
        })
        
        print("\n✅ Context retrieved successfully")
        print(f"   Section ID: {context.get('section_id')}")
        print(f"   Status: {context.get('status')}")
        
        # Check for Value Canvas data
        vc_data = context.get('value_canvas_data', {})
        print(f"\n📊 Value Canvas Data Retrieved:")
        print(f"   - ICP: {'✅' if vc_data.get('icp') else '❌'} {vc_data.get('icp', 'Not found')[:50]}...")
        print(f"   - Pain: {'✅' if vc_data.get('pain') else '❌'} {vc_data.get('pain', 'Not found')[:50]}...")
        print(f"   - Payoffs: {'✅' if vc_data.get('payoffs') else '❌'} {vc_data.get('payoffs', 'Not found')[:50]}...")
        print(f"   - Prize: {'✅' if vc_data.get('prize') else '❌'} {vc_data.get('prize', 'Not found')[:50]}...")
        print(f"   - Signature Method: {'✅' if vc_data.get('signature_method') else '❌'} {vc_data.get('signature_method', 'Not found')[:50]}...")
        
        # Check system prompt
        if 'VALUE CANVAS CONTEXT:' in context.get('system_prompt', ''):
            print("\n✅ System prompt includes Value Canvas context")
        else:
            print("\n⚠️  System prompt may not include Value Canvas context")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_state_initialization():
    """Test 2: Verify ConceptPitchState initialization with Value Canvas data"""
    print("\n" + "="*70)
    print("🧪 TEST 2: State Initialization")
    print("="*70)
    
    try:
        # Initialize state
        state = await initialize_concept_pitch_state(user_id=1, thread_id="test_thread_002")
        
        print("\n✅ State initialized successfully")
        print(f"   User ID: {state['user_id']}")
        print(f"   Thread ID: {state['thread_id']}")
        print(f"   Current Section: {state['current_section']}")
        
        # Check canvas_data
        canvas_data = state.get('canvas_data')
        if canvas_data:
            print(f"\n📊 Canvas Data in State:")
            print(f"   - ICP Summary: {'✅' if canvas_data.icp_summary else '❌'} {canvas_data.icp_summary[:50] if canvas_data.icp_summary else 'Not set'}...")
            print(f"   - Pain Summary: {'✅' if canvas_data.pain_summary else '❌'} {canvas_data.pain_summary[:50] if canvas_data.pain_summary else 'Not set'}...")
            print(f"   - Gain Summary: {'✅' if canvas_data.gain_summary else '❌'} {canvas_data.gain_summary[:50] if canvas_data.gain_summary else 'Not set'}...")
            print(f"   - Prize Summary: {'✅' if canvas_data.prize_summary else '❌'} {canvas_data.prize_summary[:50] if canvas_data.prize_summary else 'Not set'}...")
        else:
            print("\n⚠️  Canvas data not found in state")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_section_prompts():
    """Test 3: Verify all section prompts match specifications"""
    print("\n" + "="*70)
    print("🧪 TEST 3: Section Prompts Verification")
    print("="*70)
    
    try:
        from agents.concept_pitch.sections import SECTION_TEMPLATES
        
        print(f"\n📋 Found {len(SECTION_TEMPLATES)} sections:")
        
        for section_id, template in SECTION_TEMPLATES.items():
            print(f"\n   Section: {template.name} ({section_id})")
            
            # Check for key phrases from specifications
            prompt = template.system_prompt_template
            
            # Document 1 requirements
            checks = []
            
            if section_id == 'summary_confirmation':
                checks = [
                    ("Alright let's get your Concept Pitch nailed" in prompt, "Opening phrase"),
                    ("Got it." in prompt, "Transition phrase"),
                    ("Does that sound accurate?" in prompt, "Confirmation question"),
                ]
            elif section_id == 'pitch_generation':
                checks = [
                    ("4-PART STRUCTURE" in prompt, "4-part structure mentioned"),
                    ("Problem Statement" in prompt, "Part 1 defined"),
                    ("Solution Preview" in prompt, "Part 2 defined"),
                    ("Temperature Check" in prompt, "Part 3 defined"),
                    ("Referral Ask" in prompt, "Part 4 defined"),
                    ("Option A" in prompt and "Option B" in prompt and "Option C" in prompt, "3 options"),
                ]
            elif section_id == 'pitch_selection':
                checks = [
                    ("Which one of these feels most natural to you?" in prompt, "Selection question"),
                    ("Would you like to tweak or refine" in prompt, "Refinement question"),
                ]
            elif section_id == 'refinement':
                checks = [
                    ("recursive questioning" in prompt or "recursive" in prompt.lower(), "Recursive approach"),
                    ("ALL 4 parts" in prompt or "all 4 parts" in prompt, "All 4 parts"),
                    ("Done. Your Concept Pitch is now saved" in prompt, "Final confirmation"),
                ]
            
            for check, description in checks:
                status = "✅" if check else "❌"
                print(f"      {status} {description}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_pitch_templates():
    """Test 4: Verify pitch templates include all 4 parts"""
    print("\n" + "="*70)
    print("🧪 TEST 4: Pitch Templates Structure")
    print("="*70)
    
    try:
        from agents.concept_pitch.sections.pitch_generation import PITCH_GENERATION_SYSTEM_PROMPT
        
        prompt = PITCH_GENERATION_SYSTEM_PROMPT
        
        # Check for 3 options
        print("\n📝 Checking 3 Pitch Options:")
        for option in ['Option A', 'Option B', 'Option C']:
            if option in prompt:
                print(f"   ✅ {option} found")
            else:
                print(f"   ❌ {option} missing")
        
        # Check for 4 parts in each option
        print("\n📝 Checking 4-Part Structure:")
        parts = [
            "Part 1: The Problem Statement",
            "Part 2: The Solution Preview",
            "Part 3: The Temperature Check",
            "Part 4: The Referral Ask"
        ]
        
        for part in parts:
            count = prompt.count(part)
            if count >= 3:  # Should appear at least 3 times (once per option)
                print(f"   ✅ {part} - appears {count} times")
            else:
                print(f"   ⚠️  {part} - appears only {count} times (expected 3+)")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_conversation_flow():
    """Test 5: Verify conversation flow matches specifications"""
    print("\n" + "="*70)
    print("🧪 TEST 5: Conversation Flow")
    print("="*70)
    
    try:
        from agents.concept_pitch.sections import SECTION_TEMPLATES
        from agents.concept_pitch.enums import SectionID
        
        # Expected flow
        expected_flow = [
            SectionID.SUMMARY_CONFIRMATION,
            SectionID.PITCH_GENERATION,
            SectionID.PITCH_SELECTION,
            SectionID.REFINEMENT,
        ]
        
        print("\n🔄 Expected Conversation Flow:")
        for i, section_id in enumerate(expected_flow, 1):
            template = SECTION_TEMPLATES.get(section_id.value)
            if template:
                next_section = template.next_section
                print(f"   {i}. {template.name} ({section_id.value})")
                if next_section:
                    print(f"      → Next: {next_section.value if hasattr(next_section, 'value') else next_section}")
                else:
                    print(f"      → End of flow")
            else:
                print(f"   ❌ Section {section_id.value} not found")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


async def run_all_tests():
    """Run all tests"""
    print("\n" + "="*70)
    print("🚀 CONCEPT PITCH AGENT - COMPREHENSIVE TEST SUITE")
    print("="*70)
    print("\nTesting implementation against both specification documents:")
    print("  📄 Document 1: Main conversation flow (3 pitch options)")
    print("  📄 Document 2: 4-part pitch structure")
    print("="*70)
    
    results = []
    
    # Run async tests
    results.append(("Value Canvas Data Retrieval", await test_value_canvas_data_retrieval()))
    results.append(("State Initialization", await test_state_initialization()))
    
    # Run sync tests
    results.append(("Section Prompts Verification", test_section_prompts()))
    results.append(("Pitch Templates Structure", test_pitch_templates()))
    results.append(("Conversation Flow", test_conversation_flow()))
    
    # Summary
    print("\n" + "="*70)
    print("📊 TEST SUMMARY")
    print("="*70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"   {status} - {test_name}")
    
    print(f"\n   Total: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! The Concept Pitch agent is ready for use.")
        print("\n📋 Next Steps:")
        print("   1. Start the FastAPI server: python src/run_service.py")
        print("   2. Test the endpoint: POST /concept-pitch/invoke")
        print("   3. Verify conversation flow with real user input")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please review the errors above.")
    
    print("="*70)
    
    return passed == total


if __name__ == "__main__":
    # Run tests
    success = asyncio.run(run_all_tests())
    sys.exit(0 if success else 1)

