# multilinemanager.py
# 06/22/2025 - Voltur
#
# Handle switching into multi-line mode for a chat message 
# 


from voltlogger import Logger
from chatcolors import Colors
from chatcolors import ChatColors

class MultiLineManager:
    toggle_string = "///"
    def read(self, exit_str=None):
        self.toggle_string = exit_str or self.toggle_string

        Logger.log(f"{ChatColors.system}Multiline mode: type your message, end with '///' on a new line{Colors.reset}")
        lines = []
        while True:
            line = input()
            if line.strip() == "///":
                break
            lines.append(line)
        return "\n".join(lines)

MultiLineManager = MultiLineManager()