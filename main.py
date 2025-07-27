import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Checking for argument passed in for the prompt
if len(sys.argv) < 1:
    print("No argument passed.")
    sys.exit(1)

def main():
    load_dotenv()

    api_key = os.environ.get("GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)
    
    user_prompt = sys.argv[1]
      
    # ROLES 
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages
    )

    
    print(response.text)
    
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    main()
