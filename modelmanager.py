# modelmanager.py
# 06/22/2025 - Voltur
#
# Get a list of models from the LLM 
# 

from voltlogger import Logger
from chatcolors import Colors
from chatcolors import ChatColors

class ModelManager:
    def show(self, llm):
        models = llm.client.get_models() or "feature not available"
        model_list = ""
        for model in models['data']: 
            model_list += f"\n\t{model.get('name', '??')} - {model.get('id', '??')}"
        Logger.log(f"\n{Colors.italic}{ChatColors.system}Models found:{model_list}{Colors.reset}\n")

ModelManager = ModelManager()