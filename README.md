# web-programming-assignments

Hi there! This repo consists of snippets of work that I have done for my school assignments (specifically, ICT239). The main languages used are javascript and python through the use of the flask flamework, with the use of HTML and CSS for the HTML views.

Here is a short description of what is in this repo:
## A basic chat application
#### Question 1 - barebones static chat application [Link](Jan_2019_Web_Programming/q1)
- A static chat application.
- A button was created to allow input of new chats, with attributes such as Name, Status and Message
- 2 buttons were created that allows CSS design changes to parts of the chat history
- Utilized: HTML, CSS, Javascript

#### Question 2 - Using Flask and the MVC framework for implementation [Link](Jan_2019_Web_Programming/q2)
- Changed the functionality of the buttons
- Addition of a REST web API (Flask API)
- Conversation data stored in a Python dictionary
- AJAX call using jQuery to change list attributes
- Utilized: HTML, CSS, Javascript, jQuery, Python, Flask framework

## A simple reporting dashboard 
#### Question 3 - Simple table showing report results [Link](Jan_2019_Web_Programming/q3)
- Creation of a basic table to show limited number of results on the dashboard's first page
- A button to load the next 10 records when clicked
- Sorting via clicking of table headers
- Delete feature via a checkbox
- Utilized: HTML, CSS, Javascript, jQuery, Python, Flask framework

#### Question 4 - Chart with visualization [Link](Jan_2019_Web_Programming/q4)
- An add on to question 3
- A visual interactive line chart to show different types of data
- A visual stacked bar charts to show specific data
  - Note: Due to being unfamiliar with javascript at the time, although I was able to generate the results on the backend through Flask, I was unable to convert the data sent to the HTML view into the correct format to be read by the ChartJS library.
- Utilized: HTML, CSS, Javascript, jQuery, Python, Flask framework, ChartJS Library

## A simple video streaming website
#### ECA Question 1 - Static video "Home Page" [Link](Jan_2019_Web_Programming/ECA/Q1)
- An add on to question 3
- Static HTML + CSS page to create a structured home page layout for video elements and any other information (EG: Terms of use, Banners, details)
- Made site mobile friendly as well
- Creation of an advertisement banner at the top section
- Dynamic auto-play video feature when user hovers over videos
- Profile information pop up
- Utilized: HTML, CSS, Javascript

#### ECA Question 2 - Changing Question 1 to use the Flask Framework [Link](Jan_2019_Web_Programming/ECA/Q2)
- Models were designed to keep information about
  - Registered users
  - Video posts
  - User profile information
  - Banner advertisments
- A HTML template was created to replace the static HTML in ECA Question 1
- A registration interface and controller was added to allow registration of new users.
- A login interface and controller was also added. This includes locking of an account after repeated incorrect password attempts.
- Utilized: HTML, CSS, Javascript, jQuery, Python, Flask framework

#### ECA Question 3 - Implementation of a video posting interface [Link](Jan_2019_Web_Programming/ECA/Q3)
- A "Post Video" interface and controller was added to alow upload of video clips
  - Users can also add in a video description to be shown
  - Video information are stored in a SQLite database (EG: Filepath, filename)
- To modify existing videos, an "Edit Video" interface and controller was also added.
- Users can also update their profile via the "Edit Profile" interface and controller.
- Videos exceeding 50mb cannot be uploaded.
- Utilized: HTML, CSS, Javascript, jQuery, Python, Flask framework, SQLite, SQLAlchemy ORM

#### ECA Question 4 - Reporting backend admin dashboard[Link](Jan_2019_Web_Programming/ECA/Q4)
- Line charts were used to showcase data such as
  - Number of videos posted by each user
  - Storage used by each user
  - Advertisment statistics
- Utilized: HTML, CSS, Javascript, jQuery, Python, Flask framework, SQLite, SQLAlchemy ORM, ChartJS Library