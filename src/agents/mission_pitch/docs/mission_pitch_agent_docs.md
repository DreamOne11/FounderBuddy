# Mission Pitch Agent - Documentation

## Overview

The Mission Pitch Agent helps founders create a compelling 90-second narrative that connects their personal authenticity to their business purpose. The agent guides users through 6 core components that form a cohesive mission pitch.

## Architecture

### Modular Structure
```
mission_pitch/
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
│   ├── hidden_theme/     # Life pattern discovery
│   ├── personal_origin/  # Formative memory identification
│   ├── business_origin/  # Business opportunity moment
│   ├── mission/          # Mission statement crafting
│   ├── three_year_vision/ # 3-year milestone definition
│   ├── big_vision/       # Aspirational future vision
│   └── implementation/   # Complete pitch assembly
└── docs/                 # Documentation
```

## Mission Pitch Framework

### The 6 Components

1. **Hidden Theme** - The 1-sentence recurring pattern in their life
2. **Personal Origin** - Early memory that shaped their worldview
3. **Business Origin** - The moment they knew "this should be a business"
4. **Mission** - Clear statement of change they're making for whom
5. **3-Year Vision** - Believable, exciting milestone that energizes the team
6. **Big Vision** - Aspirational future that passes the "Selfless Test"

### Integration Flow
```
Hidden Theme → Personal Origin → Business Origin → Mission → 3-Year Vision → Big Vision → Complete Pitch
```

## Technical Implementation

### LangGraph Flow
```
Initialize → Router → Chat Agent → Memory Updater → Router
                 ↓                                    ↑
            Implementation ←←←←←←←←←←←←←←←←←←←←←←←←←←←←←┘
```

### Key Features
- **Modular sections**: Each component isolated for maintainability
- **Progressive disclosure**: One question at a time approach
- **Validation system**: Confidence ratings and completion criteria
- **Data extraction**: Structured data capture from conversations
- **Export capability**: Complete 90-second pitch generation

## Usage

### API Integration
The agent integrates with the main service through the standard agent pattern:
- Agent ID: 4 (Mission Pitch)
- Endpoint: `/mission-pitch/invoke`
- State management: Thread-based conversation tracking
- Output: Structured mission pitch components and final narrative

### Development Status
- ✅ Modular structure created
- ✅ Section definitions complete
- ⏳ Integration with main agent.py (pending)
- ⏳ Testing and validation (pending)

## Next Steps

1. Update main `agent.py` to use modular structure
2. Test section integration and data flow
3. Validate prompt effectiveness
4. Add comprehensive testing
5. Document API endpoints and usage patterns
