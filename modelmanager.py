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
        if "data" in models:
            for model in models['data']: 
                model_list += f"\n\t{model.get('name', '??')} - {model.get('id', '??')}"
        elif "models" in models:
            for model in models['models']: 
                model_list += f"\n\t{model.get('name', '??')} - {model.get('model', '??')}"
        Logger.log(f"\n{ChatColors.system}Models found:{model_list}{Colors.reset}\n")

ModelManager = ModelManager()