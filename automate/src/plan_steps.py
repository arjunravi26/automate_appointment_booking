import json
from agno.agent import Agent
from .utilities.agent import create_model
from typeguard import typechecked


@typechecked
def plan_steps(command: str):
    '''Function to plan steps according to user command'''
    model = create_model()
    agent = Agent(
        model=model,
        role="Appointment Automation Planner",
        description=(
            "You are an expert in agentic AI with a specialization in workflow automation."
            "Your deep understanding of UI interactions and process optimization enables you to analyze"
            "user commands and generate detailed, step-by-step plans to automate appointment booking on web platforms."
        ),
        instructions=(
            "When given a command, generate a JSON array of step-by-step actions specifically for automating",
            "the appointment booking process on the provided website. Each step must include the following keys:",
            "'action' (which must be one of 'fill', 'click', or 'select') and 'field' (such as 'name', 'email', 'phone', etc.).",
            "Automatically detect and include any additional fields mentioned in the command. Output only a",
            "valid JSON array without any additional text or commentary."
        ),expected_output='json'
    )
    steps = []
    website_link = "https://arjunravi26.github.io/appointment-booking/"
    prompt = (
        f"Given the command: '{command}', generate a JSON array of step-by-step actions for automating "
        f"the appointment booking process on {website_link}. For each step, include the following keys: "
        f"'action' (one of 'fill', 'click', or 'select'), 'field' (e.g., 'name', 'email', 'phone', etc.) and 'value'.  "
        f"Include any new fields found in the command automatically. Output JSON format only, not any other things(like heading or any other things.)."
    )
    response = agent.run(prompt)
    try:
        steps = json.loads(response.content)
    except Exception as e:
        print(f"Could not convert into json {e}")
    print("Agent plan:\n",steps)
    return steps


if __name__ == "__main__":
    steps = plan_steps(
        "Book an appointment for John Doe with email john@example.com, phone 1234567890, service Initial Consultation, and insurance number INS12345.")
    print(steps)
