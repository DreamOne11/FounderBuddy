# DentApp AI Builder API Integration Testing

## API Base URL
`https://dentappaibuilder.enspirittech.co.uk`

## Test Results

### 1. GET Section Details
**Endpoint**: `GET /section_states/{agent_id}/{section_id}?user_id={user_id}`

**Test Command**:
```bash
curl -X GET "https://dentappaibuilder.enspirittech.co.uk/section_states/1/1?user_id=1" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json"
```

**Response Structure**:
```json
{
    "success": true,
    "message": "Section data retrieved successfully",
    "data": {
        "asset_id": 1,
        "current_version": 1,
        "content": "{\"text\":\"...\"}",  // Note: content is JSON string, not object
        "metadata": "{\"ai_generated\":true,...}",  // Note: metadata is JSON string
        "is_completed": true,
        "created_at": "2025-08-08T13:41:07.000000Z",
        "updated_at": "2025-08-08T13:41:07.000000Z"
    },
    "version_history": [...],
    "recent_ai_interactions": [...]
}
```

**Key Observations**:
- `content` field is a **JSON string**, not a Tiptap JSON object
- `metadata` field is also a **JSON string**
- Uses `asset_id` instead of section record ID
- Uses `is_completed` boolean instead of status string

### 2. POST Save Section (Tested)
**Endpoint**: `POST /section_states/{agent_id}/{section_id}`

**Test Payload (IMPORTANT: content must be JSON string)**:
```json
{
    "user_id": 1,
    "content": "{\"type\":\"doc\",\"content\":[{\"type\":\"paragraph\",\"content\":[{\"type\":\"text\",\"text\":\"Test content from Value Canvas agent integration\"}]}]}",
    "metadata": {
        "ai_generated": false,
        "source": "value_canvas_agent"
    },
    "is_completed": true,
    "save_type": "manual"
}
```

**Actual Response**:
```json
{
    "success": true,
    "message": "Asset created successfully",
    "data": {
        "asset_id": 2,
        "current_version": 1,
        "previous_version": 0,
        "is_completed": true,
        "has_changes": true,
        "version_created": true,
        "is_ai_generated": false,
        "ai_interaction_id": null,
        "ai_tracing_id": null
    },
    "change_detection": {
        "content_changed": true,
        "change_summary": "Content modified"
    },
    "version_history": [...]
}
```

**Critical Finding**: 
- ❌ Content sent as object will fail with: `"The content field must be a string."`
- ✅ Content MUST be sent as JSON string (serialized Tiptap JSON)

### 3. Get All Sections Status (Tested)
**Endpoint**: `POST /agent/get-all-sections-status/{agent_id}`

**Test Payload**:
```json
{
    "user_id": 1
}
```

**Actual Response**:
```json
{
    "success": true,
    "message": "Sections status retrieved successfully",
    "data": {
        "user_id": 1,
        "agent_id": 1,
        "total_sections": 5,
        "completed_sections": 1,
        "agent_completion_percentage": 20,
        "is_agent_completed": false,
        "sections": [
            {
                "section_id": 1,
                "section_name": "offer",
                "is_completed": true,
                "has_content": true,
                "current_version": 1,
                "ai_interaction_count": 1
            },
            {
                "section_id": 2,
                "section_name": "pain",
                "is_completed": false,
                "has_content": false,
                "current_version": 0,
                "ai_interaction_count": 0
            },
            {
                "section_id": 3,
                "section_name": "obstacles",
                "is_completed": false,
                "has_content": false,
                "current_version": 0,
                "ai_interaction_count": 0
            },
            {
                "section_id": 4,
                "section_name": "ideal_customer",
                "is_completed": false,
                "has_content": false,
                "current_version": 0,
                "ai_interaction_count": 0
            },
            {
                "section_id": 5,
                "section_name": "prize",
                "is_completed": false,
                "has_content": false,
                "current_version": 0,
                "ai_interaction_count": 0
            }
        ]
    }
}
```

**Section Mapping Discovered**:
- Section 1: "offer"
- Section 2: "pain"
- Section 3: "obstacles"
- Section 4: "ideal_customer"
- Section 5: "prize"

**Note**: These section names don't match our Value Canvas sections exactly!

## Integration Challenges

### 1. Data Format Differences ✅ CONFIRMED
- **Current System**: Expects Tiptap JSON objects
- **New API**: Requires JSON **strings** for content (will reject objects)
- **Solution**: Use `json.dumps()` when sending, `json.loads()` when receiving

### 2. ID Mapping ✅ CONFIRMED
- **Current System**: Uses `doc_id` (document identifier)
- **New API**: Uses `agent_id` (agent identifier)
- **Solution**: Need to determine if agent_id is fixed or needs mapping

### 3. Status Management ✅ CONFIRMED
- **Current System**: Uses status strings ("done", "in_progress", "pending")
- **New API**: Uses `is_completed` boolean
- **Solution**: 
  - `is_completed=true` ← `status="done"`
  - `is_completed=false` ← `status="in_progress" or "pending"`

### 4. Section ID Mismatch 🚨 CRITICAL
- **Current Value Canvas Sections**:
  - interview, icp, pain_1, pain_2, pain_3, deep_fear
  - payoff_1, payoff_2, payoff_3, signature_method, mistakes, prize
- **New API Sections** (only 5!):
  - 1: offer, 2: pain, 3: obstacles, 4: ideal_customer, 5: prize
- **Major Problem**: API only has 5 sections, we need 12+ sections!
- **Solution Needed**: Either:
  - Backend team needs to add more sections
  - Or we need to map multiple Value Canvas sections to single API sections

## Proposed Adapter Pattern

```python
class DentAppAPIAdapter:
    def __init__(self, base_url: str, agent_id: int):
        self.base_url = base_url
        self.agent_id = agent_id
        self.section_id_map = {
            "interview": 1,
            "icp": 2,
            "pain_1": 3,
            # ... etc
        }
    
    async def get_section(self, user_id: str, section_id: str):
        # Map section_id string to numeric
        numeric_id = self.section_id_map.get(section_id, 1)
        # Make API call
        # Parse JSON strings to objects
        # Convert is_completed to status
        
    async def save_section(self, user_id: str, section_id: str, content: dict, score: int, status: str):
        # Convert status to is_completed
        # Serialize content to JSON string if needed
        # Map section_id
        # Make API call
```

## Next Steps

1. **Test remaining endpoints** with actual data
2. **Confirm section ID mapping** with backend team
3. **Clarify agent_id usage** - is it per-user, per-document, or fixed?
4. **Test Tiptap JSON format** compatibility
5. **Implement adapter layer** in tools.py

## Questions for Backend Team

1. What's the mapping between string section IDs (like "icp") and numeric IDs?
2. Is `agent_id` fixed for all Value Canvas operations, or does it vary?
3. Should `content` be a JSON string or can it accept objects?
4. How does the version limit (10 versions) affect our save operations?
5. Is there authentication required for these endpoints?