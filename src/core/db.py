from supabase import Client, create_client

from core.settings import settings

# Supabase client with anonymous key (for general operations)
supabase: Client | None = None
if settings.SUPABASE_URL and settings.SUPABASE_ANON_KEY:
    supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_ANON_KEY.get_secret_value())

# Supabase client with service role key (for admin operations)
supabase_admin: Client | None = None
if settings.SUPABASE_URL and settings.SUPABASE_SERVICE_ROLE_KEY:
    supabase_admin = create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_ROLE_KEY.get_secret_value())

async def execute_context_query(sql_query: str) -> str:
    """
    Execute a SQL query and return the result as formatted context for system prompt.
    
    Args:
        sql_query: The SQL query to execute
        
    Returns:
        Formatted string containing the query results
    """
    if not supabase:
        return "# Context Data\n\nSupabase not configured - no context data available."
    
    try:
        response = supabase.rpc('exec_sql', {'query': sql_query}).execute()
        
        if response.data:
            # Format the results as markdown
            context = "# Context Data\n\n"
            if isinstance(response.data, list) and response.data:
                # Table format for multiple rows
                if len(response.data) > 0:
                    # Get column headers from first row
                    headers = list(response.data[0].keys())
                    context += "| " + " | ".join(headers) + " |\n"
                    context += "|" + "---|" * len(headers) + "\n"
                    
                    # Add data rows
                    for row in response.data[:10]:  # Limit to first 10 rows
                        values = [str(row.get(h, '')) for h in headers]
                        context += "| " + " | ".join(values) + " |\n"
                    
                    if len(response.data) > 10:
                        context += f"\n*Showing first 10 of {len(response.data)} rows*\n"
            else:
                context += str(response.data)
            
            return context
        else:
            return "# Context Data\n\nNo data returned from query."
            
    except Exception as e:
        return f"# Context Data\n\nError executing query: {str(e)}"


async def get_user_context(user_id: int) -> str:
    """
    Get comprehensive user context data for personalizing system prompts.
    
    Args:
        user_id: The UUID of the user to get context for
        
    Returns:
        Formatted string containing user profile and activity data
    """
    print(f"[DEBUG] get_user_context called with user_id: {user_id}")
    print(f"[DEBUG] supabase client available: {supabase is not None}")
    print(f"[DEBUG] supabase_admin client available: {supabase_admin is not None}")
    
    if not supabase_admin:
        print("[DEBUG] Supabase admin client not configured")
        return "## User Context\n\nSupabase admin client not configured - using default system prompt."
    
    try:
        print(f"[DEBUG] Calling get_user_complete_info RPC with user_id: {user_id} using admin client")
        
        # 使用 service role 客户端调用 RPC 函数（需要访问 auth.users 表）
        response = supabase_admin.rpc('get_user_complete_info', {'target_user_id': user_id}).execute()
        print(f"[DEBUG] RPC response type: {type(response)}")
        print(f"[DEBUG] RPC response data type: {type(response.data)}")
        print(f"[DEBUG] RPC response data: {response.data}")
        
        if response.data:
            user_data = response.data
            print(f"[DEBUG] User data keys: {list(user_data.keys()) if isinstance(user_data, dict) else 'Not a dict'}")
            return format_user_context(user_data)
        else:
            print("[DEBUG] No data returned from RPC call")
            return "## User Context\n\nUser not found or no data available - using default system prompt."
            
    except Exception as e:
        print(f"[DEBUG] Exception in get_user_context: {e}")
        return f"## User Context\n\nError retrieving user context: {str(e)} - using default system prompt."


def format_user_context(user_data: dict) -> str:
    """
    Format user data into a readable context for system prompts.
    
    Args:
        user_data: Dictionary containing complete user profile and activity data
        
    Returns:
        Formatted string for system prompt inclusion with all available data
    """
    if not user_data:
        return "## User Context\n\nNo user data available - using default system prompt."
    
    import json
    
    context = "## Complete User Context\n\n"
    context += "Below is the complete user profile and activity data. Use this information to provide highly personalized assistance.\n\n"
    
    # Format the entire user data as readable JSON
    try:
        # Pretty print the JSON with proper formatting
        formatted_json = json.dumps(user_data, indent=2, ensure_ascii=False, default=str)
        context += "```json\n"
        context += formatted_json
        context += "\n```\n\n"
    except Exception:
        # Fallback to string representation if JSON serialization fails
        context += f"```\n{str(user_data)}\n```\n\n"
    
    context += """
### Key Information Summary:
- **User**: {name}
- **Role**: {job_title} at {company_name}
- **Industry**: {industry}
- **Experience**: {experience_years} years
- **Career Goal**: {career_goal}
- **Location**: {location}

### Activity Statistics:
- **Challenges**: {challenges_completed}/{challenges_total} completed
- **Interview Attempts**: {attempts_total} total, Average score: {avg_score}
- **Courses**: {courses_enrolled} enrolled, {courses_purchased} purchased
- **Credits**: {credit_balance} balance

### Instructions:
Please provide highly personalized assistance based on this user's complete profile, skills, experience, goals, and activity history. 
Reference specific details from their background when relevant to make your responses more valuable and targeted.
""".format(
        name=user_data.get('profile', {}).get('name', 'N/A'),
        job_title=user_data.get('profile', {}).get('job_title', 'N/A'),
        company_name=user_data.get('profile', {}).get('company_name', 'N/A'),
        industry=user_data.get('profile', {}).get('industry', 'N/A'),
        experience_years=user_data.get('profile', {}).get('experience_years', 'N/A'),
        career_goal=user_data.get('profile', {}).get('career_goal', 'N/A'),
        location=user_data.get('profile', {}).get('location', 'N/A'),
        challenges_completed=user_data.get('stats', {}).get('challenges_completed', 0),
        challenges_total=user_data.get('stats', {}).get('challenges_total', 0),
        attempts_total=user_data.get('stats', {}).get('attempts_total', 0),
        avg_score=user_data.get('stats', {}).get('avg_score', 0),
        courses_enrolled=user_data.get('stats', {}).get('courses_enrolled', 0),
        courses_purchased=user_data.get('stats', {}).get('courses_purchased', 0),
        credit_balance=user_data.get('stats', {}).get('credit_balance', 0)
    )
    
    return context


"""
Usage Guide:

1. Use `supabase` (anonymous key) for:
   - Reading public data
   - Calling RPC functions that don't require elevated permissions
   - General operations that follow RLS (Row Level Security) policies

2. Use `supabase_admin` (service role key) for:
   - Admin operations that bypass RLS policies
   - Writing system data
   - Operations requiring elevated permissions
   - Bulk operations

3. Use `execute_context_query` for:
   - Getting context data for system prompts
   - Executing read-only queries for agent context

Example:
    from core.db import supabase, supabase_admin, execute_context_query
    
    # For general operations
    if supabase:
        response = supabase.rpc('get_system_prompt', {'p_name': 'rag_assistant_prompt'}).execute()
    
    # For admin operations
    if supabase_admin:
        response = supabase_admin.table('admin_logs').insert({'action': 'system_update'}).execute()
    
    # For context data in agents
    context = await execute_context_query("SELECT * FROM knowledge_base LIMIT 5")
"""
