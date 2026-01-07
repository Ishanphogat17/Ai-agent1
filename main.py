import os
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import types


def main():
#    print("Hello from ai-agent-1!")
    
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key == None:
        raise Exception("RuntimeError")
    
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("--verbose",action="store_true", help="Verbose mode")
    parser.add_argument( "user_prompt", type=str, help="User prompt")
    args = parser.parse_args()
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=messages
    )
    print(response.text)
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

if __name__ == "__main__":
    main()
