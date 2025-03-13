from .plan_steps import plan_steps
from .extract_attribute import find_element_attributes
from .element_attribute_agent import map_steps_to_elements


def review(command):
    steps = plan_steps(command)

    element_info = find_element_attributes()
    final_steps = map_steps_to_elements(
        steps=steps, element_attributes=element_info)
    missing_infos = []
    for step in final_steps:
        if step['required'] and step['value'] == None:
            missing_infos.append(step['field_name'])
    print(missing_infos)
    if missing_infos:
        updated_command = command
        for missing_info in missing_infos:
            reenter = input(
                f"Sorry! some values are missing, try to fill {missing_info}: ")
            updated_command = updated_command + ", " + missing_info + " is " + reenter
        print(updated_command)
        final_steps = review(command=updated_command)
    return final_steps



if __name__ == "__main__":
    command = "Book an appointment for John Doe with phone 1234567890, service Initial Consultation, and insurance number INS12345."
    review(command)
