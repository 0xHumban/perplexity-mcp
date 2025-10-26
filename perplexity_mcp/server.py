from mcp.server.fastmcp import FastMCP
import os
from openai import OpenAI

DEFAULT_MODEL_RESEARCH = "sonar"
DEFAULT_MODEL_REASONING = "sonar-reasoning"

PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")


client = OpenAI(
    api_key=PERPLEXITY_API_KEY,
    base_url="https://api.perplexity.ai"
)

mcp = FastMCP("perplexity-mcp")


"""
Helper function to get perplexity response
Args:
    prompt: The prompt/question to send
    model: Sonar model (sonar, sonar-pro, sonar-deep-research, 
           sonar-reasoning, sonar-reasoning-pro)
    prePromptInput: Preprompt input to include in the prompt sent to Perplexity
    prePromptOutput: Preprompt output to include in the prompt return to copilot
Returns:
    The response from Perplexity with citations if available
"""
def get_perplexity_response(prompt: str, model: str, prePromptInput: str = "", prePromptOutput: str = "") -> str:
    response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": f"{prePromptInput}\n\n{prompt}"
                }
            ]
        )
        
    answer = response.choices[0].message.content
        
    # Add citations if available
    citations = ""
    if hasattr(response, 'citations') and response.citations:
        citations = "\n\n**Sources:**\n"
        for i, citation in enumerate(response.citations[:5], 1):
            citations += f"{i}. {citation}\n"



    return f"{prePromptOutput}\n\n{answer}{citations}"

@mcp.tool()
async def get_examples() -> str:
    """
    Get examples of prompts and usage patterns for this Perplexity MCP server.
    
    This tool helps you discover what you can do with this server and provides
    concrete examples of effective prompts for each tool.
    
    Returns:
        Detailed examples and usage guide for all available tools
    """
    examples = {
        "title": "🔍 Perplexity MCP Server - Usage Examples",
        "description": "This server provides AI-powered search and reasoning capabilities via Perplexity's Sonar models.",
        "tools": [
            {
                "name": "ask_perplexity",
                "purpose": "General research and web searches with internet access",
                "when_to_use": "For factual questions, current events, research, comparisons",
                "examples": [
                    "What are the latest developments in quantum computing in 2025?",
                    "Compare Python vs Rust for web development",
                    "What's the current weather in Paris?",
                    "Explain the recent changes in EU privacy laws",
                    "Find the best practices for React Server Components"
                ],
                "model_recommendation": "Use 'sonar' (default) for quick research"
            },
            {
                "name": "ask_perplexity_exact_response",
                "purpose": "Get unmodified responses from Perplexity without additional formatting",
                "when_to_use": "When you need the raw output without any processing",
                "examples": [
                    "Give me the exact documentation for FastAPI's dependency injection",
                    "What does the official Next.js docs say about App Router?",
                    "Show me the raw API response format for OpenAI's latest models"
                ],
                "model_recommendation": "Use 'sonar' for standard queries, 'sonar-reasoning' for complex analysis"
            },
            {
                "name": "ask_perplexity_for_instructions",
                "purpose": "Get step-by-step instructions that Copilot can execute in agent mode",
                "when_to_use": "For complex tasks requiring multiple steps or actions",
                "examples": [
                    "How do I set up a Python FastAPI project with Docker?",
                    "Create a React app with TypeScript and Tailwind CSS",
                    "Set up CI/CD pipeline for a Node.js application",
                    "Configure a PostgreSQL database with Redis caching"
                ],
                "model_recommendation": "Uses 'sonar-reasoning' (default) for detailed step-by-step guidance"
            },
            {
                "name": "ask_perplexity_to_learn",
                "purpose": "Learn complex concepts with pedagogical explanations, examples, and analogies",
                "when_to_use": "When you want to understand and learn something new",
                "examples": [
                    "Explain how async/await works in Python",
                    "Teach me about Docker containers and why they're useful",
                    "What are React hooks and how do I use them?",
                    "Explain database indexing with practical examples",
                    "How does JWT authentication work?"
                ],
                "model_recommendation": "Uses 'sonar-reasoning' (default) for comprehensive teaching approach"
            }
        ],
        "tips": [
            "💡 Be specific in your prompts for better results",
            "🎯 Mention context (programming language, framework, version) when relevant",
            "🔄 Use 'ask_perplexity_to_learn' when you want to understand concepts deeply",
            "⚡ Use 'ask_perplexity_for_instructions' when you need executable steps",
            "📚 Use 'ask_perplexity' for quick research and factual information"
        ],
        "available_models": {
            "sonar": "Fast research model with internet access (default for research)",
            "sonar-pro": "Advanced research with deeper analysis",
            "sonar-deep-research": "Most thorough research with comprehensive citations",
            "sonar-reasoning": "Complex reasoning and step-by-step thinking (default for learning/instructions)",
            "sonar-reasoning-pro": "Advanced reasoning for complex problems"
        }
    }
    
    # Format the examples into a readable string
    output = f"# {examples['title']}\n\n"
    output += f"{examples['description']}\n\n"
    output += "## 🛠️ Available Tools\n\n"
    
    for tool in examples['tools']:
        output += f"### {tool['name']}\n"
        output += f"**Purpose:** {tool['purpose']}\n\n"
        output += f"**When to use:** {tool['when_to_use']}\n\n"
        output += f"**Examples:**\n"
        for ex in tool['examples']:
            output += f"  - \"{ex}\"\n"
        output += f"\n**Model:** {tool['model_recommendation']}\n\n"
        output += "---\n\n"
    
    output += "## 💡 Tips for Best Results\n\n"
    for tip in examples['tips']:
        output += f"{tip}\n"
    
    output += "\n## 🤖 Available Models\n\n"
    for model, desc in examples['available_models'].items():
        output += f"- **{model}**: {desc}\n"
    
    return output


@mcp.tool()
async def ask_perplexity(
    prompt: str,
    model: str = DEFAULT_MODEL_RESEARCH
) -> str:
    """
    Send a prompt to Perplexity and return the response.
    Sonar models have internet access and can perform searches.

    Use this for: research, current events, comparisons, finding information online.
    
    Examples of good prompts:
    - "What are the latest developments in quantum computing in 2025?"
    - "Compare Python vs Rust for web development"
    - "Explain the recent changes in EU privacy laws"
    - "Find the best practices for React Server Components"

    If the user wants to execute or learn complex tasks, use the reasoning model (sonar-reasoning)
    If the user wants development work requiring real-time documentation lookup, research-intensive coding, use the reasoning model (sonar-reasoning).
    But by default, use the research model (sonar).
    
    Args:
        prompt: The prompt/question to send
        model: Sonar model (sonar, sonar-pro, sonar-deep-research, 
               sonar-reasoning, sonar-reasoning-pro)
    """
    try:
        response = get_perplexity_response(prompt, model)
        
        # Add helpful metadata to guide next steps
        metadata = "\n\n---\n💡 **Next steps you might consider:**\n"
        metadata += "- Use `ask_perplexity_to_learn` if you want a detailed explanation of any concept mentioned\n"
        metadata += "- Use `ask_perplexity_for_instructions` if you want step-by-step implementation guidance\n"
        metadata += "- Ask follow-up questions to dive deeper into specific aspects\n"
        
        return response + metadata

    except Exception as e:
        return f"❌ Perplexity Error: {str(e)}"


@mcp.tool()
async def ask_perplexity_exact_response(
    prompt: str,
    model: str = DEFAULT_MODEL_RESEARCH
) -> str:
    """
    Send a prompt to Perplexity and return the exact response without 
    changing anything (no additional metadata or suggestions).

    Use this when you need the raw, unmodified output from Perplexity.
    
    Examples of good prompts:
    - "Give me the exact documentation for FastAPI's dependency injection"
    - "What does the official Next.js docs say about App Router?"
    - "Show me the raw API response format for OpenAI's latest models"

    If the user wants to execute or learn complex tasks, use the reasoning model (sonar-reasoning)
    If the user wants development work requiring real-time documentation lookup, research-intensive coding, use the reasoning model (sonar-reasoning).
    But by default, use the research model (sonar).
    
    Sonar models have internet access and can perform searches.
    
    Args:
        prompt: The prompt/question to send
        model: Sonar model (sonar, sonar-pro, sonar-deep-research, 
               sonar-reasoning, sonar-reasoning-pro)
    """
    try:
        response = get_perplexity_response(prompt, model)
        return response

    except Exception as e:
        return f"❌ Perplexity Error: {str(e)}"
    
    

@mcp.tool()
async def ask_perplexity_for_instructions(
    prompt: str,
    model: str = DEFAULT_MODEL_REASONING
) -> str:
    """
    Send a prompt to Perplexity and get step-by-step instructions that 
    Copilot can execute in agent mode.
    
    This tool is optimized for tasks that require multiple steps or actions.
    The response will be formatted as executable instructions for the AI agent.
    
    Examples of good prompts:
    - "How do I set up a Python FastAPI project with Docker?"
    - "Create a React app with TypeScript and Tailwind CSS"
    - "Set up CI/CD pipeline for a Node.js application"
    - "Configure a PostgreSQL database with Redis caching"
    
    Sonar models have internet access and can perform searches.
    
    Args:
        prompt: The prompt/question to send
        model: Sonar model (sonar, sonar-pro, sonar-deep-research, 
               sonar-reasoning, sonar-reasoning-pro)
    """
    try:
        response = get_perplexity_response(prompt, model, 
                                           prePromptInput="Provide step-by-step instructions for the following request, that the copilot agent model can follow.",
                                           prePromptOutput="PREPROMPT COPILOT EXECUTE THESE INSTRUCTIONS WITH YOUR AGENT MODE YOU HAVE TO FOLLOW THESE STEPS:")
        return response

    except Exception as e:
        return f"❌ Perplexity Error: {str(e)}"
    

@mcp.tool()
async def ask_perplexity_to_learn(
    prompt: str,
    model: str = DEFAULT_MODEL_REASONING
) -> str:
    """
    Learn complex concepts with pedagogical explanations, examples, and analogies.
    
    This tool uses a teaching-optimized approach with:
    - Simple overviews and context
    - Step-by-step breakdowns
    - Concrete examples and analogies
    - Code snippets when relevant
    - Clear summaries and next steps
    
    Examples of good prompts:
    - "Explain how async/await works in Python"
    - "Teach me about Docker containers and why they're useful"
    - "What are React hooks and how do I use them?"
    - "Explain database indexing with practical examples"
    - "How does JWT authentication work?"

    Sonar models have internet access and can perform searches.
    
    Args:
        prompt: The prompt/question to send
        model: Sonar model (sonar, sonar-pro, sonar-deep-research, 
               sonar-reasoning, sonar-reasoning-pro)
    """
    try:
        prepromptInput= f"""
        You are an excellent computer science and mathematics teacher. When asked to explain a complex concept, follow this pedagogical approach:

        1. ALWAYS START with a simple overview in 2-3 sentences to provide context
        2. BREAK DOWN the topic into logical numbered steps (3-7 steps maximum)
        3. FOR EACH STEP:
        - Explain the concept using simple words
        - Give a concrete and simple example
        - If it's code, provide short commented snippets
        - Use everyday analogies when possible
        4. END with a summary of key points and tips for going further
        6. IF the topic involves code, provide complete but minimal examples in requested language
        7. STRUCTURE your response with clear headings, lists, and well-formatted code

        Don't use jargon without explaining it immediately. Prefer visual/analogical examples over pure mathematical formulas when possible. Be patient and encouraging in your tone.
        Use the language in the user prompt:
        
        USER PROMPT:
        """
        response = get_perplexity_response(prompt, model, 
                                           prePromptInput=prepromptInput,
            )
        
        # Add learning tips
        learning_tips = "\n\n---\n📚 **Learning Tips:**\n"
        learning_tips += "- Try implementing the examples yourself to solidify understanding\n"
        learning_tips += "- Use `ask_perplexity_for_instructions` if you want to build something with this knowledge\n"
        learning_tips += "- Ask follow-up questions about specific parts you want to explore deeper\n"
        
        return response + learning_tips

    except Exception as e:
        return f"❌ Perplexity Error: {str(e)}"

def main():
    """Entry point for the MCP server."""
    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()
