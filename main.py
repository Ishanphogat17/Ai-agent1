import os
#dotenv is to get env variables
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import types



from prompts import system_prompt
from call_function import available_functions


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
        contents=messages,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=0,
            tools=[available_functions]
        )
    )
    if response.function_calls:
        for call in response.function_calls:
            print(f"Function call: {call.name}")
            print(f"args: {call.args}")
    else:
        print(response.text)
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

if __name__ == "__main__":
    main()
