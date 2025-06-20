# volt-chat.py
# 05/19/2025 - Voltur
#
# Example use of LLMConversation to create a basic text chat with an LLM.
# 


import os
import sys
from voltlogger import Logger
from voltllmclient import LLMConversation

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
  --api-url=<openai_api_url>:  Overrides the default OpenAI API URL.  
                                  (e.g., --api-url=http://localhost:3000/api/chat/completions)

Examples:
  {script_name} Gemma3:12b Alice --api-url=http://my-local-server:8000/api/chat
  {script_name} Llama2 Bob
"""
    Logger.help(message)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        usage()
        exit(1)
    
    user_api_url = "http://localhost:3000/api/chat/completions"

    for arg in sys.argv[1:]:
        if arg.startswith("--help"):
            usage()
            sys.exit(0)
        elif arg.startswith("--api-url="):
            user_api_url = arg.split("=")[1]
            if not user_api_url:
                print("Error: --api-url provided but no API url was specified.")
                sys.exit(1)
    
    class colors:
        reset = '\033[0m'
        bold = '\033[01m'
        italic = '\033[03m'
        disable = '\033[02m'
        underline = '\033[04m'
        reverse = '\033[07m'
        strikethrough = '\033[09m'
        invisible = '\033[08m'

        class fg:
            black = '\033[30m'
            red = '\033[31m'
            green = '\033[32m'
            orange = '\033[33m'
            blue = '\033[34m'
            purple = '\033[35m'
            cyan = '\033[36m'
            lightgrey = '\033[37m'
            darkgrey = '\033[90m'
            lightred = '\033[91m'
            lightgreen = '\033[92m'
            yellow = '\033[93m'
            lightblue = '\033[94m'
            pink = '\033[95m'
            lightcyan = '\033[96m'

        class bg:
            black = '\033[40m'
            red = '\033[41m'
            green = '\033[42m'
            orange = '\033[43m'
            blue = '\033[44m'
            purple = '\033[45m'
            cyan = '\033[46m'
            lightgrey = '\033[47m'
    
    # Set up some defau lt colors
    text_color = colors.fg.lightgrey
    sys_color = colors.fg.darkgrey
    sender_color = colors.fg.green
    recpt_color = colors.fg.purple
    highlight_color = colors.fg.cyan

    # Set up your chat identities
    persona = sys.argv[1] or "Gemma3"
    handle = sys.argv[2] or "User"
    llm = LLMConversation(model=persona, system_prompt="We are best buds!", api_url=user_api_url)

    Logger.log(f"\n{colors.italic}{sys_color}Connected to {llm.client.api_url}{colors.reset}\n")

    # Main loop
    while True:
        your_message = input(f"{colors.bold}{sender_color}{handle.capitalize()}{colors.reset}: {text_color}")
        if your_message in {"/quit","/bye","/exit"}:
            Logger.log(f"{colors.reset}{colors.italic}{sys_color}\nExiting...{colors.reset}\n")
            break
        response = llm.send_with_summary_context(your_message)
        response = response.replace(f"{handle.capitalize()}", f" {colors.bold}{highlight_color}{handle.upper()}{colors.reset}{text_color}")
        Logger.log(f"\n{colors.reset}{colors.bold}{recpt_color}{persona.capitalize()}{colors.reset}: {text_color}{response}{colors.reset}\n")