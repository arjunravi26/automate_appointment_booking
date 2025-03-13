from automate.src.execute import execute_plan
from automate.src.review import review

def automate(command):
    final_step = review(command)
    dates = execute_plan(final_step)
    return dates