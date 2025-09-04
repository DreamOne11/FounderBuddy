"""Memory updater node for Signature Pitch Agent."""

import logging

from langchain_core.messages import AIMessage, SystemMessage
from langchain_core.runnables import RunnableConfig

from core.llm import get_model

from ..models import (
    RouterDirective,
    SectionContent,
    SectionState,
    SectionStatus,
    SignaturePitchSectionID,
    SignaturePitchState,
    TiptapDocument,
    TiptapParagraphNode,
    TiptapTextNode,
)
from ..tools import (
    create_tiptap_content,
    extract_plain_text,
    save_section,
)

logger = logging.getLogger(__name__)


def convert_bullet_list_to_paragraphs(tiptap_content: dict) -> dict:
    """
    Convert Tiptap bulletList structures to paragraph format for model validation.
    
    Args:
        tiptap_content: Tiptap JSON content that may contain bulletList structures
        
    Returns:
        Tiptap JSON content with bulletList converted to paragraphs
    """
    if not isinstance(tiptap_content, dict):
        return tiptap_content
    
    def extract_text_from_node(node: dict) -> str:
        """Recursively extract text from any Tiptap node."""
        if not isinstance(node, dict):
            return ""
        
        if node.get("type") == "text":
            return node.get("text", "")
        
        text_parts = []
        if "content" in node and isinstance(node["content"], list):
            for child in node["content"]:
                text_parts.append(extract_text_from_node(child))
        
        return "".join(text_parts)
    
    # Create a copy to avoid modifying the original
    converted_content = {"type": "doc", "content": []}
    
    if "content" in tiptap_content and isinstance(tiptap_content["content"], list):
        for item in tiptap_content["content"]:
            if isinstance(item, dict):
                if item.get("type") == "bulletList":
                    # Convert bulletList to paragraphs
                    if "content" in item and isinstance(item["content"], list):
                        for list_item in item["content"]:
                            if isinstance(list_item, dict) and list_item.get("type") == "listItem":
                                # Extract all text from the list item
                                text = extract_text_from_node(list_item).strip()
                                if text:
                                    # Create a paragraph with bullet point
                                    paragraph = {
                                        "type": "paragraph",
                                        "content": [{
                                            "type": "text",
                                            "text": f"• {text}"
                                        }]
                                    }
                                    converted_content["content"].append(paragraph)
                elif item.get("type") == "paragraph":
                    # Keep paragraphs as-is but ensure proper structure
                    paragraph = {
                        "type": "paragraph",
                        "content": []
                    }
                    
                    if "content" in item and isinstance(item["content"], list):
                        for content_item in item["content"]:
                            if isinstance(content_item, dict) and content_item.get("type") == "text":
                                paragraph["content"].append({
                                    "type": "text",
                                    "text": content_item.get("text", "")
                                })
                            elif isinstance(content_item, dict) and content_item.get("type") == "hardBreak":
                                paragraph["content"].append({
                                    "type": "hardBreak"
                                })
                    
                    converted_content["content"].append(paragraph)
                else:
                    # For other types, try to extract text and convert to paragraph
                    text = extract_text_from_node(item).strip()
                    if text:
                        paragraph = {
                            "type": "paragraph",
                            "content": [{
                                "type": "text",
                                "text": text
                            }]
                        }
                        converted_content["content"].append(paragraph)
    
    return converted_content


async def memory_updater_node(
    state: SignaturePitchState, config: RunnableConfig
) -> SignaturePitchState:
    """
    Memory updater node that persists section states and updates canvas data.
    Enhanced with sophisticated two-branch logic from Value Canvas.
    """
    logger.info("=== DATABASE_DEBUG: memory_updater_node() ENTRY ===")
    logger.info("DATABASE_DEBUG: Memory updater node processing agent output")

    agent_out = state.get("agent_output")
    logger.debug(f"DATABASE_DEBUG: Agent output exists: {bool(agent_out)}")
    if agent_out:
        logger.debug(
            f"DATABASE_DEBUG: Agent output - section_update: {bool(agent_out.section_update)}, is_satisfied: {agent_out.is_satisfied}, router_directive: {agent_out.router_directive}"
        )

    # [DIAGNOSTIC] Log state before update
    logger.info(f"DATABASE_DEBUG: section_states BEFORE update: {state.get('section_states', {})}")
    logger.debug(f"DATABASE_DEBUG: Current section: {state.get('current_section')}")
    context_packet = state.get("context_packet")
    logger.debug(
        f"DATABASE_DEBUG: Context packet section: {context_packet.section_id if context_packet else None}"
    )

    # Decide status based on satisfaction and directive
    def _status_from_output(is_satisfied, directive):
        """Return status *string* to align with get_next_unfinished_section() logic."""
        if directive == RouterDirective.NEXT:
            return SectionStatus.DONE.value  # "done"
        if is_satisfied is not None and is_satisfied:
            return SectionStatus.DONE.value
        return SectionStatus.IN_PROGRESS.value

    # [SAVE_SECTION_DEBUG] Track decision path in memory_updater_node
    logger.info("SAVE_SECTION_DEBUG: memory_updater_node decision analysis:")
    logger.info(f"SAVE_SECTION_DEBUG: - agent_out exists: {bool(agent_out)}")
    if agent_out:
        logger.info(
            f"SAVE_SECTION_DEBUG: - agent_out.section_update exists: {bool(agent_out.section_update)}"
        )
        logger.info(f"SAVE_SECTION_DEBUG: - agent_out.is_satisfied: {agent_out.is_satisfied}")
        logger.info(
            f"SAVE_SECTION_DEBUG: - agent_out.router_directive: {agent_out.router_directive}"
        )
    else:
        logger.info("SAVE_SECTION_DEBUG: - No agent_out, will not call save_section")

    if agent_out and agent_out.section_update:
        # BRANCH 1: Process section_update (when LLM provides structured content)
        section_id = state["current_section"].value
        logger.info(
            f"SAVE_SECTION_DEBUG: ✅ ENTERING BRANCH 1: Processing section_update for section {section_id}"
        )
        logger.info(f"DATABASE_DEBUG: Processing section_update for section {section_id}")
        logger.debug(
            f"DATABASE_DEBUG: Section update content type: {type(agent_out.section_update)}"
        )

        # DEBUG: Log what content is being saved to which section
        logger.warning(f"CONTENT_DEBUG: About to save content to section {section_id}")
        if isinstance(agent_out.section_update, dict) and "content" in agent_out.section_update:
            content_dict = agent_out.section_update["content"]
            if isinstance(content_dict, dict) and "content" in content_dict:
                # Try to extract first paragraph text for debugging
                try:
                    first_para = content_dict["content"][0]
                    if isinstance(first_para, dict) and "content" in first_para:
                        first_text = first_para["content"][0].get("text", "No text")
                        logger.warning(
                            f"CONTENT_DEBUG: First paragraph starts with: {first_text[:100]}..."
                        )
                except Exception:
                    logger.warning("CONTENT_DEBUG: Could not extract content preview")

        # Save to database using save_section tool (make non-blocking for DB issues)
        logger.info("SAVE_SECTION_DEBUG: ✅ CALLING save_section with structured content")
        logger.debug("DATABASE_DEBUG: Calling save_section tool with structured content")

        # [CRITICAL DEBUG] Log the exact parameters being passed to save_section
        computed_status = _status_from_output(agent_out.is_satisfied, agent_out.router_directive)
        logger.info("SAVE_SECTION_DEBUG: About to call save_section with:")
        logger.info(f"SAVE_SECTION_DEBUG: - user_id: {state['user_id']}")
        logger.info(f"SAVE_SECTION_DEBUG: - thread_id: {state['thread_id']}")
        logger.info(f"SAVE_SECTION_DEBUG: - section_id: {section_id}")
        logger.info(
            f"SAVE_SECTION_DEBUG: - is_satisfied: {agent_out.is_satisfied} (type: {type(agent_out.is_satisfied)})"
        )
        logger.info(
            f"SAVE_SECTION_DEBUG: - status: {computed_status} (type: {type(computed_status)})"
        )
        logger.info(
            f"SAVE_SECTION_DEBUG: - router_directive was: {agent_out.router_directive} (type: {type(agent_out.router_directive)})"
        )

        try:
            save_result = await save_section.ainvoke(
                {
                    "user_id": state["user_id"],
                    "thread_id": state["thread_id"],
                    "section_id": section_id,
                    "content": agent_out.section_update["content"]
                    if isinstance(agent_out.section_update, dict)
                    else agent_out.section_update,
                    "satisfaction_feedback": agent_out.user_satisfaction_feedback,
                    "status": computed_status,
                }
            )
            logger.debug(f"DATABASE_DEBUG: save_section returned: {bool(save_result)}")
        except Exception as e:
            logger.warning(
                f"DATABASE_DEBUG: save_section failed (expected if DB not configured): {e}"
            )
            # Continue with local state management even if database save fails

        # Update local state (this is critical for proper functioning)
        logger.debug("DATABASE_DEBUG: Updating local section_states with new content")
        # Parse the section_update content properly
        if isinstance(agent_out.section_update, dict) and "content" in agent_out.section_update:
            # Convert bullet lists to paragraphs before validation
            converted_content = convert_bullet_list_to_paragraphs(agent_out.section_update["content"])
            try:
                tiptap_doc = TiptapDocument.model_validate(converted_content)
            except Exception as e:
                logger.warning(f"Failed to validate converted content: {e}")
                logger.debug(f"Converted content: {converted_content}")
                # Fallback to basic paragraph structure
                tiptap_doc = TiptapDocument(
                    type="doc", 
                    content=[TiptapParagraphNode(
                        type="paragraph",
                        content=[TiptapTextNode(
                            type="text",
                            text="Content validation failed - please regenerate summary"
                        )]
                    )]
                )
        else:
            logger.error(
                f"SAVE_SECTION_DEBUG: Invalid section_update structure: {type(agent_out.section_update)}"
            )
            tiptap_doc = TiptapDocument(type="doc", content=[])

        state["section_states"][section_id] = SectionState(
            section_id=SignaturePitchSectionID(section_id),
            content=SectionContent(
                content=tiptap_doc,
                plain_text=None,  # Will be filled later if needed
            ),
            satisfaction_feedback=agent_out.user_satisfaction_feedback,
            status=_status_from_output(agent_out.is_satisfied, agent_out.router_directive),
        )
        logger.info(
            f"SAVE_SECTION_DEBUG: ✅ BRANCH 1 COMPLETED: Section {section_id} saved with structured content"
        )

        # Extract structured data and update canvas_data using LLM
        try:
            await extract_and_update_canvas_data(state, section_id, agent_out.section_update)
        except Exception as e:
            logger.warning(f"DATABASE_DEBUG: Failed to extract structured data (non-critical): {e}")

        logger.info(f"DATABASE_DEBUG: ✅ Section {section_id} updated with structured content")

        # Reset consecutive stays counter since we made progress
        state["consecutive_stays"] = 0

    # Handle cases where agent provides score/status but no structured section_update
    elif agent_out:
        # BRANCH 2: Process agent output without section_update (when LLM provides score but no content)
        logger.info(
            "SAVE_SECTION_DEBUG: ✅ ENTERING BRANCH 2: Processing agent output without section_update"
        )
        logger.info(
            "DATABASE_DEBUG: Processing agent output without section_update (likely score/status only)"
        )

        if state.get("context_packet"):
            score_section_id = state["context_packet"].section_id.value
            logger.debug(
                f"DATABASE_DEBUG: Processing score/status update for section {score_section_id}"
            )

            # Only proceed if there's satisfaction feedback to save.
            if agent_out.is_satisfied is None:
                logger.info(
                    f"DATABASE_DEBUG: No satisfaction data or section_update for {score_section_id}, skipping save."
                )
                return state

            # We have satisfaction data, so we MUST save. We need to find the content.
            content_to_save = None

            # 1. Try to find content in the current state for the section
            if (
                score_section_id in state.get("section_states", {})
                and state["section_states"][score_section_id].content
            ):
                logger.info(
                    f"SAVE_SECTION_DEBUG: Found content for section {score_section_id} in state."
                )
                # The content in state should now be the correct Tiptap document
                content_to_save = state["section_states"][
                    score_section_id
                ].content.content.model_dump()

            # 2. If not in state, recover from previous message history with improved logic
            if not content_to_save:
                logger.warning(
                    f"SAVE_SECTION_DEBUG: Content for {score_section_id} not in state, recovering from history."
                )
                messages = state.get("messages", [])
                summary_text = None
                # Search backwards through the message history to find the last summary message.
                for msg in reversed(messages):
                    if isinstance(msg, AIMessage):
                        # A summary message typically contains these keywords.
                        content_lower = msg.content.lower()
                        if "summary" in content_lower and (
                            "satisfied" in content_lower or "rate 0-5" in content_lower
                        ):
                            summary_text = msg.content
                            logger.info(
                                "SAVE_SECTION_DEBUG: Found candidate summary message in history."
                            )
                            break

                if summary_text:
                    logger.info(
                        "SAVE_SECTION_DEBUG: Recovered summary text, converting to Tiptap format."
                    )
                    try:
                        content_to_save = await create_tiptap_content.ainvoke(
                            {"text": summary_text}
                        )
                    except Exception as e:
                        logger.error(
                            f"SAVE_SECTION_DEBUG: Failed to convert summary to Tiptap: {e}"
                        )
                else:
                    logger.error(
                        f"SAVE_SECTION_DEBUG: Could not recover summary from message history for {score_section_id}."
                    )

            # 3. If we found content (either from state or recovery), proceed with saving.
            if content_to_save:
                computed_status = _status_from_output(
                    agent_out.is_satisfied, agent_out.router_directive
                )
                logger.info(
                    f"SAVE_SECTION_DEBUG: ✅ Calling save_section for {score_section_id} with satisfaction and content."
                )

                try:
                    await save_section.ainvoke(
                        {
                            "user_id": state["user_id"],
                            "thread_id": state["thread_id"],
                            "section_id": score_section_id,
                            "content": content_to_save,
                            "satisfaction_feedback": agent_out.user_satisfaction_feedback,
                            "status": computed_status,
                        }
                    )
                except Exception as e:
                    logger.warning(
                        f"DATABASE_DEBUG: save_section failed (expected if DB not configured): {e}"
                    )

                # Update local state consistently, whether it existed before or not.
                # Convert content_to_save to TiptapDocument
                if isinstance(content_to_save, dict):
                    # Convert bullet lists to paragraphs before validation
                    converted_content = convert_bullet_list_to_paragraphs(content_to_save)
                    try:
                        tiptap_doc = TiptapDocument.model_validate(converted_content)
                    except Exception as e:
                        logger.warning(f"Failed to validate converted content: {e}")
                        logger.debug(f"Converted content: {converted_content}")
                        # Fallback to basic paragraph structure
                        tiptap_doc = TiptapDocument(
                            type="doc", 
                            content=[TiptapParagraphNode(
                                type="paragraph",
                                content=[TiptapTextNode(
                                    type="text",
                                    text="Content validation failed - please regenerate summary"
                                )]
                            )]
                        )
                else:
                    tiptap_doc = content_to_save

                state.setdefault("section_states", {})[score_section_id] = SectionState(
                    section_id=SignaturePitchSectionID(score_section_id),
                    content=SectionContent(content=tiptap_doc, plain_text=None),
                    satisfaction_feedback=agent_out.user_satisfaction_feedback,
                    status=computed_status,
                )
                logger.info(
                    f"DATABASE_DEBUG: ✅ Updated/created section state for {score_section_id} with satisfaction {agent_out.is_satisfied}"
                )
            else:
                # 4. If content recovery failed, we must not call save_section with empty content.
                logger.error(
                    f"DATABASE_DEBUG: ❌ CRITICAL: Aborting save for section {score_section_id} due to missing content."
                )

        else:
            logger.warning(
                "DATABASE_DEBUG: ⚠️ Cannot update section state as context_packet is missing"
            )

    else:
        # No agent output at all - safety mechanism for stuck states
        logger.info("SAVE_SECTION_DEBUG: ❌ No agent_out - applying safety mechanism")

        # Safety mechanism: if we're stuck in stay mode without progress, force next
        if state.get("router_directive") == "stay":
            consecutive_stays = state.get("consecutive_stays", 0) + 1
            state["consecutive_stays"] = consecutive_stays

            if consecutive_stays >= 3:  # After 3 stays without progress, force next
                logger.warning(
                    "Memory updater node - Forcing next due to no progress after multiple stays"
                )
                state["router_directive"] = "next"
                state["consecutive_stays"] = 0

    # [SAVE_SECTION_DEBUG] Final decision summary
    if not agent_out:
        logger.info(
            "SAVE_SECTION_DEBUG: ❌ FINAL RESULT: No agent_out - save_section was NEVER called"
        )
    elif agent_out.section_update:
        logger.info(
            "SAVE_SECTION_DEBUG: ✅ FINAL RESULT: Had section_update - save_section was called in BRANCH 1"
        )
    elif agent_out:
        logger.info(
            "SAVE_SECTION_DEBUG: ✅ FINAL RESULT: Had agent_out but no section_update - save_section was called in BRANCH 2 (if conditions met)"
        )
    else:
        logger.info(
            "SAVE_SECTION_DEBUG: ❌ FINAL RESULT: Unknown state - save_section may not have been called"
        )

    # [DIAGNOSTIC] Log state after update
    logger.info(f"DATABASE_DEBUG: section_states AFTER update: {state.get('section_states', {})}")
    logger.info("=== DATABASE_DEBUG: memory_updater_node() EXIT ===")

    return state


async def extract_and_update_canvas_data(
    state: SignaturePitchState, section_id: str, section_update: dict
) -> None:
    """Extract structured data from section content and update canvas_data."""
    logger.info(f"Extracting structured data for section: {section_id}")

    # Get plain text from tiptap content
    plain_text = await extract_plain_text.ainvoke(section_update["content"])

    # Extract data based on section type
    llm = get_model()

    try:
        # Import section-specific data models
        from ..capstone_sections import (
            AuthorityData,
            ClarityData,
            EssenceData,
            NextStepsData,
            OpportunityData,
            ProblemData,
            SolutionData,
            TheWhyData,
        )

        if section_id == SignaturePitchSectionID.CLARITY.value:
            structured_llm = llm.with_structured_output(ClarityData)
            extracted_data = await structured_llm.ainvoke(
                [
                    SystemMessage(
                        content=f"Extract clarity data from this content: {plain_text}"
                    )
                ]
            )

            # Update canvas_data dict with extracted fields
            canvas_data = state["canvas_data"]
            if extracted_data.name:
                canvas_data["name"] = extracted_data.name
            if extracted_data.same:
                canvas_data["same"] = extracted_data.same
            if extracted_data.fame:
                canvas_data["fame"] = extracted_data.fame

        elif section_id == SignaturePitchSectionID.AUTHORITY.value:
            structured_llm = llm.with_structured_output(AuthorityData)
            extracted_data = await structured_llm.ainvoke(
                [
                    SystemMessage(
                        content=f"Extract authority data from this content: {plain_text}"
                    )
                ]
            )

            canvas_data = state["canvas_data"]
            if extracted_data.experience:
                canvas_data["experience"] = extracted_data.experience
            if extracted_data.associations:
                canvas_data["associations"] = extracted_data.associations
            if extracted_data.accolades:
                canvas_data["accolades"] = extracted_data.accolades
            if extracted_data.results:
                canvas_data["results"] = extracted_data.results
            if extracted_data.authority_pillars:
                canvas_data["authority_pillars"] = extracted_data.authority_pillars

        elif section_id == SignaturePitchSectionID.PROBLEM.value:
            structured_llm = llm.with_structured_output(ProblemData)
            extracted_data = await structured_llm.ainvoke(
                [
                    SystemMessage(
                        content=f"Extract problem data from this content: {plain_text}"
                    )
                ]
            )

            canvas_data = state["canvas_data"]
            if extracted_data.context:
                canvas_data["context"] = extracted_data.context
            if extracted_data.dominant_problems:
                canvas_data["dominant_problems"] = extracted_data.dominant_problems

        elif section_id == SignaturePitchSectionID.SOLUTION.value:
            structured_llm = llm.with_structured_output(SolutionData)
            extracted_data = await structured_llm.ainvoke(
                [
                    SystemMessage(
                        content=f"Extract solution data from this content: {plain_text}"
                    )
                ]
            )

            canvas_data = state["canvas_data"]
            if extracted_data.focus:
                canvas_data["focus"] = extracted_data.focus
            if extracted_data.payoffs:
                canvas_data["payoffs"] = extracted_data.payoffs
            if extracted_data.what_how:
                canvas_data["what_how"] = extracted_data.what_how
            if extracted_data.prize:
                canvas_data["prize"] = extracted_data.prize

        elif section_id == SignaturePitchSectionID.THE_WHY.value:
            structured_llm = llm.with_structured_output(TheWhyData)
            extracted_data = await structured_llm.ainvoke(
                [SystemMessage(content=f"Extract why data from this content: {plain_text}")]
            )

            canvas_data = state["canvas_data"]
            if extracted_data.origin:
                canvas_data["origin"] = extracted_data.origin
            if extracted_data.mission:
                canvas_data["mission"] = extracted_data.mission
            if extracted_data.vision:
                canvas_data["vision"] = extracted_data.vision

        elif section_id == SignaturePitchSectionID.OPPORTUNITY.value:
            structured_llm = llm.with_structured_output(OpportunityData)
            extracted_data = await structured_llm.ainvoke(
                [
                    SystemMessage(
                        content=f"Extract opportunity data from this content: {plain_text}"
                    )
                ]
            )

            canvas_data = state["canvas_data"]
            if extracted_data.proposal:
                canvas_data["proposal"] = extracted_data.proposal
            if extracted_data.wedding:
                canvas_data["wedding"] = extracted_data.wedding
            if extracted_data.honeymoon:
                canvas_data["honeymoon"] = extracted_data.honeymoon

        elif section_id == SignaturePitchSectionID.NEXT_STEPS.value:
            structured_llm = llm.with_structured_output(NextStepsData)
            extracted_data = await structured_llm.ainvoke(
                [
                    SystemMessage(
                        content=f"Extract next steps data from this content: {plain_text}"
                    )
                ]
            )

            canvas_data = state["canvas_data"]
            if extracted_data.call_to_action:
                canvas_data["call_to_action"] = extracted_data.call_to_action

        elif section_id == SignaturePitchSectionID.ESSENCE.value:
            structured_llm = llm.with_structured_output(EssenceData)
            extracted_data = await structured_llm.ainvoke(
                [
                    SystemMessage(
                        content=f"Extract essence data from this content: {plain_text}"
                    )
                ]
            )

            canvas_data = state["canvas_data"]
            if extracted_data.reputation:
                canvas_data["reputation"] = extracted_data.reputation
            if extracted_data.feeling:
                canvas_data["feeling"] = extracted_data.feeling

        logger.info(f"Successfully extracted and updated canvas data for section: {section_id}")

    except Exception as e:
        logger.warning(f"Failed to extract structured data for section {section_id}: {e}")
        # Continue without structured extraction - the content is still saved
