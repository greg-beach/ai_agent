import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys

from prompts import system_prompt
from call_function import available_functions


def main():
    load_dotenv()

    verbose = "--verbose" in sys.argv
    args = []
    for arg in sys.argv[1:]:
        if not arg.startswith("--"):
            args.append(arg)

    if not args:
        print("AI Code Assistant\n")
        print("Usage: python main.py \"your prompt here\"\n")
        print("Example: python main.py \"How do I build a calculator app?\"\n")
        sys.exit(1)

    user_prompt = " ".join(args)

    verbose = False
    if args[-1] == "--verbose":
        verbose = True 

    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]
   
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
   
    response = client.models.generate_content(
        model="gemini-2.0-flash-001", 
        contents=messages, 
        config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt))

    if verbose:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    
    print("Response:\n")
    if not response.function_calls:
        return response.text
    
    for function_call_part in response.function_calls:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    


if __name__ == "__main__":
    main()
