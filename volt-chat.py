# volt-chat.py
# 05/19/2025 - Voltur
#
# Example use of LLMConversation to create a basic text chat with an LLM.
# 


import os
import sys

# ANSI Chat colors
from chatcolors import Colors
from chatcolors import ChatColors
from voltlogger import Logger
from voltllmclient import LLMConversation
from commandrouter import CommandRouter


def usage():
    script_name = os.path.basename(sys.argv[0])
    message = f"""
Usage: {script_name} <model_name> <user_name> [--api-url=<openai_api_url>]

Description:
  Starts a text-based chat session with an LLM.

Arguments:
  <model_name>:   The name of the LLM to use (e.g., "Gemma3").
  <user_name>:   Your name to identify yourself in the chat.

Optional Arguments:
  --base-url=<openai_base_url>:  Overrides the default OpenAI base URL.
                                  (e.g., --base-url=http://localhost:3000)
  --no-color                   Disable ANSI color output (helpful for logs or plain terminals).

Examples:
  {script_name} Gemma3:12b Alice --base-url=http://my-local-server:8000
  {script_name} Llama2 Bob

Notes:
  - Type your message and press Enter to chat.
  - Commands must begin with a '/' character.
  - Use --no-color if your terminal doesn't support ANSI escape codes.

"""
    Logger.help(message)

def run_chat(llm, handle, persona):
    router = CommandRouter(llm=llm, persona=persona)

    # Main loop
    while True:

        # Prompt the user for chat
        prompt_prefix = f"{Colors.bold}{ChatColors.sender}{handle.capitalize()}{Colors.reset}: {ChatColors.text}"
        your_message = input(prompt_prefix).strip()

        # Handle any / commands from the user
        handled = router.handle(your_message)
        if handled is True:
            continue # handled!
        elif isinstance(handled, str):
            your_message = handled # Pass the mssage on!
        
        # Hand the chat message to the LLM
        try:
            print(f"\n{Colors.italic}{ChatColors.system}Thinking...{Colors.reset}", end="\r", flush=True)
            response = llm.send_with_full_context(your_message)
            print(" " * 80, end="\r")
        except Exception as e:
            Logger.log(f"\n{Colors.fg.red}Error from LLM: {e}{Colors.reset}\n")
            continue

        # Tell us what the LLM had to say about it
        response = response.replace(f"{handle.capitalize()}", f" {Colors.bold}{ChatColors.highlight}{handle.upper()}{Colors.reset}{ChatColors.text}")
        Logger.log(f"{Colors.reset}{Colors.bold}{ChatColors.recpt}{persona.capitalize()}{Colors.reset}: {ChatColors.text}{response}{Colors.reset}\n")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        usage()
        sys.exit(1)
    
    user_api_url = "http://localhost:3000"

    for arg in sys.argv[1:]:
        if arg.startswith("--help"):
            usage()
            sys.exit(0)
        elif arg.startswith("--base-url="):
            user_api_url = arg.split("=")[1]
            if not user_api_url:
                print("Error: --base-url provided but no base URL was specified.")
                sys.exit(1)

    # Set up your chat identities
    persona = sys.argv[1] or "Gemma3"
    handle = sys.argv[2] or "User"
    llm = LLMConversation(model=persona, system_prompt="We are best buds!", base_url=user_api_url)

    Logger.log(f"\n{Colors.italic}{ChatColors.system}Connected to {llm.client.base_url} using model '{persona}'{Colors.reset}\n")

    # This is the main loop. FYI.
    run_chat(llm=llm, handle=handle, persona=persona)
