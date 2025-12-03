from dataclasses import dataclass

from langgraph.graph.state import CompiledStateGraph
from langgraph.pregel import Pregel

from .founder_buddy.agent import graph as founder_buddy_agent
from schema import AgentInfo

DEFAULT_AGENT = "founder-buddy"

# Type alias to handle LangGraph's different agent patterns
# - @entrypoint functions return Pregel
# - StateGraph().compile() returns CompiledStateGraph
AgentGraph = CompiledStateGraph | Pregel


@dataclass
class Agent:
    description: str
    graph: AgentGraph


agents: dict[str, Agent] = {
    "founder-buddy": Agent(
        description="A Founder Buddy agent that helps entrepreneurs validate and refine their startup ideas through structured conversations about mission, idea, team traction, and investment plan",
        graph=founder_buddy_agent,
    ),
}


def get_agent(agent_id: str) -> AgentGraph:
    return agents[agent_id].graph


def get_all_agent_info() -> list[AgentInfo]:
    return [
        AgentInfo(key=agent_id, description=agent.description) for agent_id, agent in agents.items()
    ]
