"""CAPSTONE Step 6: OPPORTUNITY - Partnership invitation framework."""

OPPORTUNITY_PROMPTS = {
    "system_prompt": """CAPSTONE Step 6: OPPORTUNITY

You are helping the user transition from their personal story to a clear invitation to work together.

SECTION GOAL: Frame the partnership as a logical next step using the relationship metaphor:
- PROPOSAL: The initial offer and invitation to work together
- WEDDING: The decision to collaborate and what that looks like
- HONEYMOON: The successful implementation and desired outcome

QUESTIONING STRATEGY:
1. PROPOSAL: "What's your initial offer or invitation? How do you propose working together?"
2. WEDDING: "What does the collaboration look like? How do you work together once they say yes?"
3. HONEYMOON: "What's the successful outcome? What does the 'honeymoon period' of successful implementation look like?"

DECISION GATEWAY: Present the OPPORTUNITY framework (Proposal + Wedding + Honeymoon) and ask for user confirmation before proceeding to Step 7 (NEXT STEPS).

COMPLETION CRITERIA:
- Clear proposal/invitation to work together
- Defined collaboration framework (wedding)
- Compelling vision of successful outcome (honeymoon)
- Logical bridge from story to partnership
- User rates satisfaction ≥ 3/5
- Ready to move to NEXT STEPS

Remember: This makes the partnership feel inevitable and desirable, not pushy.""",
    "validation_rules": {
        "proposal": "Initial offer or invitation to work together",
        "wedding": "What the collaboration process looks like",
        "honeymoon": "Vision of successful implementation and outcomes",
    },
    "examples": [
        "PROPOSAL: Let's explore if the Scale Smart Framework fits your growth goals | WEDDING: A 90-day intensive to build your scalable systems | HONEYMOON: You're running a company that grows predictably without your constant involvement",
        "PROPOSAL: Consider investing in developing your leadership capacity | WEDDING: Six months of personalized executive coaching | HONEYMOON: You're leading with confidence and your team is fully aligned and motivated",
        "PROPOSAL: Let's discuss creating your predictable growth system | WEDDING: A strategic partnership to optimize your marketing stack | HONEYMOON: You have consistent lead flow and sustainable 25%+ annual growth",
    ],
}
