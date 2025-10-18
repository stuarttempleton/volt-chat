# historymanager.py
# 06/22/2025 - Voltur
#
# View and resend chat messages from history 
# 


from voltlogger import Logger
from chatcolors import Colors
from chatcolors import ChatColors

class HistoryManager:
    def list_history(self, llm):
        user_messages = [m["content"] for m in llm.messages if m.get("role") == "user"]

        if not user_messages:
            Logger.log(f"\n{ChatColors.system}(No messages yet.){Colors.reset}\n")
            return None

        Logger.log(f"\n{ChatColors.highlight}Recent user messages:{Colors.reset}")
        for i, line in enumerate(user_messages[-10:], start=1):
            Logger.log(f"\t{i}: {line}")
        
        return user_messages
    
    def get(self, llm):

        user_messages = self.list_history(llm=llm)

        if user_messages:
            choice = input(f"\n{ChatColors.system}Enter number to resend, or press Enter to cancel:{Colors.reset} ").strip()
            if not choice:
                Logger.log(f"{ChatColors.system}History send canceled.{Colors.reset}\n")
                return None

            try:
                index = int(choice) - 1
                if 0 <= index < len(user_messages[-10:]):
                    your_message = user_messages[-10:][index]
                    Logger.log(f"{ChatColors.system}Resending message: {your_message}{Colors.reset}")
                    return your_message
                else:
                    Logger.log(f"{Colors.fg.red}Invalid selection.{Colors.reset}\n")
                    return None
            except ValueError:
                Logger.log(f"{Colors.fg.red}Please enter a number.{Colors.reset}\n")
        return None

HistoryManager = HistoryManager()