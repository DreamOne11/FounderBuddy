"""
Simple test to verify Concept Pitch prompts match specifications
No external dependencies required
"""

import sys
from pathlib import Path

# Add src to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root / "src"))


def test_summary_confirmation():
    """Test Summary Confirmation section"""
    print("\n" + "="*70)
    print("🧪 TEST 1: Summary Confirmation Section")
    print("="*70)
    
    try:
        from agents.concept_pitch.sections.summary_confirmation.prompts import SUMMARY_CONFIRMATION_SYSTEM_PROMPT
        
        prompt = SUMMARY_CONFIRMATION_SYSTEM_PROMPT
        
        # Check for required phrases from Document 1
        checks = [
            ("Alright let's get your Concept Pitch nailed" in prompt, 
             "Opening: 'Alright let's get your Concept Pitch nailed'"),
            ("Got it." in prompt, 
             "Transition: 'Got it.'"),
            ("Does that sound accurate?" in prompt, 
             "Confirmation: 'Does that sound accurate?'"),
            ("You're building {{type of solution}} for {{ICP}}" in prompt, 
             "Summary format with placeholders"),
            ("VALUE CANVAS" in prompt.upper() or "Value Canvas" in prompt, 
             "References Value Canvas"),
        ]
        
        print("\n✅ Required Elements:")
        all_passed = True
        for check, description in checks:
            status = "✅" if check else "❌"
            print(f"   {status} {description}")
            if not check:
                all_passed = False
        
        return all_passed
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False


def test_pitch_generation():
    """Test Pitch Generation section"""
    print("\n" + "="*70)
    print("🧪 TEST 2: Pitch Generation Section")
    print("="*70)
    
    try:
        from agents.concept_pitch.sections.pitch_generation.prompts import PITCH_GENERATION_SYSTEM_PROMPT
        
        prompt = PITCH_GENERATION_SYSTEM_PROMPT
        
        # Check for 3 options
        print("\n✅ Three Pitch Options:")
        options_found = []
        for option in ['Option A', 'Option B', 'Option C']:
            found = option in prompt
            status = "✅" if found else "❌"
            print(f"   {status} {option}")
            options_found.append(found)
        
        # Check for 4-part structure
        print("\n✅ 4-Part Structure:")
        parts_checks = [
            ("4-PART STRUCTURE" in prompt, "4-PART STRUCTURE mentioned"),
            ("Part 1: The Problem Statement" in prompt, "Part 1: Problem Statement"),
            ("Part 2: The Solution Preview" in prompt, "Part 2: Solution Preview"),
            ("Part 3: The Temperature Check" in prompt, "Part 3: Temperature Check"),
            ("Part 4: The Referral Ask" in prompt, "Part 4: Referral Ask"),
        ]
        
        parts_found = []
        for check, description in parts_checks:
            status = "✅" if check else "❌"
            print(f"   {status} {description}")
            parts_found.append(check)
        
        # Check that each part appears multiple times (once per option)
        print("\n✅ Parts Repeated for Each Option:")
        part_counts = [
            (prompt.count("Part 1:"), "Part 1"),
            (prompt.count("Part 2:"), "Part 2"),
            (prompt.count("Part 3:"), "Part 3"),
            (prompt.count("Part 4:"), "Part 4"),
        ]
        
        repetition_ok = True
        for count, part_name in part_counts:
            # Should appear at least 3 times (once per option)
            status = "✅" if count >= 3 else "⚠️ "
            print(f"   {status} {part_name} appears {count} times (expected 3+)")
            if count < 3:
                repetition_ok = False
        
        return all(options_found) and all(parts_found) and repetition_ok
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_pitch_selection():
    """Test Pitch Selection section"""
    print("\n" + "="*70)
    print("🧪 TEST 3: Pitch Selection Section")
    print("="*70)
    
    try:
        from agents.concept_pitch.sections.pitch_selection.prompts import PITCH_SELECTION_SYSTEM_PROMPT
        
        prompt = PITCH_SELECTION_SYSTEM_PROMPT
        
        checks = [
            ("Which one of these feels most natural to you?" in prompt, 
             "Selection question: 'Which one of these feels most natural to you?'"),
            ("Would you like to tweak or refine" in prompt, 
             "Refinement question: 'Would you like to tweak or refine'"),
            ("Note to developer" in prompt, 
             "Developer note about saving logic"),
        ]
        
        print("\n✅ Required Elements:")
        all_passed = True
        for check, description in checks:
            status = "✅" if check else "❌"
            print(f"   {status} {description}")
            if not check:
                all_passed = False
        
        return all_passed
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False


def test_refinement():
    """Test Refinement section"""
    print("\n" + "="*70)
    print("🧪 TEST 4: Refinement Section")
    print("="*70)
    
    try:
        from agents.concept_pitch.sections.refinement.prompts import REFINEMENT_SYSTEM_PROMPT
        
        prompt = REFINEMENT_SYSTEM_PROMPT
        
        checks = [
            ("recursive questioning" in prompt or "recursive" in prompt.lower(), 
             "Recursive questioning approach"),
            ("ALL 4 parts" in prompt or "all 4 parts" in prompt, 
             "Refine all 4 parts"),
            ("Part 1" in prompt and "Part 2" in prompt and "Part 3" in prompt and "Part 4" in prompt, 
             "All 4 parts listed"),
            ("Done. Your Concept Pitch is now saved" in prompt, 
             "Final confirmation: 'Done. Your Concept Pitch is now saved'"),
            ("Concept Testing" in prompt or "Sprint Playbook" in prompt, 
             "References next steps"),
        ]
        
        print("\n✅ Required Elements:")
        all_passed = True
        for check, description in checks:
            status = "✅" if check else "❌"
            print(f"   {status} {description}")
            if not check:
                all_passed = False
        
        return all_passed
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False


def test_section_flow():
    """Test section flow"""
    print("\n" + "="*70)
    print("🧪 TEST 5: Section Flow")
    print("="*70)
    
    try:
        from agents.concept_pitch.sections import SECTION_TEMPLATES
        
        print(f"\n✅ Found {len(SECTION_TEMPLATES)} sections:")
        
        expected_sections = [
            'summary_confirmation',
            'pitch_generation',
            'pitch_selection',
            'refinement',
        ]
        
        all_found = True
        for section_id in expected_sections:
            if section_id in SECTION_TEMPLATES:
                template = SECTION_TEMPLATES[section_id]
                print(f"   ✅ {template.name} ({section_id})")
            else:
                print(f"   ❌ Missing: {section_id}")
                all_found = False
        
        return all_found
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False


def run_all_tests():
    """Run all tests"""
    print("\n" + "="*70)
    print("🚀 CONCEPT PITCH PROMPTS - STRUCTURE VERIFICATION")
    print("="*70)
    print("\nVerifying implementation matches specification documents:")
    print("  📄 Document 1: Main conversation flow")
    print("  📄 Document 2: 4-part pitch structure")
    print("="*70)
    
    results = [
        ("Summary Confirmation", test_summary_confirmation()),
        ("Pitch Generation", test_pitch_generation()),
        ("Pitch Selection", test_pitch_selection()),
        ("Refinement", test_refinement()),
        ("Section Flow", test_section_flow()),
    ]
    
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
        print("\n🎉 ALL STRUCTURE TESTS PASSED!")
        print("\n✅ The Concept Pitch prompts are correctly structured.")
        print("\n📋 Next Steps:")
        print("   1. Install dependencies: pip install -r requirements.txt")
        print("   2. Start FastAPI server: python src/run_service.py")
        print("   3. Test the endpoint: POST /concept-pitch/invoke")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please review above.")
    
    print("="*70)
    
    return passed == total


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)

