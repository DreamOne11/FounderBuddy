export async function GET() {
  try {
    const isLocal = process.env.NEXT_PUBLIC_API_ENV === 'local';
    const apiUrl = isLocal 
      ? process.env.VALUE_CANVAS_API_URL_LOCAL 
      : process.env.VALUE_CANVAS_API_URL_PRODUCTION;
    
    // Add timeout with AbortController
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 5000); // 5 second timeout
    
    const response = await fetch(`${apiUrl}/info`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        ...(process.env.VALUE_CANVAS_API_TOKEN && {
          'Authorization': `Bearer ${process.env.VALUE_CANVAS_API_TOKEN}`
        })
      },
      signal: controller.signal
    });
    
    clearTimeout(timeoutId);

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    
    // Filter to only return founder-buddy agent
    if (data.agents && Array.isArray(data.agents)) {
      data.agents = data.agents.filter((agent: { key: string }) => agent.key === 'founder-buddy');
    }
    
    return Response.json(data);
  } catch (error) {
    console.error('Failed to fetch agents:', error);
    
    // Fallback - only founder-buddy agent
    const fallbackAgents = {
      agents: [
        {
          key: 'founder-buddy',
          description: 'A Founder Buddy agent that helps entrepreneurs validate and refine their startup ideas through structured conversations about mission, idea, team traction, and investment plan'
        }
      ]
    };
    
    return Response.json(fallbackAgents);
  }
}

