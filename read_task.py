# Implement a feature to display a list of tasks.
# Allow users to view and filter tasks based on different criteria (e.g., status, due date, priority).

from dbsetup import container
from tabulate import tabulate
from shared_functions import retry, validate_priority, validate_due_date, display_tasks

# Define constants for filter options.
# This makes it easier to understand the purpose and meaning of each option within the code.
PRIORITY_FILTER = 1
DUE_DATE_FILTER = 2
KEYWORD_FILTER = 3

def create_filter_params():
  print('Filter by:\n1) Priority\t2) Due Date\t3) Keyword')

  while True:
    # The try-except block handles non-numeric inputs instead of printing errors and ending the script.
    try:
      filter_rule = int(input('Please enter your choice: '))

      if filter_rule == PRIORITY_FILTER:
        priority_value = validate_priority()
        return [priority_value, filter_rule]
      elif filter_rule == DUE_DATE_FILTER:
        due_date_value = validate_due_date()
        return [due_date_value, filter_rule]
      elif filter_rule == KEYWORD_FILTER:
        keyword_value = input('Input your keyword: ')
        return [keyword_value, filter_rule]
      else:
        print('Invalid option. Please input a number from 1-3.\n')
    except ValueError:
      print('Expecting a number input. Please input a number from 1-3.\n')

def form_query(filter_params):
  query = 'SELECT t.id, t.title, t.priority, t.due_date, t.description FROM Tasks t'

  # Query parameters are variables that store dynamic query values.
  # Using this method, the dynamic value is treated strictly as a value and not, let's say, as an SQL statement if it were inputted.
  # This prevents SQL injection attacks.
  query_param = []

  if filter_params[1] == PRIORITY_FILTER:

    # The query parameter holds a dictionary with two keys: 'name' and 'value'. 
    # The 'name' key holds the parameter name, which stands as a placeholder in the query string. '
    # The 'value' key holds the actual value that will be substituted for the parameter during query execution.
    query_param.append({'name': '@priority', 'value': filter_params[0]})
    query += ' WHERE t.priority = @priority'
  elif filter_params[1] == DUE_DATE_FILTER:
    query_param.append({'name': '@due_date', 'value': filter_params[0]})
    query += ' WHERE t.due_date = @due_date'
  elif filter_params[1] == KEYWORD_FILTER:
    query_param.append({'name': '@keyword', 'value': filter_params[0]})
    query += ' WHERE CONTAINS(LOWER(t.title), LOWER(@keyword)) OR CONTAINS(LOWER(t.description), LOWER(@keyword))' 
  
  return [query, query_param]
  
def search_db(query):

  # See the shared_functions module to understand what the retry function does.
  result = retry(lambda: list(container.query_items(
    query[0],
    query[1],
    enable_cross_partition_query=True
  )))

  return result

def read_all_tasks():
  query = 'SELECT t.id, t.title, t.description, t.due_date, t.priority FROM Tasks t'
  tasks = search_db([query, []])
  display_tasks(tasks)

def filter_tasks():
  filter_params = create_filter_params()
  query = form_query(filter_params)
  tasks = search_db(query)
  display_tasks(tasks)

if __name__ == '__main__':
  print('Would you like to: \n1) Read all tasks\t2) Filter tasks')

  while True:
    # The try-except block handles non-numeric inputs instead of printing errors and ending the script.
    try:
      read_input = int(input('Please enter your choice: '))

      if read_input == 1:
        read_all_tasks()
        break
      elif read_input == 2:
        filter_tasks()
        break
      else:
        print('Invalid choice. Please input either 1 or 2.')
    except ValueError:
      print('Expecting a number input. Please input either 1 or 2.\n')