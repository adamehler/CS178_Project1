# Flaskapp Project

This project is intended to demonstrate the ability to host a flaskapp webpage that integrates data from RDS and a DynamoDB table. It was created to showcase basic understanding of setting up a flask application and CRUD operations.

## Description
This project utilizes a flask web application to host a web page that allows users to automatically access and mutate data within a DynamoDB table.
The data returned from DynamoDB is then joined with a database from an RDS instance using SQL.

### Features of application
* Create, Read, Update, Delete user information
* Integrated html templates for a simpler user experience
* Protected against free, potentially erroneous inputs
* Able to view list of cities and characteristics thereof for users

### Data Used
This project utilizes a world dataset which contains three tables: city, country, countrylanguage

### Tools necessary
This project required the use of an AWS EC2 instance, a DynamoDB table, and an RDS instance.

### Required packages
* Flask
* Boto3
* pymysql

Once the above are setup and credentials are correctly set, the web page can be created by running `python3 flaskapp.py`

The user can then access the EC2 instance by going to the public ip address provided, or to this address for this example: `http://54.85.116.23:8080/`
