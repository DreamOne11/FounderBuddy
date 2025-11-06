"""Generate business plan node for Founder Buddy Agent."""

import logging

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.runnables import RunnableConfig

from core.llm import get_model

from ..enums import SectionStatus
from ..models import FounderBuddyState

logger = logging.getLogger(__name__)


async def generate_business_plan_node(state: FounderBuddyState | dict, config: RunnableConfig) -> FounderBuddyState | dict:
    """
    Generate a comprehensive business plan document from all collected data.
    
    This node is called when all sections are complete to create a final summary document.
    """
    logger.info("Generating business plan document")
    
    # Handle both dict and FounderBuddyState types
    if isinstance(state, dict):
        messages = state.get("messages", [])
        founder_data = state.get("founder_data", {})
    else:
        messages = state.get("messages", [])
        founder_data = state.get("founder_data", {})
    
    # Extract conversation history as text
    conversation_text = ""
    for msg in messages:
        if isinstance(msg, HumanMessage):
            conversation_text += f"用户: {msg.content}\n\n"
        elif isinstance(msg, AIMessage):
            conversation_text += f"AI: {msg.content}\n\n"
    
    # Create business plan generation prompt
    system_prompt = """You are a professional business plan writer helping founders create a comprehensive business plan document.

Based on the complete conversation history, create a well-structured business plan document in Chinese that includes:

# 创业计划书

## 1. 执行摘要 (Executive Summary)
- 业务概念概述
- 核心价值主张
- 目标市场

## 2. 使命与愿景 (Mission & Vision)
- 使命陈述
- 愿景陈述
- 目标受众

## 3. 产品/服务描述 (Product/Service Description)
- 产品描述
- 核心价值主张
- 主要功能特性
- 差异化优势

## 4. 团队与进展 (Team & Traction)
- 团队成员及角色
- 关键里程碑
- 进展指标

## 5. 融资计划 (Investment Plan)
- 融资金额
- 资金用途
- 估值
- 退出策略

## 6. 下一步行动 (Next Steps)
- 立即行动项
- 关键里程碑

要求：
- 使用Markdown格式，结构清晰
- 内容全面但简洁，控制在2-3页
- 基于对话中的实际信息，不要使用占位符
- 使用专业但易懂的语言
- 确保所有信息都来自对话内容"""

    messages_for_llm = [
        SystemMessage(content=system_prompt),
        SystemMessage(content=f"""
完整对话历史：

{conversation_text}

请基于以上对话内容，生成一份完整的创业计划书。确保所有信息都来自对话中的实际内容。
""")
    ]
    
    # Generate business plan
    llm = get_model()
    response = await llm.ainvoke(messages_for_llm)
    
    business_plan_content = response.content if hasattr(response, 'content') else str(response)
    
    # Add business plan to state
    state["business_plan"] = business_plan_content
    
    # Create final message with business plan
    final_message = f"""# 🎉 创业计划书已生成

感谢您完成所有section！以下是基于您的对话生成的完整创业计划书：

---

{business_plan_content}

---

**下一步建议：**
1. 仔细审阅这份计划书
2. 根据实际情况进行调整和完善
3. 开始执行计划中的下一步行动

祝您的创业项目顺利！🚀"""
    
    # Add final message
    state["messages"].append(AIMessage(content=final_message))
    
    # Mark as finished
    state["finished"] = True
    
    logger.info("Business plan generated successfully")
    
    return state

