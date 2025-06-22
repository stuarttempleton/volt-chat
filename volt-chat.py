# volt-chat.py
# 05/19/2025 - Voltur
#
# Example use of LLMConversation to create a basic text chat with an LLM.
# 


import os
import sys
from chatcolors import Colors
from datetime import datetime
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
  --no-color                   Disable ANSI color output (helpful for logs or plain terminals). 

Examples:
  {script_name} Gemma3:12b Alice --api-url=http://my-local-server:8000/api/chat
  {script_name} Llama2 Bob

Notes:
  - Type your message and press Enter to chat.
  - Commands must begin with a '/' character.
  - Use --no-color if your terminal doesn't support ANSI escape codes.

"""
    Logger.help(message)

def chat_help():
    help = f"""
Available Commands:

  /help         Show this help message.
  /quit         Exit the chat.
  /save         Save the current conversation transcript.
                   Saved as: YYYY-MM-DD_<model>.json
  /load         Load a transcript from a list of saved files.
                   You'll be prompted to choose by number.
  /history      View and optionally resend a recent user message.
  /models       List available models (if supported by API).
  ///           Enter multiline input mode.
                   Type multiple lines, end with '///' on a new line.


Notes:
  - Type your message and press Enter to chat.
  - Commands must begin with a '/' character.
"""
    Logger.log(f"\n{Colors.italic}{sys_color}{help}{Colors.reset}\n")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        usage()
        sys.exit(1)
    
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
    
    # Set up some defau lt Colors
    text_color = Colors.fg.lightgrey
    sys_color = Colors.fg.darkgrey
    sender_color = Colors.fg.green
    recpt_color = Colors.fg.purple
    highlight_color = Colors.fg.cyan

    # Set up your chat identities
    persona = sys.argv[1] or "Gemma3"
    handle = sys.argv[2] or "User"
    llm = LLMConversation(model=persona, system_prompt="We are best buds!", api_url=user_api_url)

    Logger.log(f"\n{Colors.italic}{sys_color}Connected to {llm.client.api_url} using model '{persona}'{Colors.reset}\n")


    # Main loop
    while True:
        prompt_prefix = f"{Colors.bold}{sender_color}{handle.capitalize()}{Colors.reset}: {text_color}"

        your_message = input(prompt_prefix).strip()

        if your_message.strip() == "///":
            Logger.log(f"{sys_color}Multiline mode: type your message, end with '///' on a new line{Colors.reset}")
            lines = []
            while True:
                line = input()
                if line.strip() == "///":
                    break
                lines.append(line)
            your_message = "\n".join(lines)

        if your_message in {"/quit","/bye","/exit"}:
            Logger.log(f"{Colors.reset}{Colors.italic}{sys_color}\nExiting...{Colors.reset}\n")
            break
        elif your_message.strip() == "/history":
            user_messages = [m["content"] for m in llm.messages if m.get("role") == "user"]

            if not user_messages:
                Logger.log(f"\n{sys_color}(No messages yet.){Colors.reset}\n")
                continue

            Logger.log(f"\n{highlight_color}Recent user messages:{Colors.reset}")
            for i, line in enumerate(user_messages[-10:], start=1):
                Logger.log(f"{i}: {line}")

            choice = input(f"\n{sys_color}Enter number to resend, or press Enter to cancel:{Colors.reset} ").strip()
            if not choice:
                Logger.log(f"{sys_color}History send canceled.{Colors.reset}\n")
                continue

            try:
                index = int(choice) - 1
                if 0 <= index < len(user_messages[-10:]):
                    your_message = user_messages[-10:][index]
                    Logger.log(f"{sys_color}Resending message: {your_message}{Colors.reset}")
                else:
                    Logger.log(f"{Colors.fg.red}Invalid selection.{Colors.reset}\n")
                    continue
            except ValueError:
                Logger.log(f"{Colors.fg.red}Please enter a number.{Colors.reset}\n")
                continue

        elif your_message.startswith("/models"):
            models = llm.client.get_models() or "feature not available"
            model_list = ""
            for model in models['data']: 
                model_list += f"\n\t{model.get('name', '??')} - {model.get('id', '??')}"
            Logger.log(f"\n{Colors.italic}{sys_color}Models found:{model_list}{Colors.reset}\n")
            continue
        elif your_message.startswith("/save"):
            date_str = datetime.now().strftime("%Y-%m-%d_%H%M")
            filename = f"{date_str}_{persona}.json"
            llm.save_transcript(filename)
            Logger.log(f"\n{sys_color}Chat saved to {filename}{Colors.reset}\n")
            continue
        elif your_message.strip() == "/load":
            files = sorted([f for f in os.listdir('.') if f.endswith('.json')], reverse=True)
            if not files:
                Logger.log(f"{Colors.fg.red}No .json transcript files found in current directory.{Colors.reset}")
                continue

            Logger.log(f"\n{highlight_color}Available transcript files:{Colors.reset}")
            for i, file in enumerate(files, start=1):
                Logger.log(f"  {i}. {file}")

            choice = input(f"\n{sys_color}Enter number to load or press Enter to cancel:{Colors.reset} ").strip()
            if not choice:
                Logger.log(f"{sys_color}Load canceled.{Colors.reset}\n")
                continue

            try:
                index = int(choice) - 1
                if 0 <= index < len(files):
                    filename = files[index]
                    llm.load_transcript(filename)
                    Logger.log(f"\n{sys_color}Loaded transcript from {filename}{Colors.reset}\n")
                else:
                    Logger.log(f"{Colors.fg.red}Invalid selection.{Colors.reset}")
            except ValueError:
                Logger.log(f"{Colors.fg.red}Please enter a number.{Colors.reset}")
            continue
        elif your_message.startswith("/") or your_message in {"/help", "/?"}:
            chat_help()
            continue

        try:
            print(f"\n{Colors.italic}{sys_color}Thinking...{Colors.reset}", end="\r", flush=True)
            response = llm.send_with_full_context(your_message)
            print(" " * 80, end="\r")
        except Exception as e:
            Logger.log(f"\n{Colors.fg.red}Error from LLM: {e}{Colors.reset}\n")
            continue

        response = response.replace(f"{handle.capitalize()}", f" {Colors.bold}{highlight_color}{handle.upper()}{Colors.reset}{text_color}")
        Logger.log(f"{Colors.reset}{Colors.bold}{recpt_color}{persona.capitalize()}{Colors.reset}: {text_color}{response}{Colors.reset}\n")