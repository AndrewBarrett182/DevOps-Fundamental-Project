# DevOps Fundamental Project - Online Marketplace

## Contents

- [Brief](#brief)
  - [Additional Requirements](#additional-requirements)
  - [My Approach](#my-approach)
- [Architecture](#architecture)
  - [Database Structure](#database-structure)
- [Project Tracking](#project-tracking)

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

## Project Tracking

