# SurgiTrack

**SurgiTrack** is a Flask-based web application designed for junior doctors and surgical trainees to log operative cases and access educational resources. Built as part of the CS50X final project, the app aims to improve surgical training by offering a lightweight alternative to bloated logbook systems.

🎥 [Video Demo](https://www.youtube.com/watch?v=0l37zi-uJw4)

---

## Why SurgiTrack?

As a surgical registrar in the UK, I created SurgiTrack to address two specific needs I faced during training:

- 🧾 A simplified **logbook system** for tracking operative experience
- 📚 Access to **educational templates** for consent forms and operation notes

Many existing systems are overly complex. SurgiTrack provides a clean, user-friendly alternative that lets trainees log procedures and monitor case tallies over time.

---

## Features

- ✅ Add and delete operations to maintain a clean, custom logbook
- 📊 View tallied counts by operation type
- 📝 Access templates for consent and operation notes
- 🎥 Embedded videos and interactive quizzes on common operations to test understanding
- 👥 User authentication (register/login/logout)
- 🌐 Responsive layout with Bootstrap + custom styling

---

## Tech Stack

- Python, Flask
- SQLite for data storage
- HTML, CSS (Bootstrap), Jinja2
- JavaScript (for quiz interactions)

---


---

## Database Schema

- **users**: `id`, `username`, `hash`
- **operations**: `id`, `user_id`, `date`, `name`, `mode`, `supervision`, `hospital`

---

## Getting Started

1. Clone the repo:
   ```bash
   git clone git@github.com:amg-ai-labs/surgitrack.git
   cd surgitrack

2. Install dependencies: 
    ```bash
    pip install -r requirements.txt
   
3. Run the app: 
    ```bash
   flask run

Then open http://127.0.0.1:5000 in your browser.
