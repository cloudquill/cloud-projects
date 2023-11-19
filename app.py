import subprocess

print("Welcome to your task manager.\nWhat would you like to do today:")
option = input("[1] Create a task\n")

# Create a task
while True:
  if int(option) == 1:
    subprocess.run(["python","./create_task.py"])
    break
  else:
    print('Invalid option. You can only create a task for now so please input "1".')