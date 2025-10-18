# transcriptmanager.py
# 06/22/2025 - Voltur
#
# Helper to handle loading and saving via the LLM 
# 

import os
from datetime import datetime
from voltlogger import Logger
from chatcolors import Colors
from chatcolors import ChatColors

class TranscriptManager:
    def __init__(self, base_dir="."):
        self.base_dir = base_dir

    def list_transcripts(self):
        files = sorted([f for f in os.listdir('.') if f.endswith('.json')], reverse=True)
        if not files:
            Logger.log(f"\n{ChatColors.system}(No .json transcript files found in current directory.){Colors.reset}\n")
            return None

        Logger.log(f"\n{ChatColors.highlight}Available transcript files:{Colors.reset}")
        for i, file in enumerate(files, start=1):
            Logger.log(f"  {i}. {file}")

        return files

    def save(self, llm, persona):
        date_str = datetime.now().strftime("%Y-%m-%d_%H%M")
        # Windows can't handle certain characters in filenames
        safe_persona = persona
        for ch in [':', '/', '\\', '*', '?', '"', '<', '>', '|']:
            safe_persona = safe_persona.replace(ch, '_')
        filename = f"{date_str}_{safe_persona}.json"
        llm.save_transcript(filename)
        Logger.log(f"\n{ChatColors.system}Chat saved to {filename}{Colors.reset}\n")

    def load(self, llm):
        files = self.list_transcripts()
        if files:
            choice = input(f"\n{ChatColors.system}Enter number to load or press Enter to cancel:{Colors.reset} ").strip()
            if not choice:
                Logger.log(f"{ChatColors.system}Load canceled.{Colors.reset}\n")
                return

            try:
                index = int(choice) - 1
                if 0 <= index < len(files):
                    filename = files[index]
                    llm.load_transcript(filename)
                    Logger.log(f"\n{ChatColors.system}Loaded transcript from {filename}{Colors.reset}\n")
                else:
                    Logger.log(f"{Colors.fg.red}Invalid selection.{Colors.reset}")
            except ValueError:
                Logger.log(f"{Colors.fg.red}Please enter a number.{Colors.reset}")


TranscriptManager = TranscriptManager()