# def execute_plan(steps: list, driver, context: dict):
#     """
#     Execute each step based on the generated JSON plan.
#     The context dict provides default values for fields.
#     """
#     for step in steps:
#         try:
#             action = step.get("action", "").lower()
#             field = step.get("field", "").lower()
#             locator_key = step.get("locator", "")
#             value = step.get("value")
#             # If the value is not provided by the agent, check the context.
#             if value is None:
#                 value = context.get(field, "")
#             locator = LocatorManager.get_locator(locator_key)
#             element = driver.find_element(*locator)
#             print(
#                 f"Executing: {action} on {field} using locator {locator_key}")
#             if action == "fill":
#                 element.clear()
#                 element.send_keys(value)
#                 time.sleep(1)
#             elif action == "click":
#                 element.click()
#                 time.sleep(1)
#             elif action == "select":
#                 # For select, we assume sending keys works or you can integrate with Select class.
#                 element = Select(element)
#                 element.select_by_visible_text(value)
#                 time.sleep(1)
#             else:
#                 print(f"Unknown action: {action}")
#         except Exception as e:
#             print(
#                 f"Error executing step for field '{step.get('field')}' with locator '{step.get('locator')}': {e}")
#     time.sleep(5)