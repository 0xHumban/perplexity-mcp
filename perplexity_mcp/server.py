from mcp.server.fastmcp import FastMCP
import os
from openai import OpenAI

DEFAULT_MODEL = "sonar"

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
    model: str = DEFAULT_MODEL
) -> str:
    """
    Send a prompt to Perplexity and return the response.
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

def main():
    """Entry point for the MCP server."""
    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()
