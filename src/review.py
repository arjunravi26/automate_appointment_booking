from plan_steps import plan_steps
from extract_attribute import find_element_attributes
from element_attribute_agent import map_steps_to_elements


def review():
    steps = plan_steps(
        "Book an appointment for John Doe with phone 1234567890, service Initial Consultation, and insurance number INS12345.")

    element_info = find_element_attributes()
    final_steps = map_steps_to_elements(
        steps=steps, element_attributes=element_info)
    missing_infos = []
    for step in final_steps:
        if step['required'] and step['value'] == '':
            missing_infos.append([step['field_name'], step])
    print(missing_infos)
    if missing_infos:
        reenter = input(
            f"Sorry! some values are missing, try to fill {missing_infos}")
        print(reenter)


if __name__ == "__main__":
    "Book an appointment for John Doe with email john@example.com, phone 1234567890, service Initial Consultation, and insurance number INS12345."
    review()
