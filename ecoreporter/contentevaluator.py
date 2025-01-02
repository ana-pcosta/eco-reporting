import json
from typing import Dict, List, Optional
from jinja2 import Template, Environment, FileSystemLoader
from ecoreporter.modelhandler import ModelHandler
from langchain_core.messages import HumanMessage, SystemMessage
from ecoreporter import ROOT_PATH


class ContentEvaluator:
    def __init__(self, instruction_doc: str, best_practice_doc: str):
        self.best_practice = best_practice_doc
        self.instructions = instruction_doc
        self.prompt_env = Environment(
            loader=FileSystemLoader(ROOT_PATH + "/ecoreporter/prompts")
        )
        self.model_handler = ModelHandler()

        ## Define the system persona and set of instructions that are common to all tasks
        system_prompt_template = self.prompt_env.get_template("system_prompt.jinja")
        self.system_prompt = system_prompt_template.render({})

    def evaluate_report_against_standards(self, report: str) -> Dict:
        """
        Identifies gaps in a report based on the instructions and standards provided
        """
        ## 1st: Compare the report against the EU standard and provide a list of gaps
        instruction_comparison_prompt_template = self.prompt_env.get_template(
            "instruction_comparison_prompt.jinja"
        )

        instruction_comparison_prompt = instruction_comparison_prompt_template.render(
            {"standard_instructions": self.instructions, "report": report}
        )

        messages = [
            SystemMessage(self.system_prompt),
            HumanMessage(instruction_comparison_prompt),
        ]

        components = self.model_handler.generate_response(messages)

        ## 2nd: Compare the report an industry best practice and provide examples of how
        # missing information can be reported

        return components

    def extract_examples_of_report_components(self, components: str) -> Dict:
        """
        Extracts examples from a report of specific components/information
        """

        ## 1st: Compare the report against the EU standard and provide a list of gaps
        example_instruction_extractor_prompt_template = self.prompt_env.get_template(
            "example_instruction_extractor_prompt.jinja"
        )

        example_instruction_extractor_prompt = (
            example_instruction_extractor_prompt_template.render(
                {"report_components": components, "report": self.best_practice}
            )
        )

        messages = [
            SystemMessage(self.system_prompt),
            HumanMessage(example_instruction_extractor_prompt),
        ]

        components = self.model_handler.generate_response(messages)

        return components

    def format_final_evaluation(self, components: Dict, examples: Dict):
        """
        Joins components descriptions and examples onto a single report evaluation
        """
        components = json.loads(components)
        examples = json.loads(examples)
        final_result = []
        for component_name, component_description in components.items():
            gap = f"- **{component_name}**: {component_description}"
            gap_examples = "\n\n".join(
                [f"  - Ex: *'{example}'*" for example in examples[component_name]]
            )
            final_result.append(f"{gap}\n\n{gap_examples}")

        return "\n\n".join(final_result)
