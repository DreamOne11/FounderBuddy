"""
Standalone verification script - reads prompt files directly
No imports from agents module required
"""

from pathlib import Path


def read_prompt_file(filepath):
    """Read a prompt file and return its content"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"   ❌ Error reading {filepath}: {e}")
        return None


def test_summary_confirmation():
    """Test Summary Confirmation prompts"""
    print("\n" + "="*70)
    print("🧪 TEST 1: Summary Confirmation Section")
    print("="*70)
    
    filepath = Path(__file__).parent.parent.parent / "src/agents/concept_pitch/sections/summary_confirmation/prompts.py"
    content = read_prompt_file(filepath)
    
    if not content:
        return False
    
    checks = [
        ("Alright let's get your Concept Pitch nailed" in content, 
         "Opening phrase from Document 1"),
        ("Got it." in content, 
         "Transition phrase"),
        ("Does that sound accurate?" in content, 
         "Confirmation question"),
        ("{{type of solution}}" in content or "type of solution" in content, 
         "Summary template format"),
    ]
    
    print("\n✅ Required Elements:")
    all_passed = True
    for check, description in checks:
        status = "✅" if check else "❌"
        print(f"   {status} {description}")
        if not check:
            all_passed = False
    
    return all_passed


def test_pitch_generation():
    """Test Pitch Generation prompts"""
    print("\n" + "="*70)
    print("🧪 TEST 2: Pitch Generation Section")
    print("="*70)
    
    filepath = Path(__file__).parent.parent.parent / "src/agents/concept_pitch/sections/pitch_generation/prompts.py"
    content = read_prompt_file(filepath)
    
    if not content:
        return False
    
    # Check for 3 options
    print("\n✅ Three Pitch Options:")
    options = ['Option A', 'Option B', 'Option C']
    options_found = []
    for option in options:
        found = option in content
        status = "✅" if found else "❌"
        print(f"   {status} {option}")
        options_found.append(found)
    
    # Check for 4-part structure
    print("\n✅ 4-Part Structure:")
    parts = [
        ("4-PART STRUCTURE" in content, "4-PART STRUCTURE mentioned"),
        ("Part 1: The Problem Statement" in content, "Part 1: Problem Statement"),
        ("Part 2: The Solution Preview" in content, "Part 2: Solution Preview"),
        ("Part 3: The Temperature Check" in content, "Part 3: Temperature Check"),
        ("Part 4: The Referral Ask" in content, "Part 4: Referral Ask"),
    ]
    
    parts_found = []
    for check, description in parts:
        status = "✅" if check else "❌"
        print(f"   {status} {description}")
        parts_found.append(check)
    
    # Count occurrences
    print("\n✅ Parts Repeated for Each Option:")
    part_counts = [
        (content.count("Part 1:"), "Part 1"),
        (content.count("Part 2:"), "Part 2"),
        (content.count("Part 3:"), "Part 3"),
        (content.count("Part 4:"), "Part 4"),
    ]
    
    repetition_ok = True
    for count, part_name in part_counts:
        status = "✅" if count >= 3 else "⚠️ "
        print(f"   {status} {part_name} appears {count} times (expected 3+)")
        if count < 3:
            repetition_ok = False
    
    return all(options_found) and all(parts_found) and repetition_ok


def test_pitch_selection():
    """Test Pitch Selection prompts"""
    print("\n" + "="*70)
    print("🧪 TEST 3: Pitch Selection Section")
    print("="*70)
    
    filepath = Path(__file__).parent.parent.parent / "src/agents/concept_pitch/sections/pitch_selection/prompts.py"
    content = read_prompt_file(filepath)
    
    if not content:
        return False
    
    checks = [
        ("Which one of these feels most natural to you?" in content, 
         "Selection question from Document 1"),
        ("Would you like to tweak or refine" in content, 
         "Refinement question"),
        ("Note to developer" in content, 
         "Developer note about save logic"),
    ]
    
    print("\n✅ Required Elements:")
    all_passed = True
    for check, description in checks:
        status = "✅" if check else "❌"
        print(f"   {status} {description}")
        if not check:
            all_passed = False
    
    return all_passed


def test_refinement():
    """Test Refinement prompts"""
    print("\n" + "="*70)
    print("🧪 TEST 4: Refinement Section")
    print("="*70)
    
    filepath = Path(__file__).parent.parent.parent / "src/agents/concept_pitch/sections/refinement/prompts.py"
    content = read_prompt_file(filepath)
    
    if not content:
        return False
    
    checks = [
        ("recursive questioning" in content.lower(), 
         "Recursive questioning approach"),
        ("ALL 4 parts" in content or "all 4 parts" in content, 
         "Refine all 4 parts"),
        ("Done. Your Concept Pitch is now saved" in content, 
         "Final confirmation from Document 1"),
        ("Concept Testing" in content or "Sprint Playbook" in content, 
         "References next steps from Document 2"),
    ]
    
    print("\n✅ Required Elements:")
    all_passed = True
    for check, description in checks:
        status = "✅" if check else "❌"
        print(f"   {status} {description}")
        if not check:
            all_passed = False
    
    return all_passed


def test_tools_integration():
    """Test tools.py for Value Canvas integration"""
    print("\n" + "="*70)
    print("🧪 TEST 5: Value Canvas Integration (tools.py)")
    print("="*70)
    
    filepath = Path(__file__).parent.parent.parent / "src/agents/concept_pitch/tools.py"
    content = read_prompt_file(filepath)
    
    if not content:
        return False
    
    checks = [
        ("DentAppClient" in content or "get_dentapp_client" in content, 
         "DentApp client integration"),
        ("VALUE_CANVAS_AGENT_ID" in content, 
         "Value Canvas agent ID"),
        ("get_section_state" in content, 
         "Fetches section state from API"),
        ("value_canvas_data" in content, 
         "Returns Value Canvas data"),
        ("icp" in content and "pain" in content and "payoffs" in content, 
         "Fetches ICP, Pain, Payoffs"),
    ]
    
    print("\n✅ Required Elements:")
    all_passed = True
    for check, description in checks:
        status = "✅" if check else "❌"
        print(f"   {status} {description}")
        if not check:
            all_passed = False
    
    return all_passed


def run_all_tests():
    """Run all verification tests"""
    print("\n" + "="*70)
    print("🚀 CONCEPT PITCH - SPECIFICATION VERIFICATION")
    print("="*70)
    print("\nVerifying implementation matches both documents:")
    print("  📄 Document 1: Main conversation flow (3 options)")
    print("  📄 Document 2: 4-part pitch structure")
    print("="*70)
    
    results = [
        ("Summary Confirmation", test_summary_confirmation()),
        ("Pitch Generation", test_pitch_generation()),
        ("Pitch Selection", test_pitch_selection()),
        ("Refinement", test_refinement()),
        ("Value Canvas Integration", test_tools_integration()),
    ]
    
    # Summary
    print("\n" + "="*70)
    print("📊 VERIFICATION SUMMARY")
    print("="*70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"   {status} - {test_name}")
    
    print(f"\n   Total: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 ALL VERIFICATION TESTS PASSED!")
        print("\n✅ Implementation matches both specification documents:")
        print("   • Document 1: Conversation flow ✅")
        print("   • Document 2: 4-part structure ✅")
        print("\n📋 Ready for Testing:")
        print("   1. Install dependencies if needed")
        print("   2. Start FastAPI: python src/run_service.py")
        print("   3. Test endpoint: POST /concept-pitch/invoke")
        print("   4. Verify conversation flow with real inputs")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed.")
        print("   Please review the errors above.")
    
    print("="*70)
    
    return passed == total


if __name__ == "__main__":
    import sys
    success = run_all_tests()
    sys.exit(0 if success else 1)

