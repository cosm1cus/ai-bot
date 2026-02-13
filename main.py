import os
import sys
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import *

def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY environment variable not set")

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    client = genai.Client(api_key=api_key)
    if args.verbose:
         print(f"User prompt: {args.user_prompt}")

    generate_content(client, messages, args.verbose)

def generate_content(client, messages, verbose):
    for _ in range(25):
        response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
            ),
        )

        if not response.usage_metadata:
            raise RuntimeError("Failed API Request")

        if verbose:
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

        if not response.function_calls:
            print("Response")
            print(response.text)
            return

        function_responses = []

        if response.candidates:
            for candidate in response.candidates:
                messages.append(candidate.content)

        for function_call in response.function_calls:
            function_call_result = call_function(function_call, verbose)
            if (
                not function_call_result.parts
                or not function_call_result.parts[0].function_response
                or not function_call_result.parts[0].function_response.response
            ):
                raise RuntimeError(f"Empty function response for {function_call.name}")
            if verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
            function_responses.append(function_call_result.parts[0])
            messages.append(types.Content(role="user", parts=function_responses))

        if not response.function_calls:
            print(response.text)
            break
    if response.function_calls:
        print("Model make maximum iterations (25)")
        sys.exit(1)

if __name__ == "__main__":
    main()