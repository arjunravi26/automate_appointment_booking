import json

from dotenv import load_dotenv
from agno.agent import Agent
from .extract_attribute import find_element_attributes
from .plan_steps import plan_steps
from .utilities.agent import create_model

load_dotenv()


def map_steps_to_elements(steps: list, element_attributes: list) -> list:
    """
    Map each step (from the appointment booking plan) with its corresponding element
    from the form, determining the element's tag and its most appropriate locator.

    Each mapping in the output JSON array is an object with:
    - 'step': the original step details (action, field, locator, value)
    - 'tag': the HTML tag of the matched element (e.g., 'input', 'select')
    - 'locator': a string representing the best locator (e.g., "id=...", "name=...", "css=...")

    The agent should decide the best match based on attributes such as id, name, class, and placeholder.
    Output should be valid JSON only.
    """
    # prompt = (
    #     f"Given the following JSON array of steps:\n{json.dumps(steps)}\n\n"
    #     f"and the following JSON array of element attributes extracted from a form:\n{json.dumps(element_attributes)}\n\n"
    #     "For each step, determine the most appropriate element from the element attributes based on the field name. "
    #     "Then provide a mapping for each element's HTML tag in the with the corresponding step and the best locator. "
    #     "If corresponding step not exist for an HTML tag then map HTML tag with its best locator."
    #     "The locator should be chosen based on uniqueness, prioritizing the 'id' attribute first, then 'name', then 'class'. "
    #     "The locator must be in the format that accept by selenium. and ouput loactor as json like by for indicate attribute and value for attribute value"
    #     "Return a JSON array(not any other things like heading or any other things.) where each element is an object with the keys 'action', 'value', 'required','field_name', 'tag', and 'locator'."
    #     "Output only valid JSON, without any extra text."
    # )
    prompt = (
    f"Given the following two JSON arrays:\n"
    f"1. Steps: {json.dumps(steps)}\n"
    f"2. Element Attributes extracted from a form: {json.dumps(element_attributes)}\n\n"

    "Your task is to generate a mapping between each element attribute and its corresponding step and HTML element details. Follow the instructions below carefully and ensure that the final output is strictly valid JSON (with no extra text, markdown formatting, or additional labels), as it will be directly passed into json.loads:\n\n"

    "1. **Step Matching:**\n"
    "   - For each element attribute, check if there is a matching step based on the 'field_name'.\n"
    "   - If a matching step exists, include its 'action' and 'value' in the mapping.\n"
    "   - If no matching step exists, set both 'action' and 'value' to null for that element attribute.\n\n"

    "2. **HTML Tag and Locator Mapping:**\n"
    "   - Map each element's HTML tag along with the corresponding step (if any) and determine the best locator for the element.\n"
    "   - The locator must be formatted as a Selenium-compatible JSON object with two keys: 'attribute' and 'value'.\n"
    "   - Choose the locator based on uniqueness, following this priority order:\n"
    "       a. 'id'\n"
    "       b. 'name'\n"
    "       c. 'class'\n"
    "       d. 'xpath'\n"
    "   - If you consider using a 'text' locator, instead use an 'xpath' locator with formatted xpath value.\n\n"

    "3. **Action Determination Based on HTML Tag:**\n"
    "   - For a 'button' tag, use the action 'click'.\n"
    "   - For an 'input' tag, use the action 'fill'.\n"
    "   - For a 'select' tag, use the action 'select'.\n\n"

    "4. **Output Format:**\n"
    "   - Return a JSON array (and nothing else) where each element is an object with the following keys:\n"
    "       - 'action'\n"
    "       - 'value'\n"
    "       - 'required'\n"
    "       - 'field_name'\n"
    "       - 'tag'\n"
    "       - 'locator' (a JSON object with keys 'attribute' and 'value')\n\n"

    "5. **Strict Output Requirement:**\n"
    "   - The final output must be strictly valid JSON that can be parsed directly with json.loads. Do not include any additional text, markdown formatting (such as triple backticks or the word 'json'), or comments in your output.\n\n"

    "6. **Output Format Example:**\n"
    "   Each mapping should follow this exact format:\n"
    "   {\n"
    "       \"action\": <value>,\n"
    "       \"value\": <value>,\n"
    "       \"required\": <value>,\n"
    "       \"field_name\": <value>,\n"
    "       \"tag\": <value>,\n"
    "       \"locator\": {\"attribute\": <value>, \"value\": <value>}\n"
    "   }\n\n"

    "Process the input data accordingly and return only the resulting JSON array without any markdown formatting or extra text."
)



    model = create_model()
    agent = Agent(model=model, expected_output='json')
    response = agent.run(prompt)
    print("Agent response:", response.content)
    try:
        mapping = json.loads(response.content)
    except Exception as e:
        print(f"Error parsing JSON from agent response: {e}")
        mapping = []
    print("Mapping result:\n", mapping)
    return mapping


# Example usage:
if __name__ == "__main__":
    # Example steps from the appointment booking process (normally generated by your LLM agent)
    steps = plan_steps(
        "Book an appointment for John Doe with email john@example.com, phone 1234567890, service Initial Consultation, and insurance number INS12345.")
    print(steps)
    # Example element attributes extracted from a web form
    element_attributes = find_element_attributes()
    print(element_attributes)
    mapping = map_steps_to_elements(steps, element_attributes)
    print("Final Mapping JSON:", json.dumps(mapping, indent=2))
    # "Then provide a mapping for each step in the with the corresponding element's HTML tag and the best locator. "
