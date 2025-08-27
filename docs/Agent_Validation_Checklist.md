# Agent Validation Checklist

Complete validation checklist for new agent implementations. Must be completed before deployment to prevent the bugs discovered in Mission Pitch Agent development.

## Pre-Implementation Validation

### Planning Phase
- [ ] **Agent ID Format Defined**: Use consistent hyphen format (`agent-name`) throughout
- [ ] **Section Flow Mapped**: Clear progression order documented
- [ ] **Data Models Designed**: All Pydantic models planned with field names
- [ ] **Database IDs Assigned**: Unique agent ID and section ID ranges allocated
- [ ] **Reference Agent Selected**: Choose working agent to copy patterns from

---

## Backend Implementation Validation

### File Structure
- [ ] **Directory Created**: `src/agents/{agent_name}/` with all required files
- [ ] **Init Files Present**: `__init__.py` in agent directory
- [ ] **All Components**: models.py, prompts.py, tools.py, agent.py all created

### Models (`models.py`)
- [ ] **Status Enum**: `SectionStatus` with PENDING, IN_PROGRESS, DONE
- [ ] **Section Enum**: All sections defined with string values
- [ ] **State Class**: Inherits from `MessagesState` with all required fields
- [ ] **Data Class**: Domain-specific fields for structured data extraction

### Prompts (`prompts.py`)
- [ ] **Section Templates**: All sections have templates with name, description, prompts
- [ ] **Section Order**: `get_section_order()` returns correct sequence
- [ ] **Next Section Logic**: `get_next_unfinished_section()` uses corrected algorithm
- [ ] **Base Prompts**: Communication style and rules defined

**Critical Check - Section Progression Logic:**
```python
# MUST use this corrected pattern
def get_next_unfinished_section(section_states: dict[str, Any]) -> SectionID | None:
    order = get_section_order()
    last_completed_index = -1
    for i, section in enumerate(order):
        state = section_states.get(section.value)
        if state and state.status == SectionStatus.DONE:
            last_completed_index = i
        else:
            break  # ← CRITICAL: Stop at first non-completed
    next_index = last_completed_index + 1
    return order[next_index] if next_index < len(order) else None
```

### Tools (`tools.py`)
- [ ] **Database Methods**: Uses `client.save_section_state()` NOT `save_section_data()`
- [ ] **Content Conversion**: Converts tiptap to plain text with `tiptap_to_plain_text()`
- [ ] **Error Handling**: Proper try/catch with logging
- [ ] **Agent ID**: Correct agent ID constant defined

**Critical Check - Database Save Pattern:**
```python
# MUST use this exact pattern
plain_text = tiptap_to_plain_text(content) if content else ""
dentapp_client = get_dentapp_client()
async with dentapp_client as client:
    response = await client.save_section_state(  # ← Correct method name
        agent_id=AGENT_ID,
        section_id=section_id_int,
        user_id=user_id,
        content=plain_text,  # ← Plain text, not tiptap
        metadata={}
    )
```

### Agent (`agent.py`)
- [ ] **Memory Updater Logic**: Uses `_status_from_output()` function from value canvas
- [ ] **Router Directive Handling**: Respects `RouterDirective.NEXT` for completion
- [ ] **Section State Updates**: Updates both database and local state consistently
- [ ] **Error Recovery**: Proper error handling with logging

**Critical Check - Status Determination:**
```python
# MUST use this exact pattern
def _status_from_output(score, directive):
    if directive == RouterDirective.NEXT:  # ← CRITICAL: Check directive first
        return SectionStatus.DONE
    if score is not None and score >= 3:
        return SectionStatus.DONE
    return SectionStatus.IN_PROGRESS
```

---

## Service Integration Validation

### Agent Registration (`src/agents/agents.py`)
- [ ] **Import Added**: Agent graph imported
- [ ] **AGENTS Dict**: Agent added with correct ID and description
- [ ] **Graph Reference**: Points to correct agent graph

### LangGraph Configuration (`langgraph.json`)
- [ ] **Entry Added**: Agent ID maps to correct graph path
- [ ] **Path Format**: Uses format `"agents.{agent_name}.agent:graph"`
- [ ] **ID Consistency**: Matches ID used in agents.py

### Service Integration (`src/service/service.py`)
- [ ] **Template Import**: `SECTION_TEMPLATES as {AGENT}_TEMPLATES` imported
- [ ] **Initialization**: Agent state initialization added to `_handle_input()`
- [ ] **Invoke Endpoint**: Template selection added (around line 340)
- [ ] **Streaming Endpoint**: Same template selection added (around line 490)

**Critical Check - Template Selection (Both Endpoints):**
```python
# Must be in BOTH invoke and streaming endpoints
if agent_id == "{agent-id}":  # ← Exact hyphen format
    section_templates = {AGENT}_TEMPLATES
elif agent_id == "social-pitch":
    section_templates = SOCIAL_PITCH_TEMPLATES
else:  # default to value_canvas
    section_templates = VALUE_CANVAS_TEMPLATES
```

### Database Integration (`src/integrations/dentapp/dentapp_utils.py`)
- [ ] **Agent ID Constant**: Unique agent ID number defined
- [ ] **Section Mappings**: All sections mapped to database IDs
- [ ] **Context Helper**: `get_agent_id_for_context()` updated
- [ ] **Inference Helper**: `infer_agent_id_from_section()` updated

---

## Frontend Integration Validation

### Config Panel (`dent-langgraph-frontend/src/components/ConfigPanel.tsx`)
- [ ] **Agents Array**: Agent added to selection dropdown
- [ ] **ID Format**: Uses same hyphen format as backend
- [ ] **Display Name**: User-friendly name provided

### Progress Sidebar (`dent-langgraph-frontend/src/components/ProgressSidebar.tsx`)
- [ ] **Section Title**: `getSectionTitle()` handles agent ID
- [ ] **ID Label**: `getIdLabel()` handles agent ID  
- [ ] **Name Label**: `getNameLabel()` handles agent ID
- [ ] **Consistent Naming**: All three functions use consistent terminology

### Chat Area (`dent-langgraph-frontend/src/components/ChatArea.tsx`)
- [ ] **Agent Name**: `getAgentName()` maps ID to display name
- [ ] **Placeholder Text**: `getPlaceholderText()` provides example prompt
- [ ] **Description**: Agent purpose description added

---

## Functional Testing Validation

### Basic Flow Testing
- [ ] **Agent Selection**: Agent appears in frontend dropdown
- [ ] **Conversation Start**: Welcome message appears
- [ ] **First Section**: Correct first section questions asked
- [ ] **User Response**: Handles user input properly
- [ ] **Section Content**: Generates appropriate responses

### Section Progression Testing  
- [ ] **Forward Progress**: Completes section → moves to next section
- [ ] **No Backward Jumps**: Never goes back to previous sections unexpectedly
- [ ] **Sequential Order**: Follows exact section order defined
- [ ] **Final Section**: Reaches implementation/completion section
- [ ] **All Sections**: Tests progression through every section

### Database Persistence Testing
- [ ] **Content Saves**: Section content persists between sessions
- [ ] **Status Updates**: Section completion status saves correctly
- [ ] **Progress Recovery**: Can resume conversation from any point
- [ ] **No Data Loss**: No content lost during section transitions

### Error Recovery Testing
- [ ] **Invalid Input**: Handles malformed user input gracefully
- [ ] **Database Errors**: Recovers from database connection issues
- [ ] **Timeout Handling**: Manages long-running operations
- [ ] **State Consistency**: Maintains consistent state during errors

---

## Performance Validation

### Response Time Testing
- [ ] **Initial Load**: Agent selection responds < 2 seconds
- [ ] **Message Response**: AI responses < 10 seconds typical
- [ ] **Section Transition**: Section changes < 3 seconds
- [ ] **Database Operations**: Save operations < 5 seconds

### Memory Usage Testing
- [ ] **State Size**: Agent state remains reasonable size
- [ ] **Message History**: Short memory properly pruned
- [ ] **No Memory Leaks**: Long conversations don't cause issues
- [ ] **Concurrent Users**: Multiple users don't interfere

---

## Security Validation

### Input Validation
- [ ] **SQL Injection**: Database queries parameterized
- [ ] **XSS Prevention**: User input properly escaped
- [ ] **Content Filtering**: Inappropriate content handling
- [ ] **Rate Limiting**: Prevents abuse/spam

### Data Protection
- [ ] **User Data**: Personal information properly handled
- [ ] **Session Security**: Thread IDs properly validated
- [ ] **Access Control**: Users can only access own data
- [ ] **Audit Logging**: Important operations logged

---

## Pre-Deployment Final Checks

### Code Quality
- [ ] **Linting**: All code passes linting checks
- [ ] **Type Checking**: TypeScript/Python typing validates
- [ ] **Testing**: Unit tests pass for all components
- [ ] **Documentation**: Code properly documented

### Integration Testing
- [ ] **End-to-End**: Complete user journey works
- [ ] **Cross-Browser**: Works in major browsers (if frontend)
- [ ] **Mobile Responsive**: Works on mobile devices
- [ ] **API Compatibility**: Backend APIs work correctly

### Deployment Readiness
- [ ] **Environment Variables**: All configs set properly
- [ ] **Database Migrations**: Schema updates applied
- [ ] **Monitoring**: Logging and metrics configured
- [ ] **Rollback Plan**: Can revert if issues occur

---

## Post-Deployment Monitoring

### First 24 Hours
- [ ] **Error Rate**: Monitor for errors < 1%
- [ ] **User Completion**: Users completing full conversations
- [ ] **Performance**: Response times within targets
- [ ] **Database Load**: DB performance stable

### First Week
- [ ] **User Feedback**: Collect and analyze user feedback  
- [ ] **Conversation Analytics**: Track section progression patterns
- [ ] **Error Analysis**: Review and fix any issues
- [ ] **Performance Optimization**: Tune for better performance

---

## Validation Sign-Off

**Developer:** _________________ **Date:** _________
**QA Tester:** _________________ **Date:** _________  
**Product Owner:** _____________ **Date:** _________

**Deployment Approved:** ☐ Yes ☐ No (specify issues): ________________

---

## Emergency Rollback Criteria

Rollback immediately if:
- [ ] Error rate > 5%
- [ ] Any infinite loops detected  
- [ ] Database corruption or data loss
- [ ] Security vulnerability discovered
- [ ] User completion rate < 50%

**Rollback Procedure:** Documented in deployment guide

This checklist must be 100% complete before any agent deployment. Missing items have caused production issues in previous releases.