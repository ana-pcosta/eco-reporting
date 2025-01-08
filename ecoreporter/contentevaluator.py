import json
from typing import Dict, List, Optional
from jinja2 import Template, Environment, FileSystemLoader
from ecoreporter.modelhandler import ModelHandler
from langchain_core.messages import HumanMessage, SystemMessage
from ecoreporter import ROOT_PATH


class ContentEvaluator:
    def __init__(self):
        self.prompt_env = Environment(
            loader=FileSystemLoader(ROOT_PATH + "/ecoreporter/prompts")
        )
        self.model_handler = ModelHandler()

        ## Define the system persona and set of instructions that are common to all tasks
        system_prompt_template = self.prompt_env.get_template("system_prompt.jinja")
        self.system_prompt = system_prompt_template.render({})

    def extract_standards_components(self, standards: str) -> Dict:
        """
        Identifies gaps in a report based on the instructions and standards provided
        """
        ## 1st: Compare the report against the EU standard and provide a list of gaps
        instruction_component_extractor_prompt_template = self.prompt_env.get_template(
            "instruction_component_extractor_prompt.jinja"
        )

        instruction_component_extractor_prompt = (
            instruction_component_extractor_prompt_template.render(
                {"standard_instructions": standards}
            )
        )

        messages = [
            SystemMessage(self.system_prompt),
            HumanMessage(instruction_component_extractor_prompt),
        ]

        components = self.model_handler.generate_response(messages)

        return components

    def evaluate_report_against_standards(self, report: str, components: str) -> Dict:
        """
        Identifies gaps in a report based on the instructions and standards provided
        """
        components = json.loads(components)

        ## 1st: Compare the report against the EU standard and provide a list of gaps
        instruction_comparison_prompt_template = self.prompt_env.get_template(
            "instruction_comparison_prompt.jinja"
        )
        gaps = []
        for component_name, component_description in components.items():
            instruction_comparison_prompt = (
                instruction_comparison_prompt_template.render(
                    {
                        "report_component_description": component_description,
                        "report_component": component_name,
                        "report": report,
                    }
                )
            )

            messages = [
                SystemMessage(self.system_prompt),
                HumanMessage(instruction_comparison_prompt),
            ]

            gap = self.model_handler.generate_response(messages)
            gaps.append(gap)

        return gaps

    def format_final_gap_evaluation(self, report_gaps: Dict, example_report_gaps: Dict):
        """
        Joins components descriptions and examples onto a single report evaluation
        """

        final_result = []
        for i, component in enumerate(report_gaps):
            component = json.loads(component)[0]
            if not component["is_reported"]:
                example = json.loads(example_report_gaps[i])[0]
                gap = f"- **{component['title']}**: {component['description']}"
                if example["is_reported"]:
                    gap_examples = f"  - Ex: *'{example['report_content']}'*"
                else:
                    gap_examples = ""
                final_result.append(f"{gap}\n\n{gap_examples}")

        return "\n\n".join(final_result)
