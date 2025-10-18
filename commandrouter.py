# commandrouter.py
# 06/22/2025 - Voltur
#
# Routes varous slash commands to the proper manager. 
# 

import sys

from voltlogger import Logger
from chatcolors import Colors, ChatColors
from transcriptmanager import TranscriptManager
from modelmanager import ModelManager
from historymanager import HistoryManager
from multilinemanager import MultiLineManager

class CommandRouter:
    def __init__(self, llm, persona, base_dir=None):
        self.llm = llm
        self.persona = persona
        if base_dir:
            TranscriptManager.base_dir = base_dir

    def update_base_dir(self, base_dir):
        TranscriptManager.base_dir = base_dir

    def handle(self, message):

        cmd = message.strip().lower()

        if cmd in {"/quit", "/bye", "/exit"}:
            Logger.log(f"{Colors.reset}{ChatColors.system}\nExiting...{Colors.reset}\n")
            sys.exit(0)

        elif cmd in {"/help", "/?"}:
            self._show_help()
            return True

        elif cmd == "/save":
            TranscriptManager.save(llm=self.llm, persona=self.persona)
            return True

        elif cmd == "/load":
            TranscriptManager.load(llm=self.llm)
            return True

        elif cmd == "/models":
            ModelManager.show(llm=self.llm)
            return True

        elif cmd == "/history":
            result = HistoryManager.get(self.llm)
            if result:
                # Return the selected history to the main loop to send to LLM
                return result
            return True  # still handled

        elif cmd == MultiLineManager.toggle_string:
            result = MultiLineManager.read()
            return result  # return string to be sent

        elif cmd.startswith("/"): # catch mistake commands before handing them to LLM
            Logger.log(f"\n{ChatColors.system}I don't know that command.{Colors.reset}")
            self._show_help()
            return True
        
        return False  # Command not recognized

    def _show_help(self):
        help_text = f"""
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
        Logger.log(f"\n{ChatColors.system}{help_text}{Colors.reset}\n")
