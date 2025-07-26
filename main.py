import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts import system_prompt
from call_function import available_functions, call_function

def main():
    print("Hello from ai-agent!")

    if len(sys.argv) < 2:
        print("Error: must add prompt to command line")
        sys.exit(1)

    verbose = "--verbose" in sys.argv
    if verbose:
        print(f"User prompt: {sys.argv[1]}")

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)

    messages = [
        types.Content(role="user", parts = [types.Part(text=sys.argv[1])]),
    ]
    for iteration in range(0,20):
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash-001",
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions], system_instruction=system_prompt
                ),
            )
            for candidate in response.candidates:
                messages.append(candidate.content)

            if verbose:
                print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
                print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

            if not response.function_calls:
                print(response.text)
                break
            else:
                for function_call_part in response.function_calls:
                    #print(f"Calling function: {function_call_part.name}({function_call_part.args})")
                    function_responses = call_function(function_call_part, verbose)
                    messages.append(function_responses)
        except Exception as e:
            print(f"Error: generation loop, iteration-{iteration}: {e}")


if __name__ == "__main__":
    main()
