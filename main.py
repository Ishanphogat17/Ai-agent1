import os
from dotenv import load_dotenv
from google import genai


def main():
#    print("Hello from ai-agent-1!")
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key == None:
        raise Exception("RuntimeError")
    client = genai.Client(api_key=api_key)
    tokens_used = prompt_token_count
    response = client.models.generate_content(
    model='gemini-2.5-flash', contents="Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."
    )
    print(f"Prompt tokens: {tokens_used}")
    print(f"
    print(response.text)

if __name__ == "__main__":
    main()
