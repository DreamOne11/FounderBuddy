# Python Backend Testing - Recursion Loop Detection Guide

This document provides comprehensive guidance for creating Python tests to detect and handle recursion loops in the LangGraph Value Canvas agent backend.

## Executive Summary

The Dent-Value-Canvas-Chat-Agent backend (LangGraph) currently experiences recursion loops where the agent gets stuck asking the same question repeatedly. This document outlines Python testing strategies specifically designed to:

1. Detect conversation recursion loops in the backend agent logic
2. Validate proper conversation flow progression
3. Test conversation state management and section transitions
4. Implement timeout and recovery mechanisms for stuck conversations

## Current Problem Analysis

### Recursion Loop Issue
The agent runs into recursion loops where it repeats the same question instead of progressing through the Value Canvas flow:

**Expected Flow:**
```
Interview → ICP → Pain → Deep Fear → Payoffs → Signature Method → Mistakes → Prize
```

**Actual Problem:**
```
Interview → Interview → Interview → [STUCK]
```

### Frontend vs Backend Testing Context

**Frontend Testing (Cypress) - Current Status:**
- Tests UI interactions and streaming responses
- Cannot detect backend agent logic issues
- Limited to validating frontend behavior and API response handling

**Backend Testing (Python) - This Guide's Focus:**
- Tests actual LangGraph agent logic
- Detects conversation state management issues
- Validates conversation flow progression
- Tests timeout and recovery mechanisms

## Python Testing Framework Architecture

### Test Structure Overview

```python
# Test Categories for Backend Recursion Detection

1. Conversation Loop Detection Tests
   - Duplicate message detection
   - Response similarity analysis
   - Question repetition identification

2. Flow Progression Validation Tests  
   - Section transition verification
   - State progression tracking
   - Conversation milestone validation

3. State Management Tests
   - Context retention verification
   - Memory persistence validation
   - Thread state consistency

4. Timeout and Recovery Tests
   - Stuck conversation detection
   - Automatic recovery mechanisms
   - Error handling and fallbacks
```

### Core Testing Components

#### 1. Conversation Loop Detection Algorithm

```python
class ConversationLoopDetector:
    """
    Detects when agent gets stuck in repetitive conversation patterns
    """
    
    def __init__(self, similarity_threshold=0.8, max_repeats=3):
        self.similarity_threshold = similarity_threshold
        self.max_repeats = max_repeats
        self.message_history = []
        
    def detect_loop(self, new_response):
        """
        Analyzes if new response indicates a conversation loop
        Returns: (is_loop, loop_details)
        """
        # Implementation details in test examples below
        pass
        
    def calculate_similarity(self, text1, text2):
        """
        Calculate semantic similarity between responses
        """
        pass
```

#### 2. Flow Progression Validator

```python
class ValueCanvasFlowValidator:
    """
    Validates proper progression through Value Canvas sections
    """
    
    EXPECTED_FLOW = [
        "interview", "icp", "pain", "deep_fear", 
        "payoffs", "signature_method", "mistakes", "prize"
    ]
    
    def validate_progression(self, conversation_history):
        """
        Validates conversation follows expected flow progression
        """
        pass
        
    def detect_section_stuck(self, current_section, message_count):
        """
        Detects if agent is stuck in one section too long
        """
        pass
```

## Detailed Test Implementation Examples

### Test 1: Basic Recursion Loop Detection

```python
import pytest
import asyncio
from unittest.mock import Mock, patch
from datetime import datetime, timedelta

class TestRecursionLoopDetection:
    
    @pytest.fixture
    def agent_client(self):
        """Mock or actual agent client for testing"""
        # Setup your agent client here
        pass
    
    @pytest.mark.asyncio
    async def test_detect_question_repetition_loop(self, agent_client):
        """
        Test Case: Detect when agent repeats the same question 3+ times
        
        Scenario: Agent gets stuck asking "What's your name?" repeatedly
        Expected: Test should identify this as a recursion loop
        """
        
        conversation_messages = [
            "Hello, I want to create my value canvas",
            "What's your name?",  # Agent response 1
            "My name is John",
            "What's your name?",  # Agent response 2 - DUPLICATE
            "I already told you, it's John",
            "What's your name?",  # Agent response 3 - RECURSION DETECTED
        ]
        
        loop_detector = ConversationLoopDetector(
            similarity_threshold=0.9,
            max_repeats=2
        )
        
        agent_responses = []
        
        for i in range(0, len(conversation_messages), 2):
            user_msg = conversation_messages[i]
            
            if i + 1 < len(conversation_messages):
                expected_agent_response = conversation_messages[i + 1]
                
                # Simulate agent response
                actual_response = await agent_client.send_message(user_msg)
                agent_responses.append(actual_response)
                
                # Check for recursion loop
                is_loop, loop_details = loop_detector.detect_loop(actual_response)
                
                if is_loop:
                    pytest.fail(f"Recursion loop detected: {loop_details}")
        
        # Validate no recursion occurred
        assert not any(loop_detector.detect_loop(response)[0] for response in agent_responses)
    
    @pytest.mark.asyncio
    async def test_semantic_similarity_loop_detection(self, agent_client):
        """
        Test Case: Detect semantically similar repeated questions
        
        Scenario: Agent asks variations of the same question
        - "What's your company name?"
        - "Could you tell me your company's name?"
        - "What is the name of your company?"
        """
        
        similar_questions = [
            "What's your company name?",
            "Could you tell me your company's name?", 
            "What is the name of your company?",
            "Can you share your company name with me?"
        ]
        
        loop_detector = ConversationLoopDetector(
            similarity_threshold=0.7,  # Lower threshold for semantic similarity
            max_repeats=2
        )
        
        conversation = [
            ("Hello", "What's your company name?"),
            ("Acme Corp", "Could you tell me your company's name?"),  # Should detect similarity
        ]
        
        for user_msg, expected_question_type in conversation:
            response = await agent_client.send_message(user_msg)
            
            is_loop, details = loop_detector.detect_loop(response)
            
            # For this test, we expect to detect the semantic loop
            if "company" in user_msg.lower() and is_loop:
                assert details["loop_type"] == "semantic_similarity"
                assert details["similarity_score"] > 0.7
```

### Test 2: Flow Progression Validation

```python
class TestFlowProgression:
    
    @pytest.mark.asyncio
    async def test_proper_section_progression(self, agent_client):
        """
        Test Case: Validate agent progresses through sections correctly
        
        Expected Flow: Interview → ICP → Pain → Deep Fear → etc.
        """
        
        flow_validator = ValueCanvasFlowValidator()
        conversation_log = []
        
        # Simulate complete value canvas conversation
        test_conversation = [
            # Interview Section
            ("Hello, I want to create my value canvas", "interview"),
            ("My name is Sarah", "interview"),
            ("My company is TechCorp", "interview"),
            ("4", "interview_rating"),  # Rating should trigger section transition
            
            # ICP Section  
            ("Ready for ICP", "icp"),
            ("My ideal client is a CTO", "icp"),
            ("5", "icp_rating"),  # Should transition to Pain
            
            # Pain Section
            ("Ready for pain points", "pain"),
            ("High costs are painful", "pain"),
            ("4", "pain_rating"),  # Should transition to Deep Fear
        ]
        
        current_section = None
        section_message_count = 0
        
        for user_message, expected_section in test_conversation:
            response = await agent_client.send_message(user_message)
            
            # Analyze response to determine current section
            detected_section = flow_validator.detect_current_section(response)
            conversation_log.append({
                "user_message": user_message,
                "agent_response": response,
                "expected_section": expected_section,
                "detected_section": detected_section,
                "timestamp": datetime.now()
            })
            
            # Validate section progression
            if detected_section != current_section:
                # Section changed - validate it's correct progression
                progression_valid = flow_validator.validate_section_transition(
                    current_section, detected_section
                )
                
                if not progression_valid:
                    pytest.fail(f"Invalid section progression: {current_section} → {detected_section}")
                
                current_section = detected_section
                section_message_count = 1
            else:
                section_message_count += 1
                
                # Check if stuck in section too long
                if section_message_count > 10:  # Max messages per section
                    pytest.fail(f"Agent stuck in {current_section} section for {section_message_count} messages")
        
        # Final validation
        final_progression = flow_validator.extract_section_progression(conversation_log)
        expected_progression = ["interview", "icp", "pain"]
        
        assert final_progression == expected_progression
    
    @pytest.mark.asyncio 
    async def test_section_stuck_detection(self, agent_client):
        """
        Test Case: Detect when agent gets stuck in one section
        
        Scenario: Agent keeps asking interview questions without progressing
        """
        
        stuck_conversation = [
            "Hello, I want to create my value canvas",
            "What's your name?",
            "John",
            "What's your company?", 
            "Acme Corp",
            "What's your name?",  # Back to name - stuck in interview
            "I said John",
            "What industry are you in?",
            "Technology", 
            "What's your name again?",  # Still stuck asking interview questions
        ]
        
        flow_validator = ValueCanvasFlowValidator()
        section_tracker = {"interview": 0, "current_section": None}
        
        for i in range(0, len(stuck_conversation), 2):
            if i + 1 < len(stuck_conversation):
                user_msg = stuck_conversation[i]
                expected_response = stuck_conversation[i + 1]
                
                actual_response = await agent_client.send_message(user_msg)
                
                # Detect current section
                current_section = flow_validator.detect_current_section(actual_response)
                
                if current_section == "interview":
                    section_tracker["interview"] += 1
                    
                    # If stuck in interview for too long
                    if section_tracker["interview"] > 6:  # Max 6 interview messages
                        pytest.fail(f"Agent stuck in interview section for {section_tracker['interview']} messages")
```

### Test 3: Timeout and Recovery Mechanisms

```python
class TestTimeoutAndRecovery:
    
    @pytest.mark.asyncio
    async def test_conversation_timeout_detection(self, agent_client):
        """
        Test Case: Detect when conversation takes too long to progress
        
        Scenario: Agent takes more than 2 minutes to progress through a section
        """
        
        start_time = datetime.now()
        max_section_duration = timedelta(minutes=2)
        
        # Simulate slow conversation
        slow_messages = [
            "Hello, I want to create my value canvas",
            "What's your name?",
            "John", 
            # Simulate agent taking too long to respond or progress
        ]
        
        section_start_time = datetime.now()
        current_section = "interview"
        
        for message in slow_messages:
            response_start = datetime.now()
            
            # Add artificial delay to simulate slow agent
            await asyncio.sleep(1)  # Simulate processing time
            
            response = await agent_client.send_message(message)
            response_time = datetime.now() - response_start
            
            # Check if section is taking too long
            section_duration = datetime.now() - section_start_time
            
            if section_duration > max_section_duration:
                # Test timeout detection mechanism
                timeout_detected = True
                recovery_action = "restart_section"  # Or other recovery strategy
                
                assert timeout_detected, f"Timeout should be detected for {current_section} after {section_duration}"
                assert recovery_action in ["restart_section", "skip_section", "escalate_to_human"]
    
    @pytest.mark.asyncio
    async def test_automatic_recovery_from_loops(self, agent_client):
        """
        Test Case: Validate automatic recovery when recursion is detected
        
        Scenario: When loop is detected, agent should implement recovery strategy
        """
        
        loop_detector = ConversationLoopDetector(max_repeats=2)
        recovery_strategies = []
        
        # Create conversation that will trigger loop
        loop_conversation = [
            "Hello",
            "What's your name?",
            "John", 
            "What's your name?",  # First repeat
            "I told you, John",
            "What's your name?",  # Second repeat - should trigger recovery
        ]
        
        for i in range(0, len(loop_conversation), 2):
            if i + 1 < len(loop_conversation):
                user_msg = loop_conversation[i]
                
                response = await agent_client.send_message(user_msg)
                
                is_loop, loop_details = loop_detector.detect_loop(response)
                
                if is_loop:
                    # Test recovery mechanism
                    recovery_response = await agent_client.trigger_recovery()
                    recovery_strategies.append(recovery_response.get("strategy"))
                    
                    # Validate recovery was effective
                    next_response = await agent_client.send_message("Let's continue")
                    
                    # Recovery should not repeat the loop
                    is_still_loop, _ = loop_detector.detect_loop(next_response)
                    assert not is_still_loop, "Recovery mechanism failed to break the loop"
        
        # Validate recovery strategies were applied
        assert len(recovery_strategies) > 0, "No recovery strategies were triggered"
        assert all(strategy in ["context_reset", "section_skip", "prompt_variation"] 
                  for strategy in recovery_strategies)
```

## Integration with Existing Test Suite

### File Structure Integration

```
tests/
├── conftest.py                          # Existing
├── core/                               # Existing  
├── service/                            # Existing
├── integration/                        # Existing
└── value_canvas/                       # Existing
    ├── Dynamic_Value_Canvas_Test.py    # Existing
    └── recursion_detection/            # NEW DIRECTORY
        ├── __init__.py
        ├── test_conversation_loops.py   # Loop detection tests
        ├── test_flow_progression.py     # Flow validation tests
        ├── test_timeout_recovery.py     # Recovery mechanism tests
        └── helpers/
            ├── __init__.py
            ├── loop_detector.py         # ConversationLoopDetector class
            ├── flow_validator.py        # ValueCanvasFlowValidator class
            └── test_fixtures.py         # Common test data
```

### Configuration Integration

Add to `pyproject.toml`:

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py", "*_test.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
markers = [
    "recursion_detection: marks tests for conversation loop detection",
    "flow_validation: marks tests for conversation flow progression",
    "recovery_mechanisms: marks tests for timeout and recovery",
]
addopts = [
    "--verbose",
    "--tb=short",
    "--strict-markers",
    "--disable-warnings",
]

# New section for recursion detection
[tool.pytest.recursion_detection]
similarity_threshold = 0.8
max_repeats = 3
section_timeout_minutes = 2
max_messages_per_section = 10
```

## Test Execution Commands

### Running Recursion Detection Tests

```bash
# Run all recursion detection tests
pytest tests/value_canvas/recursion_detection/ -v

# Run specific test categories
pytest tests/value_canvas/recursion_detection/test_conversation_loops.py -v
pytest tests/value_canvas/recursion_detection/test_flow_progression.py -v  
pytest tests/value_canvas/recursion_detection/test_timeout_recovery.py -v

# Run with specific markers
pytest -m recursion_detection -v
pytest -m flow_validation -v
pytest -m recovery_mechanisms -v

# Run with coverage
pytest tests/value_canvas/recursion_detection/ --cov=src --cov-report=html

# Run with timeout protection (prevent tests from getting stuck)
pytest tests/value_canvas/recursion_detection/ --timeout=300  # 5 minute timeout
```

## Expected Test Outcomes and Validation

### Success Criteria

1. **Loop Detection Accuracy**: Tests should detect 90%+ of actual recursion loops
2. **Flow Progression Validation**: Tests should validate correct section transitions
3. **False Positive Rate**: < 5% false positives for loop detection
4. **Recovery Effectiveness**: Recovery mechanisms should break loops within 3 attempts
5. **Performance**: Tests should complete within 5 minutes per test suite

### Test Reporting

```python
# Example test report structure
{
    "test_session": {
        "timestamp": "2025-08-28T10:30:00Z",
        "duration": "4.2 minutes",
        "tests_run": 15,
        "tests_passed": 13,
        "tests_failed": 2
    },
    "recursion_detection_results": {
        "loops_detected": 3,
        "false_positives": 0,
        "accuracy": "100%",
        "avg_detection_time": "1.2 seconds"
    },
    "flow_progression_results": {
        "section_transitions": 8,
        "valid_transitions": 7,
        "invalid_transitions": 1,
        "stuck_sections_detected": 2
    },
    "recovery_mechanism_results": {
        "recovery_attempts": 3,
        "successful_recoveries": 3,
        "recovery_strategies_used": ["context_reset", "prompt_variation"]
    }
}
```

## Continuous Integration Integration

### GitHub Actions Workflow

```yaml
# .github/workflows/recursion_detection_tests.yml
name: Backend Recursion Detection Tests

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  recursion-detection-tests:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
        
    - name: Install dependencies
      run: |
        pip install -e .
        pip install pytest pytest-asyncio pytest-timeout pytest-cov
        
    - name: Run recursion detection tests
      run: |
        pytest tests/value_canvas/recursion_detection/ \
          --timeout=300 \
          --cov=src \
          --cov-report=xml \
          --junit-xml=test-results.xml
          
    - name: Upload test results
      uses: actions/upload-artifact@v3
      with:
        name: test-results
        path: test-results.xml
```

## Troubleshooting and Debugging

### Common Issues and Solutions

1. **Tests Timing Out**: Increase timeout values in pytest configuration
2. **False Positives in Loop Detection**: Adjust similarity threshold in ConversationLoopDetector
3. **Agent Not Responding**: Check API endpoint configuration and authentication
4. **Memory Issues with Long Conversations**: Implement message history truncation

### Debug Mode Configuration

```python
# For debugging recursion detection
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Enable detailed conversation logging
ENABLE_CONVERSATION_DEBUG = True
CONVERSATION_LOG_PATH = "debug/conversation_logs/"
```

## Next Steps and Implementation

1. **Create Helper Classes**: Implement ConversationLoopDetector and ValueCanvasFlowValidator
2. **Set up Test Infrastructure**: Create test fixtures and mock agent client
3. **Implement Core Tests**: Start with basic loop detection tests
4. **Add Flow Validation**: Implement section progression validation
5. **Integrate Recovery Mechanisms**: Add timeout and recovery testing
6. **Run Test Suite**: Execute tests against actual agent backend
7. **Analyze Results**: Review test outcomes and adjust parameters
8. **Continuous Monitoring**: Set up automated test execution in CI/CD

This comprehensive testing framework will provide robust detection and handling of recursion loops in the LangGraph Value Canvas agent backend, addressing the core issue identified in the frontend testing conversation.