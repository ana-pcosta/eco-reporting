import json
from typing import Dict, List, Optional
from jinja2 import Template, Environment, FileSystemLoader
from ecoreporter.modelhandler import ModelHandler
from langchain_core.messages import HumanMessage, SystemMessage


class ContentEvaluator:
    def __init__(self, best_practice_doc: str, instruction_doc: str):
        self.best_practice = best_practice_doc
        self.instructions = instruction_doc
        self.prompt_env = Environment(loader=FileSystemLoader("./prompts"))
        self.model_handler = ModelHandler()

    def evaluate_report_against_standards(self, report: str, llm_client) -> Dict:
        """
        Evaluates a climate report using structured prompting and comparison
        """

        system_prompt_template = self.prompt_env.get_template("system_prompt.jinja")
        instruction_comparison_prompt_template = self.prompt_env.get_template(
            "instruction_comparison_prompt.jinja"
        )

        system_prompt = system_prompt_template.render({})
        instruction_comparison_prompt = instruction_comparison_prompt_template.render(
            {"standard_instructions": self.instructions, "report": report}
        )

        messages = [
            SystemMessage(system_prompt),
            HumanMessage(instruction_comparison_prompt),
        ]

        components = self.model_handler.generate_response(messages)
        report_components = json.loads(components)

        return report_components
