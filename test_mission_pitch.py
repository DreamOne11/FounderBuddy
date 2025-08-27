#!/usr/bin/env python3
"""Test script to verify mission pitch agent initialization."""

import sys
import os
sys.path.append(os.path.dirname(__file__))

try:
    # Test imports
    from src.agents.mission_pitch.tools import SECTION_PROMPTS, SECTION_TEMPLATES, get_context
    print("✅ Successfully imported SECTION_PROMPTS and SECTION_TEMPLATES")
    
    # Test template access
    hidden_theme_template = SECTION_TEMPLATES.get("hidden_theme")
    if hidden_theme_template:
        print("✅ Successfully found hidden_theme template")
        print(f"   Template name: {hidden_theme_template.name}")
    else:
        print("❌ Could not find hidden_theme template")
        print(f"   Available templates: {list(SECTION_TEMPLATES.keys())}")
    
    # Test base_rules access
    base_rules = SECTION_PROMPTS.get("base_rules", "")
    if base_rules:
        print("✅ Successfully found base_rules in SECTION_PROMPTS")
        print(f"   Base rules length: {len(base_rules)} characters")
    else:
        print("❌ Could not find base_rules in SECTION_PROMPTS")
        print(f"   Available prompts: {list(SECTION_PROMPTS.keys())}")

    print("\n✅ Mission pitch imports are working correctly!")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    
except Exception as e:
    print(f"❌ Unexpected error: {e}")
    import traceback
    traceback.print_exc()