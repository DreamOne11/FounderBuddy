# Mission Pitch Sections

This directory contains the modular section implementations for the Mission Pitch Agent. Each section represents one component of the 6-part Mission Pitch framework.

## Section Overview

### 1. Hidden Theme (`hidden_theme/`)
- **Purpose**: Discover the 1-sentence recurring life pattern
- **Output**: Personal theme that connects to business mission
- **Key**: Must be authentic and personally meaningful

### 2. Personal Origin (`personal_origin/`)
- **Purpose**: Find the early memory that shaped their worldview
- **Output**: Specific childhood/formative experience
- **Key**: Must connect clearly to their hidden theme

### 3. Business Origin (`business_origin/`)
- **Purpose**: Identify the "this should be a business" moment
- **Output**: Story of recognizing market opportunity
- **Key**: Must show external validation/demand

### 4. Mission (`mission/`)
- **Purpose**: Craft clear mission statement
- **Output**: "The change we make for whom" statement
- **Key**: Must be specific and understandable

### 5. Three-Year Vision (`three_year_vision/`)
- **Purpose**: Define believable exciting milestone
- **Output**: Specific 3-year goal with metrics
- **Key**: Must be ambitious but achievable

### 6. Big Vision (`big_vision/`)
- **Purpose**: Create aspirational future vision
- **Output**: Long-term vision that passes "selfless test"
- **Key**: Must be bigger than their business

### 7. Implementation (`implementation/`)
- **Purpose**: Assemble complete 90-second pitch
- **Output**: Integrated narrative connecting all elements
- **Key**: Must be deliverable in 90 seconds

## Section Structure

Each section contains:
- `__init__.py` - Section exports
- `models.py` - Pydantic data models
- `prompts.py` - Section-specific prompts and templates
- `[section]_design_doc.md` - Detailed design documentation (where applicable)

## Integration

Sections are imported into the main agent through:
1. `sections/__init__.py` - Aggregates all section exports
2. `models.py` - Imports section data models
3. `prompts.py` - Uses section prompts in context generation
4. `tools.py` - Leverages section models for data extraction

## Development Guidelines

When modifying sections:
1. Keep section-specific logic isolated
2. Maintain consistent model/prompt structure
3. Update section `__init__.py` exports
4. Test integration with main agent
5. Update design docs for major changes
