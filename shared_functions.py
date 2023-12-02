import re
import time
import calendar
from datetime import datetime
from tabulate import tabulate
from azure.core.exceptions import ServiceRequestError, ServiceResponseError
from requests.exceptions import ConnectionError, RequestException
from azure.cosmos.exceptions import CosmosHttpResponseError, CosmosResourceNotFoundError

# The retry function lets us execute, retry and control the execution of a function if it fails.
# If a function fails to run successfully, it is executed again a maximum of three times with a 5 secnd delay between each retry.
def retry(function, max_attempts=3, delay=5):
    for attempt in range(1, max_attempts + 1):
        try:
            result = function()
            return result
        except (ValueError, ServiceRequestError) as e:
            print(f'There is a problem: {str(e)}')
        except ConnectionError:
            print('Connection error: Unable to establish connection to the container.')
        except CosmosHttpResponseError as e:
            print('An error occurred during the query execution: ', str(e))
        except CosmosResourceNotFoundError as e:
            print("The specified resource was not found:", str(e))
        except (RequestException, ServiceResponseError) as e:
            print(f'An error occured while making the request to the container: {str(e)}')
        
        if attempt < max_attempts:
            print(f'\nRetrying in {delay} seconds...')
            time.sleep(delay)
    
    raise Exception("Maximum number of attempts reached without a successful result.")

def validate_title():
  while True:
    title = input('Task Name: ').strip()
  
    if len(title) == 0:
      print('Title cannot be empty.')
    elif len(title) > 70:
      print('Title cannot be more than 70 characters long.')
    
    # ^[\w .'-]+$ expression matches one or more occurences of alphanumeric characters, spaces and ".-'"
    elif not re.match(r"^[\w .,/!?'-]+$", title):
      print('Title can only have alphanumeric characters, spaces and ".\'-"')
    else:
      return title
    
def validate_desc():
  while True:
    desc = input('Task Description (optional): ')
    
    # This expression matches zero or more occurrences of the enclosed characters so it will match an empty input.
    if re.match(r'^[\w .,/+!?"]*$', desc):
      return desc
    else:
      print('Your description contains disallowed characters. Only alphanumeric characters, spaces and specific punctuation marks are allowed.')

def validate_due_date():
  while True:
    due_date_str = input('Due Date (DD/MM/YYYY): ')
    
    # The regular expression pattern is used to match due date in the format 
    # "DD/MM/YYYY". \d{2} matches two digits for the day and month while \d{4} 
    # is for the year. 
    # '/' matches a forward slash
    date_pattern = r'\d{2}/\d{2}/\d{4}'
    
    # Gets and stores today's date as a date object
    current_date = datetime.today().date()
    
    if re.match(date_pattern, due_date_str):
      
      # Split due_date into three using '/' as the delimiter and converting 
      # each component into integers and assigning them to day, month and year 
      # respectively.
      day, month, year = map(int, due_date_str.split('/'))
      
      if not (1 <= day <= 31 and 1 <= month <= 12):
        print("Invalid day or month.")
      else:
        
        # calendar.monthrange(year, month) represents a tuple containing the 
        # weekday of the first day of the month and the number of days in that 
        # month. So the if statement checks if 'day' is more than the total 
        # days in the specified month.
        if day > calendar.monthrange(year, month)[1]:
          print(f'Invalid day for {calendar.month_name[month]}.')
        else:
          
          # Converts due_date_str from a string to a date object so it is possible to compare with current date.
          due_date = datetime.strptime(due_date_str, '%d/%m/%Y').date()
          
          if due_date < current_date:
            print('Date cannot be in the past.')
          else:
            return due_date_str
    else:
      print('Date format is incorrect.')

def validate_priority():
  while True:
    priority = input('Priority (High, Medium or Low): ').lower()
    priority_options = ['high', 'medium', 'low']
  
    if len(priority.strip()) == 0:
      print('Priority cannot be empty.')
    elif priority not in priority_options:
      print('Invalid priority. Please choose from: High, Medium or Low.')
    else:
      return priority

def validate_keyword():
  while True:
    keyword = input('Input the search keyword: ')
    keyword_pattern = r'^[\w .,/_+!?"]+$'

    if re.match(keyword_pattern, keyword):
      return keyword
    else:
      print('Your keyword contains disallowed characters. Only alphanumeric characters, space and these puctuations (.,/_+!?") are allowed.')

def display_tasks(data):
  print(tabulate(
    [[item['id'], item['title'], item['priority'], item['due_date'], item['description']] for item in data],
    headers=['Id', 'Title', 'Priority', 'Due Date', 'Description']
  ))