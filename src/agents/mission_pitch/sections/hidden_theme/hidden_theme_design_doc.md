# Hidden Theme Section - Design Document

## Overview

The Hidden Theme is the foundational element of the Mission Pitch framework. It represents the 1-sentence recurring pattern that has shaped the founder's entire life and directly connects to their business mission.

## Purpose

- **Foundation Building**: Establishes the personal authenticity that makes the mission compelling
- **Pattern Recognition**: Helps founders see the through-line in their life experiences
- **Mission Connection**: Creates the bridge between personal story and business purpose

## Section Flow

### 1. Pattern Discovery
- Start with broad life reflection
- Look for recurring behaviors, reactions, or roles
- Identify moments when they felt most "themselves"

### 2. Theme Distillation
- Convert patterns into a single powerful sentence
- Test for emotional resonance and authenticity
- Ensure it's personal, not generic business language

### 3. Confidence Validation
- User rates their connection to the theme (0-5)
- Must achieve 3+ for section completion
- Refine until it feels genuinely true

## Data Extraction

### Required Fields
- `theme_rant`: Raw exploration of life patterns (conversational)
- `theme_1sentence`: Distilled theme statement (structured)
- `theme_confidence`: User confidence rating (0-5)

### Validation Rules
- Theme must be personally authentic, not corporate speak
- Single sentence format for memorability
- Confidence rating 3+ required for completion

## Integration Points

### Feeds Into:
- Personal Origin (provides context for early memory selection)
- Business Origin (connects pattern to business moment)
- Mission Statement (theme becomes mission foundation)

### Dependencies:
- None (first section in sequence)

## Success Metrics

- User achieves 3+ confidence rating
- Theme statement is personal and authentic
- Clear connection established between life pattern and business purpose

## Common Challenges

1. **Generic Themes**: Users default to business buzzwords
2. **Multiple Themes**: Difficulty choosing single most important pattern
3. **Vulnerability**: Hesitation to share personal insights

## Conversation Examples

### Good Theme Discovery:
- "I've always been the translator - helping technical people explain things to normal humans"
- "I see the one thing everyone else is missing in every situation"
- "I naturally make complicated things simple"

### Avoid Generic Themes:
- "I'm passionate about helping people"
- "I want to make a difference in the world"
- "I believe in innovation and excellence"
