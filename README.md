# DevOps Fundamental Project - Trading / Online Marketplace

## Contents

- [Brief](#brief)
  - [Additional Requirements](#additional-requirements)
- [Architecture](#architecture)
  - [Database Structure](#database-structure)

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

## Architecture

### Database Structure

The database structure for the project is displayed using an Entity Relationship Diagram (ERD). This diagram displays the design of the tables associated with the database.

https://lucid.app/documents#/dashboard

https://lucid.app/lucidchart/97257df1-efd7-4b00-a8ff-8f5ebd8498f4/view?page=0_0#

The ERD contains two tables: User and Items. As seen in the ERD, there is a one-to-many relationship between these two tables. This is because 1 user can own many items, but 1 item can only belong to 1 owner.
