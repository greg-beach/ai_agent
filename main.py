import os
from dotenv import load_dotenv
from google import genai
import sys


def main():
    load_dotenv()

    args = sys.argv[1:]

    if not args:
        print("AI Code Assistant\n")
        print("Usage: python main.py \"your prompt here\"\n")
        print("Example: python main.py \"How do I build a calculator app?\"\n")
        sys.exit(1)

    user_prompt = " ".join(args)
   
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
   
    response = client.models.generate_content(model="gemini-2.0-flash-001", contents=user_prompt)

    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}\n")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}\n")
    print("Respons:\n")
    print(f"{response.text}\n")


if __name__ == "__main__":
    main()
