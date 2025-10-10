"""
End-to-End Integration Test for Concept Pitch (CAOS) Agent

This test simulates the complete flow:
1. Generation → 2. Refinement → 3. Save

Tests the full integration of the Concept Pitch agent including:
- Agent state management
- Pitch generation (Pain-, Gain-, Prize-driven variations)
- Refinement logic
- Data persistence via sync layer
- JSON file creation and validation
"""

import json
import os
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock
from typing import Dict, Any

import pytest
from pydantic import BaseModel

# Import the Concept Pitch agent components
from src.agents.concept_pitch.agent import run_concept_pitch_agent, AgentState
from src.agents.concept_pitch.sync import save_pitch_to_project, load_pitch_from_project
from src.agents.concept_pitch.refine import refine_pitch
from src.agents.concept_pitch.prompts import (
    PAIN_PITCH_TEMPLATE, 
    GAIN_PITCH_TEMPLATE, 
    PRIZE_PITCH_TEMPLATE
)


class MockLLMResponse(BaseModel):
    """Mock LLM response for testing"""
    content: str


class ConceptPitchE2ETest:
    """End-to-end test orchestrator for Concept Pitch Agent"""
    
    def __init__(self):
        self.test_data = {
            "icp": "startup founders",
            "pain": "burnout and lack of clarity",
            "gain": "strategic clarity and sustainable growth", 
            "prize": "freedom to build what matters",
            "signature_method": "CAOS framework"
        }
        self.temp_dir = None
        self.saved_files = []
    
    def setup_temp_directory(self):
        """Set up temporary directory for testing file operations"""
        self.temp_dir = tempfile.mkdtemp(prefix="concept_pitch_test_")
        return self.temp_dir
    
    def cleanup_temp_directory(self):
        """Clean up temporary directory and files"""
        if self.temp_dir and os.path.exists(self.temp_dir):
            import shutil
            shutil.rmtree(self.temp_dir)
    
    def create_mock_llm_response(self, content: str) -> MockLLMResponse:
        """Create a mock LLM response"""
        return MockLLMResponse(content=content)


@pytest.fixture
def concept_pitch_test():
    """Fixture for Concept Pitch E2E test setup"""
    test = ConceptPitchE2ETest()
    test.setup_temp_directory()
    yield test
    test.cleanup_temp_directory()


@pytest.fixture
def mock_llm():
    """Mock LLM for testing"""
    with patch('src.agents.concept_pitch.agent.ChatOpenAI') as mock_chat:
        mock_instance = MagicMock()
        mock_instance.invoke.return_value = MockLLMResponse(
            content="This is a mock LLM response for testing pitch generation."
        )
        mock_chat.return_value = mock_instance
        yield mock_instance


@pytest.fixture
def mock_refine_llm():
    """Mock LLM for refinement testing"""
    with patch('src.agents.concept_pitch.refine.ChatOpenAI') as mock_chat:
        mock_instance = MagicMock()
        mock_instance.invoke.return_value = MockLLMResponse(
            content="This is a refined version of the pitch based on your feedback."
        )
        mock_chat.return_value = mock_instance
        yield mock_instance


class TestConceptPitchAgentE2E:
    """End-to-end integration tests for Concept Pitch Agent"""
    
    def test_agent_state_creation(self, concept_pitch_test):
        """Test that AgentState can be created with proper data"""
        state = AgentState(
            icp=concept_pitch_test.test_data["icp"],
            pain=concept_pitch_test.test_data["pain"],
            gain=concept_pitch_test.test_data["gain"],
            prize=concept_pitch_test.test_data["prize"],
            signature_method=concept_pitch_test.test_data["signature_method"]
        )
        
        assert state.icp == "startup founders"
        assert state.pain == "burnout and lack of clarity"
        assert state.gain == "strategic clarity and sustainable growth"
        assert state.prize == "freedom to build what matters"
        assert state.signature_method == "CAOS framework"
        assert state.needs_refinement is False
        assert state.checklist_ready is False
        assert isinstance(state.concept_pitch, dict)
        assert isinstance(state.messages, list)
    
    def test_pitch_generation_flow(self, concept_pitch_test, mock_llm):
        """Test the complete pitch generation flow"""
        # Create initial state
        initial_state = AgentState(
            icp=concept_pitch_test.test_data["icp"],
            pain=concept_pitch_test.test_data["pain"],
            gain=concept_pitch_test.test_data["gain"],
            prize=concept_pitch_test.test_data["prize"],
            signature_method=concept_pitch_test.test_data["signature_method"]
        )
        
        # Mock the graph execution
        with patch('src.agents.concept_pitch.agent.build_concept_pitch_graph') as mock_build_graph:
            mock_graph = MagicMock()
            mock_graph.invoke.return_value = AgentState(
                icp=initial_state.icp,
                pain=initial_state.pain,
                gain=initial_state.gain,
                prize=initial_state.prize,
                signature_method=initial_state.signature_method,
                concept_pitch={
                    "pain_pitch": "I've been speaking to a few startup founders, and I'm seeing the same pattern: they're constantly dealing with burnout and lack of clarity, which leads to chaotic launches and unsustainable growth.",
                    "gain_pitch": "You know how startup founders struggle with burnout and lack of clarity? I'm building something that helps them achieve strategic clarity and sustainable growth in a few weeks—without the usual hassle.",
                    "prize_pitch": "A lot of startup founders I talk to say they ultimately want freedom to build what matters. But right now they're stuck dealing with burnout and lack of clarity, and nothing seems to really move the needle.",
                    "llm_response": "Mock LLM response for pitch generation"
                },
                needs_refinement=True,
                checklist_ready=False,
                messages=[]
            )
            mock_build_graph.return_value = mock_graph
            
            # Run the agent
            result = run_concept_pitch_agent(initial_state)
            
            # Validate results
            assert result is not None
            assert isinstance(result, AgentState)
            assert "pain_pitch" in result.concept_pitch
            assert "gain_pitch" in result.concept_pitch
            assert "prize_pitch" in result.concept_pitch
            assert result.needs_refinement is True
            
            # Validate pitch content
            pain_pitch = result.concept_pitch["pain_pitch"]
            gain_pitch = result.concept_pitch["gain_pitch"]
            prize_pitch = result.concept_pitch["prize_pitch"]
            
            assert "startup founders" in pain_pitch
            assert "burnout" in pain_pitch
            assert "startup founders" in gain_pitch
            assert "strategic clarity" in gain_pitch
            assert "startup founders" in prize_pitch
            assert "freedom" in prize_pitch
    
    def test_pitch_refinement_flow(self, concept_pitch_test, mock_refine_llm):
        """Test the pitch refinement flow"""
        # Create state with existing pitches
        state_with_pitches = AgentState(
            icp=concept_pitch_test.test_data["icp"],
            pain=concept_pitch_test.test_data["pain"],
            gain=concept_pitch_test.test_data["gain"],
            prize=concept_pitch_test.test_data["prize"],
            signature_method=concept_pitch_test.test_data["signature_method"],
            concept_pitch={
                "pain_pitch": "Original pain pitch",
                "gain_pitch": "Original gain pitch", 
                "prize_pitch": "Original prize pitch"
            },
            needs_refinement=True,
            user_feedback="Make it sound more hopeful and positive"
        )
        
        # Test refinement without feedback (should ask for feedback)
        state_no_feedback = AgentState(
            icp=concept_pitch_test.test_data["icp"],
            concept_pitch={"pain_pitch": "Test pitch"},
            needs_refinement=True
        )
        
        result_no_feedback = refine_pitch(state_no_feedback)
        assert result_no_feedback.assistant_message is not None
        assert "adjustment" in result_no_feedback.assistant_message.lower()
        
        # Test refinement with feedback
        result_with_feedback = refine_pitch(state_with_pitches)
        
        assert result_with_feedback is not None
        assert isinstance(result_with_feedback, AgentState)
        assert "refined_version" in result_with_feedback.concept_pitch
        assert result_with_feedback.needs_refinement is False
        assert result_with_feedback.checklist_ready is True
        assert result_with_feedback.assistant_message is not None
        assert "refined version" in result_with_feedback.assistant_message.lower()
    
    def test_sync_layer_save_functionality(self, concept_pitch_test):
        """Test the sync layer save functionality"""
        # Mock the save directory to use temp directory
        with patch('src.agents.concept_pitch.sync.get_save_directory') as mock_get_dir:
            mock_get_dir.return_value = Path(concept_pitch_test.temp_dir)
            
            # Test data for saving
            test_pitch_data = {
                "pain_pitch": "I've been speaking to a few startup founders, and I'm seeing the same pattern: they're constantly dealing with burnout and lack of clarity, which leads to chaotic launches and unsustainable growth.",
                "gain_pitch": "You know how startup founders struggle with burnout and lack of clarity? I'm building something that helps them achieve strategic clarity and sustainable growth in a few weeks—without the usual hassle.",
                "prize_pitch": "A lot of startup founders I talk to say they ultimately want freedom to build what matters. But right now they're stuck dealing with burnout and lack of clarity, and nothing seems to really move the needle.",
                "refined_version": "This is the final refined version of the concept pitch.",
                "refinement_count": 2,
                "canvas_data": concept_pitch_test.test_data
            }
            
            # Test save functionality
            save_result = save_pitch_to_project(
                project_id="test_project_e2e",
                concept_pitch_data=test_pitch_data,
                user_id=123,
                thread_id="test_thread_e2e"
            )
            
            # Validate save result
            assert save_result["success"] is True
            assert "file_path" in save_result
            assert "filename" in save_result
            assert save_result["project_id"] == "test_project_e2e"
            assert save_result["pitch_count"] == 3
            
            # Verify file was created
            file_path = Path(save_result["file_path"])
            assert file_path.exists()
            assert file_path.suffix == ".json"
            
            # Verify file content
            with open(file_path, 'r', encoding='utf-8') as f:
                saved_data = json.load(f)
            
            # Test json.dump functionality (write test)
            test_write_data = {"test": "json.dump functionality"}
            test_write_path = file_path.parent / "test_write.json"
            with open(test_write_path, 'w', encoding='utf-8') as f:
                json.dump(test_write_data, f, indent=2, ensure_ascii=False)
            
            assert "metadata" in saved_data
            assert "pitch_variations" in saved_data
            assert "selected_pitch" in saved_data
            assert "canvas_data" in saved_data
            
            # Validate metadata
            metadata = saved_data["metadata"]
            assert metadata["project_id"] == "test_project_e2e"
            assert metadata["user_id"] == 123
            assert metadata["thread_id"] == "test_thread_e2e"
            assert metadata["agent_version"] == "concept_pitch_v1.0"
            assert metadata["refinement_count"] == 2
            
            # Validate pitch variations
            pitch_variations = saved_data["pitch_variations"]
            assert "pain_pitch" in pitch_variations
            assert "gain_pitch" in pitch_variations
            assert "prize_pitch" in pitch_variations
            assert len(pitch_variations["pain_pitch"]) > 0
            assert len(pitch_variations["gain_pitch"]) > 0
            assert len(pitch_variations["prize_pitch"]) > 0
            
            # Validate selected pitch
            assert saved_data["selected_pitch"] == test_pitch_data["refined_version"]
            
            # Store for cleanup
            concept_pitch_test.saved_files.append(file_path)
    
    def test_sync_layer_load_functionality(self, concept_pitch_test):
        """Test the sync layer load functionality"""
        # First save some data
        with patch('src.agents.concept_pitch.sync.get_save_directory') as mock_get_dir:
            mock_get_dir.return_value = Path(concept_pitch_test.temp_dir)
            
            test_pitch_data = {
                "pain_pitch": "Test pain pitch for loading",
                "gain_pitch": "Test gain pitch for loading",
                "prize_pitch": "Test prize pitch for loading",
                "refinement_count": 1
            }
            
            save_result = save_pitch_to_project(
                project_id="test_load_project",
                concept_pitch_data=test_pitch_data,
                user_id=456,
                thread_id="test_load_thread"
            )
            
            assert save_result["success"] is True
            
            # Test load functionality
            load_result = load_pitch_from_project("test_load_project")
            
            # Validate load result
            assert load_result["success"] is True
            assert "data" in load_result
            assert "metadata" in load_result
            assert "pitch_variations" in load_result
            
            # Validate loaded data
            loaded_data = load_result["data"]
            assert loaded_data["metadata"]["project_id"] == "test_load_project"
            assert loaded_data["metadata"]["user_id"] == 456
            assert loaded_data["pitch_variations"]["pain_pitch"] == "Test pain pitch for loading"
            assert loaded_data["pitch_variations"]["gain_pitch"] == "Test gain pitch for loading"
            assert loaded_data["pitch_variations"]["prize_pitch"] == "Test prize pitch for loading"
    
    def test_complete_e2e_flow(self, concept_pitch_test, mock_llm, mock_refine_llm):
        """Test the complete end-to-end flow: Generation → Refinement → Save"""
        
        # Step 1: Generation
        print("\n🚀 Step 1: Testing Pitch Generation...")
        
        initial_state = AgentState(
            icp=concept_pitch_test.test_data["icp"],
            pain=concept_pitch_test.test_data["pain"],
            gain=concept_pitch_test.test_data["gain"],
            prize=concept_pitch_test.test_data["prize"],
            signature_method=concept_pitch_test.test_data["signature_method"]
        )
        
        # Mock the complete generation flow
        with patch('src.agents.concept_pitch.agent.build_concept_pitch_graph') as mock_build_graph:
            mock_graph = MagicMock()
            
            # Mock the generation result
            generated_state = AgentState(
                icp=initial_state.icp,
                pain=initial_state.pain,
                gain=initial_state.gain,
                prize=initial_state.prize,
                signature_method=initial_state.signature_method,
                concept_pitch={
                    "pain_pitch": "I've been speaking to a few startup founders, and I'm seeing the same pattern: they're constantly dealing with burnout and lack of clarity, which leads to chaotic launches and unsustainable growth.",
                    "gain_pitch": "You know how startup founders struggle with burnout and lack of clarity? I'm building something that helps them achieve strategic clarity and sustainable growth in a few weeks—without the usual hassle.",
                    "prize_pitch": "A lot of startup founders I talk to say they ultimately want freedom to build what matters. But right now they're stuck dealing with burnout and lack of clarity, and nothing seems to really move the needle.",
                    "llm_response": "Generated three pitch variations successfully"
                },
                needs_refinement=True,
                checklist_ready=False,
                messages=[]
            )
            
            mock_graph.invoke.return_value = generated_state
            mock_build_graph.return_value = mock_graph
            
            # Run generation
            generation_result = run_concept_pitch_agent(initial_state)
            
            # Validate generation
            assert generation_result.needs_refinement is True
            assert len(generation_result.concept_pitch) >= 3
            assert "pain_pitch" in generation_result.concept_pitch
            assert "gain_pitch" in generation_result.concept_pitch
            assert "prize_pitch" in generation_result.concept_pitch
            
            print("✅ Generation step completed successfully")
            
            # Step 2: Refinement
            print("\n🔧 Step 2: Testing Pitch Refinement...")
            
            # Add user feedback for refinement
            generation_result.user_feedback = "Make the tone more conversational and add more specific examples"
            
            # Run refinement
            refinement_result = refine_pitch(generation_result)
            
            # Validate refinement
            assert refinement_result.needs_refinement is False
            assert refinement_result.checklist_ready is True
            assert "refined_version" in refinement_result.concept_pitch
            assert refinement_result.assistant_message is not None
            
            print("✅ Refinement step completed successfully")
            
            # Step 3: Save
            print("\n💾 Step 3: Testing Data Persistence...")
            
            # Mock save directory
            with patch('src.agents.concept_pitch.sync.get_save_directory') as mock_get_dir:
                mock_get_dir.return_value = Path(concept_pitch_test.temp_dir)
                
                # Prepare final data for saving
                final_pitch_data = refinement_result.concept_pitch.copy()
                final_pitch_data.update({
                    "refinement_count": 1,
                    "canvas_data": concept_pitch_test.test_data,
                    "final_status": "completed"
                })
                
                # Run save
                save_result = save_pitch_to_project(
                    project_id="e2e_test_project",
                    concept_pitch_data=final_pitch_data,
                    user_id=789,
                    thread_id="e2e_test_thread"
                )
                
                # Validate save
                assert save_result["success"] is True
                assert save_result["project_id"] == "e2e_test_project"
                assert save_result["pitch_count"] == 3
                
                # Verify file creation
                file_path = Path(save_result["file_path"])
                assert file_path.exists()
                
                # Verify file content structure
                with open(file_path, 'r', encoding='utf-8') as f:
                    saved_data = json.load(f)
                
                assert "metadata" in saved_data
                assert "pitch_variations" in saved_data
                assert "selected_pitch" in saved_data
                assert "refinement_history" in saved_data
                assert "canvas_data" in saved_data
                
                # Validate metadata
                metadata = saved_data["metadata"]
                assert metadata["project_id"] == "e2e_test_project"
                assert metadata["user_id"] == 789
                assert metadata["thread_id"] == "e2e_test_thread"
                assert metadata["agent_version"] == "concept_pitch_v1.0"
                
                print("✅ Save step completed successfully")
                
                # Step 4: Load and Verify
                print("\n📂 Step 4: Testing Data Retrieval...")
                
                load_result = load_pitch_from_project("e2e_test_project")
                
                assert load_result["success"] is True
                assert load_result["data"]["metadata"]["project_id"] == "e2e_test_project"
                assert len(load_result["data"]["pitch_variations"]) == 3
                
                print("✅ Load step completed successfully")
                
                print("\n🎉 Complete E2E Flow Test Passed!")
                print("=" * 50)
                print("✅ Generation: All three pitch variations created")
                print("✅ Refinement: Pitch successfully refined based on feedback")
                print("✅ Save: Data persisted to JSON file with proper metadata")
                print("✅ Load: Data successfully retrieved and validated")
                print("=" * 50)


def test_pitch_templates_formatting():
    """Test that pitch templates can be formatted with test data"""
    test_state = AgentState(
        icp="startup founders",
        pain="burnout and lack of clarity",
        gain="strategic clarity and sustainable growth",
        prize="freedom to build what matters"
    )
    
    # Test template formatting (this would normally be done by the agent)
    from src.agents.concept_pitch.prompts import format_pitch_template
    
    pain_pitch = format_pitch_template(PAIN_PITCH_TEMPLATE, test_state)
    gain_pitch = format_pitch_template(GAIN_PITCH_TEMPLATE, test_state)
    prize_pitch = format_pitch_template(PRIZE_PITCH_TEMPLATE, test_state)
    
    # Validate that templates are formatted
    assert "startup founders" in pain_pitch
    assert "burnout" in pain_pitch
    assert "startup founders" in gain_pitch
    assert "strategic clarity" in gain_pitch
    assert "startup founders" in prize_pitch
    assert "freedom" in prize_pitch


def test_agent_error_handling():
    """Test error handling in the agent"""
    # Test with invalid state
    invalid_state = AgentState(
        icp="",  # Empty ICP
        pain="",
        gain="",
        prize="",
        signature_method=""
    )
    
    # The agent should handle empty inputs gracefully
    with patch('src.agents.concept_pitch.agent.build_concept_pitch_graph') as mock_build_graph:
        mock_graph = MagicMock()
        mock_graph.invoke.return_value = invalid_state
        mock_build_graph.return_value = mock_graph
        
        result = run_concept_pitch_agent(invalid_state)
        
        # Should return a state even with empty inputs
        assert result is not None
        assert isinstance(result, AgentState)


if __name__ == "__main__":
    # Run the tests
    pytest.main([__file__, "-v", "--tb=short"])
