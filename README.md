# Fyyur - Music Venue and Artist Management Platform

Fyyur is a full-stack web application that connects venues and artists for live performances. It provides a platform for managing venues, artists, and shows, allowing users to discover and book live performances.

## Features

- Venue Management:
  - Create, edit, and delete venues
  - Search venues by name
  - View venue details including upcoming shows
  - Filter venues by city and state

- Artist Management:
  - Create, edit, and delete artists
  - Search artists by name
  - View artist details including upcoming shows
  - Artist profiles with social links and images

- Show Management:
  - Create new shows
  - View upcoming and past shows
  - Show details including artist and venue information
  - Automatic filtering of past and upcoming shows

- User Interface:
  - Modern and responsive design
  - Clear navigation between venues, artists, and shows
  - Search functionality for quick access
  - Form validation and error handling

## Tech Stack

- Backend:
  - Python 3.x
  - Flask
  - SQLAlchemy
  - PostgreSQL
  - Flask-Migrate
  - Flask-Moment

- Frontend:
  - HTML5
  - CSS3
  - JavaScript
  - Bootstrap

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd fyyur-project
```

2. Set up the database:
   - Ensure PostgreSQL is installed and running
   - Create a database named 'fyyur'
   - Configure database credentials in a `.env` file with `DATABASE_URL=postgresql://username:password@localhost:5432/fyyur`

3. Run the application:
```bash
uv run app.py
```

## Project Structure

```
fyyur-project/
├── app.py              # Main application file
├── config.py           # Configuration settings
├── models.py           # Database models
├── forms.py            # Flask-WTF forms
├── static/             # Static assets (CSS, JS, images)
├── templates/          # HTML templates
├── migrations/         # Database migration scripts
└── README.md          # This file
```