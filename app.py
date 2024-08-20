from dotenv import load_dotenv
import os
import pymongo
from bson import ObjectId
import argparse
from datetime import datetime

load_dotenv()

mongo_uri = os.getenv('MONGODB_URI')

client = pymongo.MongoClient(mongo_uri)
db = client.task_manager
collection = db.tasks

def add_task(name, description, due_date):
    task = {
        "name": name,
        "description": description,
        "due_date": due_date,
        "status": "pending"
    }
    result = collection.insert_one(task)
    print(f"Task added with ID: {result.inserted_id}")

def update_task(task_id, status):
    result = collection.update_one(
        {"_id": ObjectId(task_id)},  # Use ObjectId from bson
        {"$set": {"status": status}}
    )
    if result.modified_count > 0:
        print("Task updated successfully.")
    else:
        print("No task found with that ID.")

def delete_task(task_id):
    result = collection.delete_one({"_id": ObjectId(task_id)})  # Use ObjectId from bson
    if result.deleted_count > 0:
        print("Task deleted successfully.")
    else:
        print("No task found with that ID.")

def list_tasks():
    tasks = collection.find()
    for task in tasks:
        print("Document:", task)  # Debugging: Print the entire document
        task_id = task.get('_id', 'N/A')
        name = task.get('name', 'Unnamed Task')  # Use get() to avoid KeyError
        description = task.get('description', 'No description')
        due_date = task.get('due_date', 'No due date')
        status = task.get('status', 'No status')
        
        print(f"ID: {task_id}, Name: {name}, Description: {description}, Due Date: {due_date}, Status: {status}")

def main():
    parser = argparse.ArgumentParser(description="Simple Task Manager")
    parser.add_argument("--add", nargs=3, metavar=("name", "description", "due_date"), help="Add a new task")
    parser.add_argument("--update", nargs=2, metavar=("task_id", "status"), help="Update a task status")
    parser.add_argument("--delete", metavar="task_id", help="Delete a task")
    parser.add_argument("--list", action="store_true", help="List all tasks")

    args = parser.parse_args()

    if args.add:
        name, description, due_date = args.add
        add_task(name, description, due_date)
    elif args.update:
        task_id, status = args.update
        update_task(task_id, status)
    elif args.delete:
        delete_task(args.delete)
    elif args.list:
        list_tasks()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
