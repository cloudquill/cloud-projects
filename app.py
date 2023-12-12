import subprocess

print("Welcome to your task manager.\nWhat would you like to do today:")

while True:
  try:
    option = int(input("1) Create a task\t2) Read tasks\t3) Update a task\n"))
    if option == 1:
      subprocess.run(["python","./create_task.py"])
      break
    elif option == 2:
      subprocess.run(['python', './read_task.py'])
      break
    elif option == 3:
      subprocess.run(['python', './update_task.py'])
      break
    else:
      print('Invalid option. Please input a number from the range 1-3.')
  except ValueError:
    print('Expecting a number input. Please input either 1 or 2.\n')
