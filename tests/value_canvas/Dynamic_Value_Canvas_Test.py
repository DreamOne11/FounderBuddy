#!/usr/bin/env python3
"""
Dynamic Value Canvas Agent Testing Framework
Creates an intelligent test agent that can read documentation and respond dynamically to the Value Canvas Agent
"""

import asyncio
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

# Load env vars
env_path = Path('.env')
if env_path.exists():
    with open(env_path) as f:
        for line in f:
            if line.strip() and not line.startswith('#') and '=' in line:
                key, value = line.strip().split('=', 1)
                os.environ.setdefault(key, value)

sys.path.append('src')

from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.runnables import RunnableConfig
from langchain_openai import ChatOpenAI

from agents.value_canvas.agent import graph as value_canvas_agent
from agents.value_canvas.agent import initialize_value_canvas_state


class IntelligentTestUser:
    """
    An intelligent test user that can read documentation and respond dynamically
    to the Value Canvas Agent based on expected flow patterns
    """
    
    def __init__(self):
        # Business scenario data
        self.business_data = {
            "name": "Sarah Chen",
            "preferred_name": "Sarah", 
            "company": "ScaleWise Consulting",
            "industry": "Technology & Software consulting, specifically B2B SaaS",
            "specialty": "helping SaaS founders systematically scale from startup to Series A funding stage",
            "achievement": "helping three different SaaS companies successfully raise their Series A, with one going from $500K to $3M ARR in 18 months",
            "outcomes": "systematic revenue growth strategies and Series A preparation guidance",
            "awards": "featured in TechCrunch and have spoken at three major SaaS conferences this year",
            "content": "write regularly on Medium about SaaS scaling and host monthly 'Scale Smart' webinars that get 500+ attendees",
            "skills": "MBA from Stanford and am a certified EOS implementer with 8 years of SaaS experience",
            "partners": "work closely with companies like Mixpanel and Intercom, and partner with Sequoia Capital for deal flow",
            
            # ICP data
            "icp_role": "CEO/Founder - hands-on founders who are still deeply involved in day-to-day operations but need systematic scaling approaches",
            "icp_demographics": "28-40 years old, running B2B SaaS companies with $500K-$2M ARR, team of 10-50 employees, technical background with strong product sense",
            "icp_geography": "US-based, concentrated in major tech hubs like SF Bay Area, NYC, Austin, and Seattle, plus select English-speaking international founders",
            "icp_nickname": "Growth-Stage SaaS Founder",
            
            # Pain points
            "pain1": {
                "symptom": "Revenue Plateau",
                "struggle": "hit a growth ceiling around $1-2M ARR and despite trying new tactics, marketing campaigns, and sales strategies, they can't break through to the next level",
                "cost": "burning through their runway faster than planned, team morale declining due to stagnant growth, and growing investor concerns about their Series A readiness",
                "consequence": "risk missing their Series A window entirely, running out of funding before achieving required growth metrics, and watching competitors pass them by in the market"
            },
            "pain2": {
                "symptom": "Operational Chaos", 
                "struggle": "everyone on the team is working extremely hard but in different directions, meetings are getting longer without clear decisions, and the founder has become a bottleneck for everything",
                "cost": "productivity actually decreases as the team grows, key people are starting to leave for 'better opportunities,' and critical projects keep stalling or getting deprioritized",
                "consequence": "lose their best talent to competitors, develop a culture of confusion and frustration, and the founder ends up working 80-hour weeks indefinitely without being able to scale themselves out"
            },
            "pain3": {
                "symptom": "Market Positioning Blur",
                "struggle": "struggle to clearly articulate what makes them different from competitors, sales calls take forever because prospects don't immediately 'get it,' and pricing becomes a constant negotiation rather than a value conversation",
                "cost": "sales cycles stretch to 4-6 months instead of 2-3 months, win rates drop to 15-20% vs. the industry standard of 35-40%, and they're competing primarily on price rather than value",
                "consequence": "become a commodity competing purely on price, margins become unsustainable, and they lose market share to better-positioned competitors who can charge premium pricing"
            },
            
            # Deep fear
            "deep_fear": "Am I actually capable of building and leading a company at this scale? What if I'm in over my head and everyone - my team, investors, customers - eventually figures out that I don't really know what I'm doing at this level?",
            
            # Payoffs
            "payoff1": {
                "objective": "Predictable Growth",
                "desire": "consistent month-over-month growth rates that they can actually forecast and plan around, creating predictable revenue they can count on",
                "without": "without requiring a complete team overhaul, expensive new technology implementations, or founder burnout from working unsustainable hours",
                "resolution": "finally break through that revenue plateau permanently and achieve the Series A-ready growth trajectory they need"
            },
            "payoff2": {
                "objective": "Operational Excellence",
                "desire": "a high-performing team where everyone knows their role, decisions get made efficiently, and productivity scales as they add more people",
                "without": "without micromanaging everything, hiring expensive consultants for every problem, or replacing their existing team members",
                "resolution": "transform the operational chaos into a well-oiled machine that actually gets stronger and more efficient as it grows"
            },
            "payoff3": {
                "objective": "Market Authority",
                "desire": "crystal clear market positioning where prospects immediately understand their unique value, sales cycles shorten dramatically, and they can charge premium pricing as the obvious choice",
                "without": "without spending years building brand recognition, massive marketing budgets, or completely rebuilding their product from scratch",
                "resolution": "become the market leader that prospects actively seek out, making referrals and word-of-mouth their primary growth engine"
            },
            
            # Method and other elements
            "method_name": "The SCALE Framework",
            "method_principles": "Strategic Foundation, Culture Alignment, Automation Systems, Leadership Development, Execution Excellence",
            "prize": "Series A Ready"
        }
        
        # Load documentation
        self.doc_content = self._load_documentation()
        
        # Initialize LLM for dynamic response generation
        self.llm = ChatOpenAI(
            model="gpt-5-mini",  # Use GPT-5-Mini for test user responses too
            max_tokens=1000
        )
        
        # Track conversation state
        self.current_section = None
        self.conversation_history = []
        self.flow_violations = []
        self.section_completions = {}
        
    def _load_documentation(self) -> str:
        """Load the Value Canvas documentation"""
        doc_path = Path("src/agents/value_canvas/docs/AI Agent [Value Canvas]-prompts-and-instructions.md")
        if doc_path.exists():
            return doc_path.read_text(encoding='utf-8')
        return ""
    
    async def generate_dynamic_response(self, agent_message: str, context: dict) -> tuple[str, dict]:
        """
        Generate a dynamic response based on what the agent is asking
        and the current flow expectations from documentation
        """
        
        # Analyze agent message to understand what they're asking for
        section_context = self._analyze_agent_message(agent_message)
        
        # Generate appropriate response
        prompt = f"""
You are Sarah Chen, a SaaS scaling consultant being interviewed for a Value Canvas creation.

DOCUMENTATION CONTEXT (what the agent should be doing):
{self._get_relevant_doc_section(section_context.get('section', 'unknown'))}

AGENT'S MESSAGE: {agent_message}

YOUR BUSINESS DATA: {json.dumps(self.business_data, indent=2)}

CONVERSATION CONTEXT:
- Current section: {context.get('current_section', 'unknown')}
- Previous responses: {self.conversation_history[-3:] if len(self.conversation_history) >= 3 else self.conversation_history}

INSTRUCTIONS:
1. Respond naturally as Sarah Chen would
2. Provide the information the agent is asking for based on your business data
3. If the agent asks for a rating (0-5), provide a rating between 3-5 (mostly positive)
4. If you notice the agent is not following the documented flow, still respond helpfully but note any issues
5. Keep responses conversational but informative
6. If asked for choices/selections, pick the most relevant option for your SaaS consulting business

Generate only your response as Sarah Chen (no meta-commentary):
"""
        
        response = await self.llm.ainvoke([HumanMessage(content=prompt)])
        user_response = response.content
        
        # Update conversation tracking
        self.conversation_history.append({
            "agent": agent_message,
            "user": user_response,
            "section": context.get('current_section'),
            "timestamp": datetime.now().isoformat()
        })
        
        # Validate flow compliance
        flow_analysis = self._validate_flow_compliance(agent_message, section_context)
        
        return user_response, flow_analysis
    
    def _analyze_agent_message(self, message: str) -> dict:
        """Analyze agent message to understand what section/info they're requesting"""
        
        # Pattern matching for different sections and questions
        patterns = {
            'name': r'(name|call you)',
            'company': r'(company|business)',
            'industry': r'(industry|sector|field)',
            'specialty': r'(specialty|expertise|zone of genius)',
            'achievement': r'(proud|achievement|accomplish)',
            'outcomes': r'(outcomes|results|come to you)',
            'awards': r'(award|media|feature)',
            'content': r'(content|publish|blog|podcast|book)',
            'skills': r'(skill|qualification|background)',
            'partners': r'(partner|brand|client)',
            'rating': r'(rating|score|rate|0-5|how)',
            'icp_role': r'(ideal client|target|customer role)',
            'pain': r'(pain|problem|frustration|struggle)',
            'fear': r'(fear|worry|doubt|concern)',
            'payoff': r'(payoff|benefit|want|desire)',
            'method': r'(method|framework|approach|process)',
            'mistake': r'(mistake|error|wrong)',
            'prize': r'(prize|outcome|transformation)'
        }
        
        detected_topics = []
        for topic, pattern in patterns.items():
            if re.search(pattern, message.lower()):
                detected_topics.append(topic)
        
        # Determine section based on patterns
        if any(topic in ['name', 'company', 'industry', 'specialty', 'achievement', 'outcomes', 'awards', 'content', 'skills', 'partners'] for topic in detected_topics):
            section = 'interview'
        elif 'icp' in detected_topics or 'ideal client' in message.lower():
            section = 'icp'
        elif 'pain' in detected_topics:
            section = 'pain'
        elif 'fear' in detected_topics:
            section = 'deep_fear'
        elif 'payoff' in detected_topics:
            section = 'payoffs'
        elif 'method' in detected_topics:
            section = 'signature_method'
        elif 'mistake' in detected_topics:
            section = 'mistakes'
        elif 'prize' in detected_topics:
            section = 'prize'
        else:
            section = 'unknown'
            
        return {
            'section': section,
            'topics': detected_topics,
            'asking_for_rating': 'rating' in detected_topics
        }
    
    def _get_relevant_doc_section(self, section: str) -> str:
        """Extract relevant documentation section"""
        section_markers = {
            'interview': '## 1st Interview',
            'icp': '# Ideal Customer (ICP)',
            'pain': '# The Pain',
            'deep_fear': '### Deep Fear',
            'payoffs': '# The Payoffs', 
            'signature_method': '# Signature Method',
            'mistakes': '# Mistakes',
            'prize': '# The Prize'
        }
        
        if section in section_markers:
            marker = section_markers[section]
            if marker in self.doc_content:
                # Extract section content (simplified)
                start_idx = self.doc_content.find(marker)
                # Find next major section or end
                next_sections = [self.doc_content.find(f'\n# {s}') for s in ['Ideal', 'The Pain', 'VALUE CANVAS:', 'Signature', 'Mistakes', 'The Prize'] if self.doc_content.find(f'\n# {s}') > start_idx]
                end_idx = min([idx for idx in next_sections if idx > start_idx], default=len(self.doc_content))
                return self.doc_content[start_idx:end_idx][:1500]  # Limit length
        
        return "No specific documentation found for this section"
    
    def _validate_flow_compliance(self, agent_message: str, context: dict) -> dict:
        """Validate if agent is following the documented flow"""
        violations = []
        
        # Check for expected patterns based on documentation
        expected_patterns = {
            'interview': [
                'name', 'company', 'industry', 'specialty', 'achievement',
                'outcomes', 'awards', 'content', 'skills', 'partners'
            ],
            'icp': ['role', 'demographics', 'geography', 'affinity', 'affordability', 'impact', 'access'],
            'pain': ['symptom', 'struggle', 'cost', 'consequence'],
            'payoffs': ['objective', 'desire', 'without', 'resolution']
        }
        
        # Additional validation logic can be added here
        
        return {
            'violations': violations,
            'section_compliance': len(violations) == 0,
            'expected_next': self._predict_next_question(context)
        }
    
    def _predict_next_question(self, context: dict) -> str:
        """Predict what the agent should ask next based on documentation flow"""
        section = context.get('section', 'unknown')
        
        predictions = {
            'interview': "Should ask for next interview question in sequence",
            'icp': "Should ask for ICP details or viability check",
            'pain': "Should ask for pain point details (symptom/struggle/cost/consequence)",
            'payoffs': "Should ask for payoff details mirroring pain points"
        }
        
        return predictions.get(section, "Unknown next step")


class DynamicValueCanvasTest:
    """
    Main test orchestrator that coordinates the conversation between
    the Value Canvas Agent and the Intelligent Test User
    """
    
    def __init__(self):
        self.user_id = "dynamic-test-sarah"
        self.thread_id = "dynamic-test-scalewise"
        self.state = None
        self.test_user = IntelligentTestUser()
        
        # Create log file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file = f"Dynamic_Value_Canvas_Test_Log_{timestamp}.md"
        
        # Initialize log
        with open(self.log_file, 'w', encoding='utf-8') as f:
            f.write("# Dynamic Value Canvas Agent Test Log\n\n")
            f.write("## Test Overview\n")
            f.write(f"**Start Time**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("**Test Type**: Dynamic interaction between Value Canvas Agent and Intelligent Test User\n")
            f.write("**Objective**: Validate agent follows documented flow with realistic dynamic responses\n\n")
            f.write("---\n\n")
        
        # Configure Value Canvas Agent - Use GPT-5-Mini for optimal speed/quality balance
        test_model = "gpt-5-mini"  # Latest fast model with GPT-5 capabilities
        print(f"🚀 Using GPT-5-Mini for optimal speed and quality: {test_model}")
            
        self.config = RunnableConfig(
            configurable={
                "thread_id": f"{self.user_id}-{self.thread_id}",
                "model": test_model
            }
        )
        
        print(f"🔧 Dynamic test initialized, log will be saved to: {self.log_file}")
    
    def log_interaction(self, round_num: int, user_input: str, agent_response: str, 
                       flow_analysis: dict, duration: float):
        """Log each interaction with flow analysis"""
        
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(f"## Round {round_num} - Dynamic Interaction\n\n")
            f.write(f"**Time**: {datetime.now().strftime('%H:%M:%S')} (Duration: {duration:.2f}s)\n\n")
            f.write(f"**👤 User (Sarah)**: {user_input}\n\n")
            f.write(f"**🤖 Value Canvas Agent**: {agent_response}\n\n")
            
            # Flow analysis
            f.write("### Flow Analysis\n")
            f.write(f"**Section Detected**: {flow_analysis.get('section_compliance', 'Unknown')}\n")
            if flow_analysis.get('violations'):
                f.write(f"**⚠️ Flow Violations**: {', '.join(flow_analysis['violations'])}\n")
            else:
                f.write("**✅ Flow Compliance**: Agent following expected pattern\n")
            f.write(f"**Expected Next**: {flow_analysis.get('expected_next', 'Unknown')}\n\n")
            
            f.write("---\n\n")
    
    async def run_dynamic_conversation(self, max_rounds: int = 50):
        """Run a dynamic conversation between the agents"""
        
        print("🎭 Starting Dynamic Value Canvas Agent Test")
        print("="*80)
        
        # Initialize conversation
        if self.state is None:
            print("🔄 Initializing Value Canvas Agent state...")
            self.state = await initialize_value_canvas_state(self.user_id, self.thread_id)
        
        # Start conversation
        round_num = 1
        current_message = "Hi! I'm Sarah Chen and I'd like to create my Value Canvas. Let's build this together!"
        
        try:
            while round_num <= max_rounds:
                print(f"\n⏳ Round {round_num} - Dynamic Conversation")
                print(f"📤 User: {current_message}")
                
                start_time = datetime.now()
                
                # Send message to Value Canvas Agent
                self.state["messages"].append(HumanMessage(content=current_message))
                
                print("🤖 Value Canvas Agent processing...")
                result = await value_canvas_agent.ainvoke(self.state, config=self.config)
                self.state = result
                
                if result["messages"] and isinstance(result["messages"][-1], AIMessage):
                    agent_response = result["messages"][-1].content
                else:
                    agent_response = "❌ No response from agent"
                    break
                
                print(f"📥 Agent: {agent_response[:100]}..." if len(agent_response) > 100 else f"📥 Agent: {agent_response}")
                
                # Generate dynamic user response
                print("🧠 Generating dynamic user response...")
                context = {
                    'current_section': self.state.get('current_section'),
                    'round': round_num
                }
                
                user_response, flow_analysis = await self.test_user.generate_dynamic_response(
                    agent_response, context
                )
                
                end_time = datetime.now()
                duration = (end_time - start_time).total_seconds()
                
                print(f"📤 Dynamic Response: {user_response}")
                print(f"✅ Round {round_num} Complete (Duration: {duration:.2f}s)")
                
                # Log interaction
                self.log_interaction(round_num, current_message, agent_response, flow_analysis, duration)
                
                # Check for completion signals
                if self._is_conversation_complete(agent_response, user_response):
                    print("\n🎉 Conversation completed successfully!")
                    break
                
                # Set up next round
                current_message = user_response
                round_num += 1
                
                # Small delay to avoid rate limits
                await asyncio.sleep(1)
            
            # Final summary
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write("\n## 🎉 Dynamic Test Complete\n\n")
                f.write(f"**End Time**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"**Total Rounds**: {round_num - 1}\n")
                f.write(f"**Flow Violations**: {len(self.test_user.flow_violations)}\n")
                f.write(f"**Test Status**: {'✅ Success' if round_num <= max_rounds else '⚠️ Max rounds reached'}\n")
        
        except Exception as e:
            print(f"\n❌ Test error at round {round_num}: {e}")
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write("\n## ❌ Test Error\n")
                f.write(f"**Round**: {round_num}\n")
                f.write(f"**Error**: {str(e)}\n")
    
    def _is_conversation_complete(self, agent_response: str, user_response: str) -> bool:
        """Check if the conversation has reached a natural completion"""
        completion_signals = [
            "complete value canvas",
            "implementation",
            "ready to test",
            "all sections complete",
            "canvas is ready"
        ]
        
        combined_text = (agent_response + " " + user_response).lower()
        return any(signal in combined_text for signal in completion_signals)


async def main():
    """Main test execution"""
    test = DynamicValueCanvasTest()
    await test.run_dynamic_conversation(max_rounds=50)


if __name__ == '__main__':
    asyncio.run(main())