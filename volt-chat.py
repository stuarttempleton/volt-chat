# volt-chat.py
# 05/19/2025 - Voltur
#
# Example use of LLMConversation to create a basic text chat with an LLM.
# 


import os
import subprocess
import sys
import socket
from options import resolve_options

# ANSI Chat colors
from chatcolors import Colors
from chatcolors import ChatColors
from voltlogger import Logger
from voltllmclient import LLMConversation
from commandrouter import CommandRouter
from ExecutionManager import ExecutionManager


def usage():
        script_name = os.path.basename(sys.argv[0])
        message = f"""
Usage: {script_name} [--persona=MODEL] [--handle=USERNAME] [--base-url=URL] [--system-prompt=TEXT] [--config=PATH] [--no-color]

Description:
    Starts a text-based chat session with an LLM.

Options:
    --persona=MODEL         Name of the LLM model to use (default: Gemma3)
    --handle=USERNAME       Display name of the chat participant (default: User)
    --base-url=URL          Base URL of the local LLM server (default: http://localhost:3000)
    --system-prompt=TEXT    Override the system prompt
    --config=PATH           Explicitly load a config file (JSON or YAML)
    --no-color              Disable ANSI color output

Examples:
    {script_name} --persona=Gemma3:12b --handle=Alice --base-url=http://my-local-server:8000
    {script_name} --persona=Llama2 --handle=Bob

Notes:
    - Type your message and press Enter to chat.
    - Commands must begin with a '/' character.
    - Use --no-color if your terminal doesn't support ANSI escape codes.
"""
        Logger.help(message)

def get_bash_style_cwd():
    cwd = os.getcwd()
    home = os.path.expanduser('~')
    if cwd.startswith(home):
        return '~' + cwd[len(home):]
    return cwd

def is_root():
    return os.geteuid() == 0

def get_prompt_suffix():
    if (os.name == 'nt'):
        return "> "
    suffix = "# " if is_root() else "$ "
    return suffix

def git_branch() -> str | None:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            stderr=subprocess.DEVNULL,
        ).decode().strip()
    except Exception:
        return None
    
def build_prompt(handle: str) -> str:
    user = f"{ChatColors.sender}{handle}@{socket.gethostname()}:{Colors.reset}"
    cwd = f"{ChatColors.system}(cwd:{get_bash_style_cwd()}){Colors.reset}"
    delimiter = ">"

    branch = git_branch()
    if branch:
        branch_str = f" - {branch}"
        cwd = cwd.replace(")", f"{branch_str})")

    return f"{user} {delimiter} {cwd} "
    
def build_sender(sender: str, model: str) -> str:
    user = f"{Colors.fg.cyan}{sender}@{socket.gethostname()}:{Colors.reset}"
    model = f"{ChatColors.system}(model:{model}){Colors.reset}"
    delimiter = ">"

    return f"{user} {delimiter} {model} "

def run_chat(llm, opts):
    router = CommandRouter(llm=llm, opts=opts)

    # REPL loop
    while True:

        # READ
        # Prompt the user 
        prompt_prefix = build_prompt(opts.handle)
        if router.last_command_error != 0:
            prompt_prefix = f"{Colors.fg.red}[{router.last_command_error}] {Colors.reset}" + prompt_prefix
            router.last_command_error = 0
        your_message = input(prompt_prefix).strip()

        # Handle any / commands from the user
        handled = router.handle(your_message)
        if handled is True:
            continue # handled!
        elif isinstance(handled, str):
            your_message = handled # Pass the message on!

        # EVAL
        # Hand the chat message to the LLM
        try:
            print(f"\n{ChatColors.system}Thinking...{Colors.reset}", end="\r", flush=True)
            response = llm.send_with_full_context(your_message)
            print(" " * 80, end="\r")
        except Exception as e:
            Logger.log(f"\n{Colors.fg.red}Error from LLM: {e}{Colors.reset}\n")
            continue

        # PRINT && LOOP
        # Tell us what the LLM had to say about it
        Logger.log(f"{build_sender(opts.shell_name, opts.persona)} {ChatColors.text}{response}{Colors.reset}\n")


def main() -> None:
    # Check for --help or -h before parsing other options
    if any(arg in ("--help", "-h") for arg in sys.argv[1:]):
        usage()
        sys.exit(0)

    opts = resolve_options()

    llm = LLMConversation(
        model=opts.persona,
        system_prompt=opts.system_prompt,
        base_url=opts.base_url,
    )
    shell_exec_enabled_warning = ""
    if getattr(opts, "shell_exec_privs", 0) > 0:
        shell_exec_enabled_warning = f"{Colors.fg.yellow}CAUTION: Shell exec enabled!{Colors.reset}\n"

    Logger.log(
        f"\n{ChatColors.system}"
        f"Connected to {llm.client.base_url} using model '{opts.persona}'\n"
        f"{shell_exec_enabled_warning}"
        f"{Colors.reset}"
    )

    run_chat(llm=llm, opts=opts)


if __name__ == "__main__":
    main()
