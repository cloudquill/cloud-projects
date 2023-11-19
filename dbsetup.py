from shared_functions import retry
from azure.cosmos import CosmosClient, PartitionKey

# Establish connection to CosmosDB account
uri = "xxxxxxxxxxxxxxxxxxxxxxxxxx"
key = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
client = retry(lambda: CosmosClient(uri, key))

# Create a database that will store the tasks and get a reference to it
db_name = 'Task Manager'
database = retry(lambda: client.create_database_if_not_exists(id=db_name))

# Create a container and set the partition key
container_name = 'Tasks'
key_path = PartitionKey(path='/priority')
container = retry(lambda: database.create_container_if_not_exists(id=container_name, partition_key=key_path))