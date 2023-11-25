import uuid
from dbsetup import container
from shared_functions import retry
from shared_functions import validate_title, validate_desc, validate_due_date, validate_priority

title = validate_title()
desc = validate_desc()
due_date = validate_due_date()
priority = validate_priority()

# uuid generates random 128-bit values consisting of alphanumeric characters and '-'.
# It is used to generate unique ids for each task.
# new_task is a dictionary that stores a task's details.
new_task = {
  'id': str(uuid.uuid4()),
  'title': title,
  'description': desc,
  'due_date': due_date,
  'priority': priority
}

# See the shared_functions module to understand what the retry function does.
# The lambda function delays the execution of the create_item() method until called by the retry function.
result = retry(lambda: container.create_item(new_task))

# If the variable result contained a string, that will mean an error occurred.
if not isinstance(result, str):
  print("Task created successfully.")