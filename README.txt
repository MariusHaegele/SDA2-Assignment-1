Microservices Setup Guide
-------------------------

This document describes how to run the microservices in Docker. Please follow the instructions carefully to get the services running successfully.


Requirements
------------
Docker Desktop should be installed and started on your computer.


Instructions
------------
1. Open Docker Desktop
Make sure that Docker Desktop is running before proceeding.

2. Open a terminal in Docker

3. Change to the "project-root" directory
cd path/to/project-root

4. Start the microservices
Execute the following command to create and start the microservices:

docker-compose up --build

This command creates and starts the Docker images and containers for the defined microservices.


After executing the command
---------------------------
After executing the docker-compose up --build command, the following Docker images and containers should be created and started:

Images:

orders_ticket
customer_info
vendorinfo
employee_info
ticket_system

Containers:

orders_ticket
customer_info
vendorinfo
employee_info
ticket_system

These microservices are now ready to receive and process CRUD requests. They can now use the endpoints of the services to interact with them.


