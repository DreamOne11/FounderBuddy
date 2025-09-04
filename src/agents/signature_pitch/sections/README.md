# Signature Pitch Sections

This directory contains the modular section implementations for the Signature Pitch Agent. Each section represents one component of the 6-part Signature Pitch framework.

## Section Overview

### 1. Active Change (`active_change/`)
- **Purpose**: Define the transformation you create in the world
- **Output**: Specific change or transformation statement
- **Key**: Must be observable and meaningful, not just a service

### 2. Specific Who (`specific_who/`)
- **Purpose**: Identify the exact audience you serve
- **Output**: Precise target audience description
- **Key**: Must be specific enough to be actionable - "everyone" attracts no one

### 3. Outcome/Prize (`outcome_prize/`)
- **Purpose**: Define the compelling result they desire
- **Output**: Specific desirable outcome clients want
- **Key**: Must be magnetic - something they actively want, not just problem-solving

### 4. Core Credibility (`core_credibility/`)
- **Purpose**: Establish proof you can deliver the transformation
- **Output**: Compelling evidence and specific results
- **Key**: Must be relevant to the specific transformation, not generic credentials

### 5. Story Spark (`story_spark/`)
- **Purpose**: Create a short narrative hook that demonstrates transformation
- **Output**: Brief, compelling story showing transformation in action
- **Key**: Must be real example that target audience can relate to

### 6. Signature Line (`signature_line/`)
- **Purpose**: Craft the concise pitch that ties everything together
- **Output**: One-line signature and 90-second complete pitch
- **Key**: Must be both compelling and comfortable to deliver

### 7. Implementation (`implementation/`)
- **Purpose**: Assemble complete magnetic signature pitch
- **Output**: Integrated 90-second pitch with all elements
- **Key**: Must create desire to learn more, not just inform

## Section Structure

Each section contains:
- `__init__.py` - Section exports
- `models.py` - Pydantic data models
- `prompts.py` - Section-specific prompts and templates

## Integration

Sections are imported into the main agent through:
1. `sections/__init__.py` - Aggregates all section exports
2. `models.py` - Imports section data models
3. `nodes/memory_updater.py` - Uses section models for data extraction
4. `tools.py` - Leverages section models for structured data capture

## Framework Philosophy

The Signature Pitch creates a **magnetic pull** between:
- **Current frustrated state** (what they're experiencing now)
- **Desired future state** (the outcome/prize they want)

With you positioned as the **obvious guide** who provides the transformation.

## Development Guidelines

When modifying sections:
1. Keep section-specific logic isolated
2. Maintain consistent model/prompt structure
3. Update section `__init__.py` exports
4. Test integration with main agent
5. Ensure prompts create magnetic attraction, not just information transfer
