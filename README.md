# DevOps Fundamental Project - Online Marketplace

## Contents

- [Brief](#brief)
  - [Additional Requirements](#additional-requirements)
  - [My Approach](#my-approach)
- [Architecture](#architecture)
  - [Database Structure](#database-structure)
  - [CI Pipeline](#ci-pipeline)
- [Project Tracking](#project-tracking)
- [Risk Assessment](#risk-assessment)
- [Testing](#testing)

## Brief

The overall objective for this project is:

> - To create a CRUD application with utilisation of supporting tools, methodologies, and technologies that encapsulate all core modules covered during training.

This is to demonstrate my capability with the technologies and concepts I have been taught and assessing my development against the SFIA framework. 

### Additional Requirements

A list of the scope/requirements of this project are as follows:

> - A Trello board (or equivalent Kanban board tech) with full expansion on user stories, use cases and tasks needed to complete the project. It could also provide a record of any issues or risks that I faced creating my project.
>
> - A relational database used to store data persistently for the project, this database needs to have at least 2 tables in it, to demonstrate my understanding, I am also required to model a relationship.
>
> - Clear Documentation from a design phase describing the architecture I will use for you project as well as a detailed Risk Assessment. 
>
> - A functional CRUD application created in Python, following best practices and design principles, that meets the requirements set on my Kanban Board.
>
> - Fully designed test suites for the application I am creating, as well as automated tests for validation of the application. I must provide high test coverage in my backend and provide consistent reports and evidence to support a TDD approach.
>
> - A functioning front-end website and integrated API's, using Flask.
>
> - Code fully integrated into a Version Control System using the Feature-Branch model which will subsequently be built through a CI server and deployed to a cloud-based virtual machine.

### My Approach

For my project, I decided to create an application for a simple online marketplace which consists of:

- Login Page / Create New Account

  This is the initial starting point of the application.
  - Username field
  - Password field
  - Login button
  - Create new account button

  Creating an account and logging in with the username "admin" allows access to the admin page.

- Admin Page

  This is the page accessible by the "admin" user.
  - Logout button
  - Displays all created users
  - Edit details button for each user
    - Able to delete user along with all entries associated with that user from the database
    - Back button to return to the view of all users

- Home Page

  This is the page that every other user is automatically sent to when loggin in.
  - Logout button
  - Add new item button
  - Buy new item button
  - Display all items owned by the user
  - Drop down box and submit button to sort all items in the desired order
  - Clickable item names to allow for updating information on the chosen item

- Add New Item Page

  This is the page that allows the user to enter a new item into the database automatically assigning it to them.
  - Item name field
  - Stock field
  - Price field
  - For sale? checkbox
  - Add new item button
  - Back button

- Buy New Item Page

  This is the page that displays all the items in the database that meet the requirements: Marked as for sale, Has at least 1 in stock, and is owned by a different person to the user that is logged in.
  - Displays all the items currently for sale
  - Buy item button
    - Lowers the stock by 1 when clicked
    - If the stock level goes to 0 it is marked as no longer for sale and can no longer be seen in this page
  - Back button

- Update/Delete Item Page

  This is the page that allows for an items details to be updated. All fields are filled with the item's existing contents as default for a clearer display to the user.
  - Item name field
  - Stock field
  - Price field
  - For sale? checkbox
  - Update item details button
  - Delete button
  - Back button

## Architecture

### Database Structure

The database structure for the project is displayed using an Entity Relationship Diagram (ERD). This diagram displays the design of the tables associated with the database.

![image](https://user-images.githubusercontent.com/82821693/119006315-2c9b5400-b988-11eb-8b37-0567968ee0de.png)

The ERD contains two tables: Users and Inventory. As seen in the ERD, there is a one-to-many relationship between these two tables. This is because 1 user can own many items, but 1 item can only belong to 1 user.

### CI Pipeline

![image](https://user-images.githubusercontent.com/82821693/119286046-6778e280-bc3b-11eb-824d-7c117f60b7d3.png)

This is the Continuous Integration (CI) pipeline for this project. A flask framework was used working in conjuction with a Google Cloud Platform (GCP) Virtual Machine (VM) instance. Continuous Integration enables the development process to be more frequent and more reliable. 

This project uses a Jenkins CI server to handle the pipeline. It retrieves the code from the repository on GitHub and then performs these build instructions:
- Installing python
- Installing pip
- Installing gunicorn
- Installing all the packages in the requirements.txt file
- Creates the DATABASE_URI and the SECRET_KEY
- Runs the application

If there is a fault within the build process, the application will fail to run and the error reasoning can be easily obtained through the console output. 

Once the build is successful, the application runs using the gunicorn command. Gunicorn is a type of Web Server Gateway Interface (WSGI) HTTP server. It uses a pre-fork worker model that consists of 4 workers which is what is recommended in the Gunicorn documentation.

## Project Tracking

To track the progress of the project, Jira was used. 

https://andrewbarrett.atlassian.net/jira/software/projects/TOM/boards/1

![image](https://user-images.githubusercontent.com/82821693/119284143-ee778c00-bc36-11eb-8266-a3ec720b1c0e.png)

The Jira board uses a Kanban format that consists of 3 different columns:
- To Do
- In Progress
- Done

The cards within the board have epics assigned to them so that it is clear what the issue refers to. The epics that make up this board are:
- Documentation
  - This is referring to all the documents that was to be used in the creation of this README.
- User Stories
  - These are the implementations that correspond to a user's actions.
- Admin
  - These are the implementations that correspond to the admin actions.
- Database
  - These refer to the tables created in the database.
- Testing
  - Everything here refers to the testing processu: unit testing, integration testing, and results.
- Integration
  - This refers to the deployment of the application on GCP and Jenkins.

## Risk Assessment

![image](https://user-images.githubusercontent.com/82821693/119288666-e6bce500-bc40-11eb-92c0-deb79e86b2f3.png)

## Testing

To perform the testing for the project, pytest was used. This is true for both unit and integration testing. How this works is essentially by creating a dummy test database with preset information, performing a function, and then deleting those changes. This process is repeated for as many tests written. Results are obtained through assertion such that the output value would be something known and can be checked with the test values. By explicitly asking, it is possible for the pytest command to yield a coverage report which shows the proportion of the code that has been tested.