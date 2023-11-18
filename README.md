# Task Manager Project
Welcome to the task manager project. It is a simple python project that lets you create and store tasks in an Azure Cosmos Database. The key features of this project are:
- Create and store tasks
- Filter and read specific tasks
- Update tasks
- Delete tasks

## Table of Contents
1. [Prerequisite](#prerequisite)
2. [Installation](#installation)
3. Usage

## Prerequisite
- An Azure Subscription: if you don't have one, you can [create a free account](https://azure.microsoft.com/en-us/free) and you get free credits to use to deploy cloud resources. 
- An Azure Cosmos Database: we'll be needing the database URI and connection key.
- Install the packages in the requirements.txt file.

## Installation
1. First things first is creating the Azure Cosmos Database:
- In the search bar at the top of your azure account, type in 'cosmos' then click on 'Azure Cosmos DB'
![azure_search_bar](\images\search_cosmos.png)
- On the Cosmos DB page, click on 'create.'
![db_page](\images\create_db.png)
- The next step is choosing the API for the database account. For this project, we'll go with the NoSQL option.
![nosql_option](\images\nosql_api.png)
- Then we fill out just the 'Basic' section in the setup page. Ensure to select the 'serveless' option for the capacity mode to keep costs low.
![serverless_capacity_mode](\images\serverless.png)
- After filling the basic section, click on review+create and then create after validation is completed.

2. After DB creation process is complete, the next step is to create a connection to our DB. This will enable us store, retrieve and perform other operations on our DB. To do this, we would require the DB's Uniform Resource Identifier (URI) and the primary key:
- Head over to the DB resource you just created. At the top of your azure account, type the name of your DB account and click the resource from the results.
- By the side of the page is the resource's menu. Under 'Settings' in the resource's menu, click on Keys. Or you could type 'keys' in the littler search box at the top of the menu and click on keys.
- The resuting page contains the URI and the primary key of the current DB account. Copy them someplace safe.

3. Now you will edit the dbsetup.py file in the folder you cloned. Fill in your DB account URI and primary key in the uri and key variables respectively.
4. But before you run the Task Manager app, you need to install the packages in the requirements.txt file. Open a terminal, 'cd' to the project's directory and run the code below:
````python
pip install -r requirements.txt
````
5. Once complete, run the app with the below code in the same terminal in the project's directory:
````python
python app.py
````
\
Have fun!