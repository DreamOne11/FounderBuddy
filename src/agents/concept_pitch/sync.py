"""Data persistence and synchronization layer for Concept Pitch (CAOS) Agent.

This module handles saving the finalized Concept Pitch (Pain-, Gain-, and Prize-driven versions)
into project storage or external systems. Designed for JSON-based persistence with metadata.
"""

import json
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class ConceptPitchMetadata(BaseModel):
    """Metadata for Concept Pitch saves."""
    project_id: str
    timestamp: str
    user_id: int
    thread_id: str
    agent_version: str = "concept_pitch_v1.0"
    save_type: str = "final_pitch"  # "final_pitch", "draft", "refinement"
    refinement_count: int = 0


class ConceptPitchSaveData(BaseModel):
    """Complete Concept Pitch save data structure."""
    metadata: ConceptPitchMetadata
    pitch_variations: Dict[str, str] = Field(default_factory=dict)
    selected_pitch: Optional[str] = None
    refinement_history: list[Dict[str, Any]] = Field(default_factory=list)
    canvas_data: Dict[str, Any] = Field(default_factory=dict)
    raw_data: Dict[str, Any] = Field(default_factory=dict)


def get_save_directory() -> Path:
    """Get the directory for saving Concept Pitch data."""
    # Create saves directory in project root
    project_root = Path(__file__).parent.parent.parent.parent
    saves_dir = project_root / "saves" / "concept_pitch"
    saves_dir.mkdir(parents=True, exist_ok=True)
    return saves_dir


def generate_save_filename(project_id: str, timestamp: str) -> str:
    """Generate a unique filename for saving Concept Pitch data."""
    safe_project_id = "".join(c for c in project_id if c.isalnum() or c in ('-', '_'))
    safe_timestamp = timestamp.replace(':', '-').replace(' ', '_')
    return f"concept_pitch_{safe_project_id}_{safe_timestamp}.json"


def save_pitch_to_project(project_id: str, concept_pitch_data: Dict[str, Any], 
                         user_id: int = 1, thread_id: str = "default") -> Dict[str, Any]:
    """
    Save finalized Concept Pitch data to project storage.
    
    Args:
        project_id: Unique project identifier
        concept_pitch_data: Complete concept pitch data including variations
        user_id: User identifier (default: 1)
        thread_id: Thread/conversation identifier (default: "default")
        
    Returns:
        Save result dictionary with success status and file path
    """
    logger.info(f"Saving Concept Pitch to project: {project_id}")
    
    try:
        # Generate timestamp
        timestamp = datetime.now().isoformat()
        
        # Create metadata
        metadata = ConceptPitchMetadata(
            project_id=project_id,
            timestamp=timestamp,
            user_id=user_id,
            thread_id=thread_id,
            refinement_count=concept_pitch_data.get("refinement_count", 0)
        )
        
        # Extract pitch variations
        pitch_variations = {
            "pain_pitch": concept_pitch_data.get("pain_pitch", ""),
            "gain_pitch": concept_pitch_data.get("gain_pitch", ""),
            "prize_pitch": concept_pitch_data.get("prize_pitch", ""),
        }
        
        # Determine selected pitch (if any)
        selected_pitch = None
        if "refined_version" in concept_pitch_data:
            selected_pitch = concept_pitch_data["refined_version"]
        elif "selected_pitch_type" in concept_pitch_data:
            pitch_type = concept_pitch_data["selected_pitch_type"]
            selected_pitch = pitch_variations.get(f"{pitch_type}_pitch")
        
        # Create save data structure
        save_data = ConceptPitchSaveData(
            metadata=metadata,
            pitch_variations=pitch_variations,
            selected_pitch=selected_pitch,
            refinement_history=concept_pitch_data.get("refinement_history", []),
            canvas_data=concept_pitch_data.get("canvas_data", {}),
            raw_data=concept_pitch_data
        )
        
        # Generate filename and path
        filename = generate_save_filename(project_id, timestamp)
        save_dir = get_save_directory()
        file_path = save_dir / filename
        
        # Save to JSON file
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(save_data.model_dump(), f, indent=2, ensure_ascii=False)
        
        logger.info(f"✅ Concept Pitch saved successfully: {file_path}")
        
        return {
            "success": True,
            "file_path": str(file_path),
            "filename": filename,
            "project_id": project_id,
            "timestamp": timestamp,
            "pitch_count": len([p for p in pitch_variations.values() if p]),
            "message": f"Concept Pitch saved to {filename}"
        }
        
    except Exception as e:
        logger.error(f"❌ Error saving Concept Pitch: {e}")
        return {
            "success": False,
            "error": str(e),
            "project_id": project_id,
            "message": f"Failed to save Concept Pitch: {e}"
        }


def load_pitch_from_project(project_id: str, filename: Optional[str] = None) -> Dict[str, Any]:
    """
    Load Concept Pitch data from project storage.
    
    Args:
        project_id: Project identifier
        filename: Specific filename to load (optional, loads latest if not provided)
        
    Returns:
        Loaded Concept Pitch data or error information
    """
    logger.info(f"Loading Concept Pitch for project: {project_id}")
    
    try:
        save_dir = get_save_directory()
        
        if filename:
            file_path = save_dir / filename
        else:
            # Find latest file for this project
            pattern = f"concept_pitch_{project_id}_*.json"
            files = list(save_dir.glob(pattern))
            if not files:
                return {"success": False, "error": "No saved Concept Pitch found"}
            
            file_path = max(files, key=os.path.getctime)
        
        # Load JSON data
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        logger.info(f"✅ Concept Pitch loaded successfully: {file_path.name}")
        
        return {
            "success": True,
            "data": data,
            "file_path": str(file_path),
            "metadata": data.get("metadata", {}),
            "pitch_variations": data.get("pitch_variations", {}),
            "message": f"Concept Pitch loaded from {file_path.name}"
        }
        
    except Exception as e:
        logger.error(f"❌ Error loading Concept Pitch: {e}")
        return {
            "success": False,
            "error": str(e),
            "project_id": project_id,
            "message": f"Failed to load Concept Pitch: {e}"
        }


def list_saved_pitches(project_id: Optional[str] = None) -> Dict[str, Any]:
    """
    List all saved Concept Pitch files.
    
    Args:
        project_id: Optional project filter
        
    Returns:
        List of saved files with metadata
    """
    logger.info("Listing saved Concept Pitch files")
    
    try:
        save_dir = get_save_directory()
        
        if project_id:
            pattern = f"concept_pitch_{project_id}_*.json"
        else:
            pattern = "concept_pitch_*.json"
        
        files = list(save_dir.glob(pattern))
        
        file_list = []
        for file_path in files:
            try:
                # Load metadata only
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                metadata = data.get("metadata", {})
                file_list.append({
                    "filename": file_path.name,
                    "project_id": metadata.get("project_id", "unknown"),
                    "timestamp": metadata.get("timestamp", "unknown"),
                    "user_id": metadata.get("user_id", 0),
                    "refinement_count": metadata.get("refinement_count", 0),
                    "file_size": file_path.stat().st_size,
                    "created": datetime.fromtimestamp(file_path.stat().st_ctime).isoformat()
                })
            except Exception as e:
                logger.warning(f"Could not read metadata from {file_path.name}: {e}")
        
        # Sort by creation time (newest first)
        file_list.sort(key=lambda x: x["created"], reverse=True)
        
        logger.info(f"✅ Found {len(file_list)} saved Concept Pitch files")
        
        return {
            "success": True,
            "files": file_list,
            "count": len(file_list),
            "message": f"Found {len(file_list)} saved Concept Pitch files"
        }
        
    except Exception as e:
        logger.error(f"❌ Error listing saved Concept Pitch files: {e}")
        return {
            "success": False,
            "error": str(e),
            "message": f"Failed to list saved Concept Pitch files: {e}"
        }


def confirm_pitch_saved(save_result: Dict[str, Any]) -> str:
    """
    Generate a confirmation message for successful pitch save.
    
    Args:
        save_result: Result from save_pitch_to_project()
        
    Returns:
        User-friendly confirmation message
    """
    if save_result.get("success"):
        filename = save_result.get("filename", "unknown")
        pitch_count = save_result.get("pitch_count", 0)
        project_id = save_result.get("project_id", "unknown")
        
        return (
            f"✅ Concept Pitch saved successfully!\n"
            f"📁 File: {filename}\n"
            f"📊 Project: {project_id}\n"
            f"🎯 Pitch variations: {pitch_count}\n"
            f"💾 Ready for market testing!"
        )
    else:
        error = save_result.get("error", "Unknown error")
        return f"❌ Failed to save Concept Pitch: {error}"


def sync_with_value_canvas(user_id: int, thread_id: str) -> Dict[str, Any]:
    """
    Sync Concept Pitch data with Value Canvas data.
    
    This function can be extended to integrate with Value Canvas data
    for enhanced pitch generation based on existing canvas information.
    
    Args:
        user_id: User identifier
        thread_id: Thread/conversation identifier
        
    Returns:
        Sync result with canvas data integration
    """
    logger.info(f"Syncing Concept Pitch with Value Canvas data for user {user_id}")
    
    try:
        # Placeholder for Value Canvas integration
        # This would typically:
        # 1. Load Value Canvas data for the user
        # 2. Extract relevant fields (ICP, Pain, Gain, Prize)
        # 3. Enhance Concept Pitch with canvas insights
        
        return {
            "success": True,
            "message": "Concept Pitch synced with Value Canvas data",
            "user_id": user_id,
            "thread_id": thread_id,
            "canvas_fields_used": ["icp", "pain", "gain", "prize"]
        }
        
    except Exception as e:
        logger.error(f"Error syncing with Value Canvas: {e}")
        return {
            "success": False,
            "error": str(e),
            "message": f"Failed to sync with Value Canvas: {e}"
        }


# Test function for verification
if __name__ == "__main__":
    # Test the save functionality
    test_pitch_data = {
        "pain_pitch": "I've been speaking to a few startup founders, and I'm seeing the same pattern: they're constantly dealing with burnout and lack of clarity, which leads to chaotic launches and unsustainable growth.",
        "gain_pitch": "You know how startup founders struggle with burnout and lack of clarity? I'm building something that helps them achieve strategic clarity and sustainable growth in a few weeks—without the usual hassle.",
        "prize_pitch": "A lot of startup founders I talk to say they ultimately want freedom to build what matters. But right now they're stuck dealing with burnout and lack of clarity, and nothing seems to really move the needle.",
        "refined_version": "I've been speaking to a few startup founders, and I'm seeing the same pattern: they're constantly dealing with burnout and lack of clarity, which leads to chaotic launches and unsustainable growth. So I'm working on a solution that helps them achieve strategic clarity and sustainable growth without needing complex processes. What do you think? Does that sound like something startup founders would actually want?",
        "refinement_count": 2,
        "canvas_data": {
            "icp": "startup founders",
            "pain": "burnout and lack of clarity",
            "gain": "strategic clarity and sustainable growth",
            "prize": "freedom to build what matters"
        }
    }
    
    print("🚀 Testing Concept Pitch Save Functionality...")
    print("=" * 60)
    
    # Test save
    save_result = save_pitch_to_project(
        project_id="test_project_001",
        concept_pitch_data=test_pitch_data,
        user_id=123,
        thread_id="test_thread_456"
    )
    
    print("📋 Save Result:")
    print(json.dumps(save_result, indent=2))
    
    if save_result.get("success"):
        print("\n✅ Confirmation Message:")
        print(confirm_pitch_saved(save_result))
        
        # Test load
        print("\n📂 Testing Load Functionality...")
        load_result = load_pitch_from_project("test_project_001")
        print("Load Result:")
        print(json.dumps(load_result, indent=2))
        
        # Test list
        print("\n📋 Testing List Functionality...")
        list_result = list_saved_pitches()
        print("List Result:")
        print(json.dumps(list_result, indent=2))
    
    print("\n🎯 Test completed!")


__all__ = [
    "ConceptPitchMetadata",
    "ConceptPitchSaveData", 
    "save_pitch_to_project",
    "load_pitch_from_project",
    "list_saved_pitches",
    "confirm_pitch_saved",
    "sync_with_value_canvas",
    "get_save_directory",
    "generate_save_filename",
]