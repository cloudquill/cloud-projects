from dbsetup import container
from shared_functions import retry, validate_priority, validate_due_date, validate_title, validate_desc, validate_keyword, display_tasks

# These constants are simply indicators for what field is being edited instead of using magic numbers.
TITLE, PRIORITY, DUE_DATE, DESCRIPTION = '1', '2', '3', '4'

def keyword_search():
  while True:
    keyword = validate_keyword()

    # This query pulls the a task's id, title, description, priority and due date if its title or description contains the search keyword
    query = '''
      SELECT t.id, t.title, t.description, t.priority, t.due_date 
      FROM Tasks t 
      WHERE CONTAINS(LOWER(t.title), LOWER(@keyword)) OR CONTAINS(LOWER(t.description), LOWER(@keyword))
    '''
    query_params = [{'name': '@keyword', 'value': keyword}]

    # The database is queried.
    query_result = retry(lambda: list(container.query_items(
      query,
      parameters=query_params,
      enable_cross_partition_query=True
    )))
    
    if len(query_result) > 0:
      return query_result
    else:
      print('No results for that keyword. Please input another.')

def task_to_update(search_result):
  # Arranges each task information in a neat table.
  display_tasks(search_result)

  while True:
    task_to_update_id = input('Please paste the task id you wish to update: ')
    
    for item in search_result:
      # If pasted id is in search results, return the task information for that task id.
      if task_to_update_id == item['id']:
        return item
    
    print('Invalid item id. Please copy and paste the item id from the list shown.')

def update_field():
  while True:
    field_to_edit = input('1) Title\n2) Priority\n3) Due Date\n4) Description\nPlease input the field number to update: ')

    if field_to_edit == TITLE:
      new_value = validate_title()
      return ['title', new_value]
    elif field_to_edit == PRIORITY:
      new_value = validate_priority()
      return ['priority', new_value]
    elif field_to_edit == DUE_DATE:
      new_value = validate_due_date()
      return ['due_date', new_value]
    elif field_to_edit == DESCRIPTION:
      new_value = validate_desc()
      return ['description', new_value]
    else:
      print('Sorry, that field number is invalid. Please choose from the range 1-4.')

def update_task(task_to_update_dict, updated_field_value):
  # When updating the priority field of a task, treating it as a new entry occurs because 
  # the priority is the partition key. Consequently, if the priority is edited, there will 
  # be two tasks with the same ID but different priority values. As a result, it is necessary 
  # to delete the initial task before updating any task whose priority was edited.
  if updated_field_value[0] == 'priority':
    retry(lambda: container.delete_item(
      task_to_update_dict['id'], 
      partition_key=task_to_update_dict['priority']
    ))
  
  # The task field to be updated is set to its new value and sent to the database.
  task_to_update_dict[updated_field_value[0]] = updated_field_value[1]
  retry(lambda: container.upsert_item(task_to_update_dict))
  print("task updated successfully.")

if __name__ == '__main__':
  search_result = keyword_search()
  task_to_update_dict = task_to_update(search_result)
  updated_field_value = update_field()
  update_task(task_to_update_dict, updated_field_value)