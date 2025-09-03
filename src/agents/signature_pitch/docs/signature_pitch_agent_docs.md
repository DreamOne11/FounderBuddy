# Signature Pitch Agent - Documentation

## Overview

The Signature Pitch Agent helps founders and professionals create a compelling 90-second magnetic pitch that captures attention, builds credibility, and creates desire. The agent guides users through 6 core components that form a cohesive signature pitch.

## Architecture

### Modular Structure
```
signature_pitch/
├── agent.py              # Main agent entry point (will be updated to use modular structure)
├── models.py             # Core state and data models
├── prompts.py            # Base prompts and templates  
├── tools.py              # Integration tools and utilities
├── nodes/                # Individual graph nodes
│   ├── initialize.py     # State initialization
│   ├── router.py         # Navigation and context loading
│   ├── chat_agent.py     # Conversation generation
│   ├── memory_updater.py # State persistence and data extraction
│   └── implementation.py # Final pitch assembly
├── graph/                # Graph construction
│   ├── builder.py        # Graph assembly
│   └── routes.py         # Routing logic
├── sections/             # Section-specific implementations
│   ├── active_change/    # Transformation definition
│   ├── specific_who/     # Target audience identification
│   ├── outcome_prize/    # Desired result definition
│   ├── core_credibility/ # Proof establishment
│   ├── story_spark/      # Narrative hook creation
│   ├── signature_line/   # Complete pitch assembly
│   └── implementation/   # Final integration
└── docs/                 # Documentation
```

## Signature Pitch Framework

### The 6 Components

1. **Active Change** - The transformation you create in the world
2. **Specific Who** - The exact audience you serve
3. **Outcome/Prize** - The compelling result they desire
4. **Core Credibility** - Proof you can deliver
5. **Story Spark** - A short narrative hook or example
6. **Signature Line** - The concise pitch (90 seconds → 1 line)

### Magnetic Framework
```
Active Change → Specific Who → Outcome/Prize → Core Credibility → Story Spark → Signature Line → Complete Pitch
```

The framework creates a **magnetic pull** between current frustrated state and desired future, positioning the user as the obvious guide.

## Technical Implementation

### LangGraph Flow
```
Initialize → Router → Chat Agent → Memory Updater → Router
                 ↓                                    ↑
            Implementation ←←←←←←←←←←←←←←←←←←←←←←←←←←←←←┘
```

### Key Features
- **Modular sections**: Each component isolated for maintainability
- **Magnetic psychology**: Focus on creating desire, not just solving problems
- **Progressive disclosure**: One element at a time approach
- **Validation system**: Confidence ratings and completion criteria
- **Data extraction**: Structured data capture from conversations
- **Export capability**: Complete 90-second pitch generation

## Usage

### API Integration
The agent integrates with the main service through the standard agent pattern:
- Agent ID: 5 (Signature Pitch)
- Endpoint: `/signature-pitch/invoke`
- State management: Thread-based conversation tracking
- Output: Structured signature pitch components and final magnetic pitch

### Development Status
- ✅ Modular structure created
- ✅ Section definitions complete
- ⏳ Integration with main agent.py (pending)
- ⏳ Testing and validation (pending)

## Signature Pitch Philosophy

### Unlike Generic Elevator Pitches
- **Rooted in psychology**: Creates magnetic attraction
- **Storytelling-based**: Uses narrative to build connection
- **Positioning-focused**: Establishes unique market position
- **Desire-creating**: Makes prospects think "I need this"

### The Magnetic Pull
- **Current State**: Frustrated, struggling with specific challenge
- **Desired State**: Compelling outcome they actively want
- **Guide**: You as the obvious solution provider
- **Transformation**: Clear path from current to desired state

## Next Steps

1. Update main `agent.py` to use modular structure
2. Test section integration and data flow
3. Validate pitch effectiveness and magnetic appeal
4. Add comprehensive testing
5. Document API endpoints and usage patterns

## Framework Success Metrics

A successful Signature Pitch should:
- ✅ **Capture attention** immediately
- ✅ **Build credibility** quickly
- ✅ **Create desire** for the transformation
- ✅ **Position as obvious guide**
- ✅ **Prompt next step** naturally
