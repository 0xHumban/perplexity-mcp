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
async def ask_perplexity(
    prompt: str,
    model: str = DEFAULT_MODEL_RESEARCH
) -> str:
    """
    Send a prompt to Perplexity and return the response.
    Sonar models have internet access and can perform searches.

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
        return response

    except Exception as e:
        return f"❌ Perplexity Error: {str(e)}"


@mcp.tool()
async def ask_perplexity_exact_response(
    prompt: str,
    model: str = DEFAULT_MODEL_RESEARCH
) -> str:
    """
    Send a prompt to Perplexity and return the exact response without 
    changing anything.

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
    Send a prompt to Perplexity and execute the instructions in agent mode given by the Perplexity response.
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
     Send a prompt to Perplexity and return the exact response without 
    changing anything.

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
        return response

    except Exception as e:
        return f"❌ Perplexity Error: {str(e)}"

def main():
    """Entry point for the MCP server."""
    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()
