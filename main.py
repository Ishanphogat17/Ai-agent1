import os
#dotenv is to get env variables
from dotenv import load_dotenv
from google import genai
from google.genai import errors
import argparse
from google.genai import types
import time



from prompts import system_prompt
from call_function import available_functions, call_function


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
    
    # Retry logic with exponential backoff
    max_retries = 3
    retry_delay = 1  # Initial delay in seconds
    
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=messages,
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    temperature=0,
                    tools=[available_functions]
                )
            )
            break  # Success, exit retry loop
        except errors.ServerError as e:
            if attempt < max_retries - 1:
                print(f"API error (attempt {attempt + 1}/{max_retries}): {e}. Retrying in {retry_delay}s...", flush=True)
                time.sleep(retry_delay)
                retry_delay *= 2  # Exponential backoff
            else:
                print(f"API error after {max_retries} attempts: {e}")
                raise
        except Exception as e:
            print(f"Unexpected error: {e}")
            raise
    
    
    # Handle function calls from the LLM
    function_results = []
    if response.function_calls:
        for call in response.function_calls:
            # Execute the function call
            function_call_result = call_function(call, verbose=args.verbose)
            
            # Validate the response has parts
            if not function_call_result.parts:
                raise Exception("Function call returned empty parts")
            
            # Validate the function_response exists
            if function_call_result.parts[0].function_response is None:
                raise Exception("Function call returned None function_response")
            
            # Validate the response field exists
            if function_call_result.parts[0].function_response.response is None:
                raise Exception("Function call returned None response")
            
            # Add to results list
            function_results.append(function_call_result.parts[0])
            
            # Print result in verbose mode
            if args.verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
    else:
        print(response.text)
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

if __name__ == "__main__":
    main()
