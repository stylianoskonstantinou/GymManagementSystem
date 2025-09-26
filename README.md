# Gym Management System

## About

Gym Management System developed in Python with PostgreSQL backend. It offers essential features for managing gym members, subscriptions, attendance, and membership status through an easy-to-use graphical interface. Designed to simplify gym operations and improve administrative efficiency.

## Features

- Add, update, and delete gym members.
- Manage multiple subscription types with start and end dates.
- Track member attendance and generate attendance summaries.
- Search members by surname or subscription type.
- User-friendly graphical interface built with Tkinter.
- Reliable backend using PostgreSQL database.

## Technology Stack

- Python 3.x
- psycopg2-binary
- Tkinter (GUI)
- PostgreSQL

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/stylianoskonstantinou/GymManagementSystem.git
   cd GymManagementSystem
   ```

2. Install Python dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up the PostgreSQL database:
   - Import the schema from `gym_database.sql`.
   - Update the database connection credentials in `gym_app.py` before running the application.

4. **Note:** Tkinter comes pre-installed with most Python distributions.  
   - For Linux, you may need to install it separately:
     ```
     sudo apt-get install python3-tk
     ```

## Configuration

Edit the database connection in `gym_app.py`:

```
conn = psycopg2.connect(
    host="your_host",
    port="5432",
    dbname="your_database",
    user="your_username",
    password="your_password"
)
```

Make sure not to upload your real credentials to any public repositories.

## Usage

Run the application:

```
python gym_app.py
```

Use the GUI to add members, manage subscriptions, track attendance, and generate reports.

## Author
Stylianos Konstantinou
Postgraduate student in Applied Informatics, Department of Electrical and Computer Engineering, University of Thessaly.
[8](https://www.reddit.com/r/programming/comments/cfeu99/readme_template_i_use_for_most_of_my_projects/)
[9](https://www.youtube.com/watch?v=12trn2NKw5I)
[10](https://gitlab.com/ton1czech/project-readme-template)
