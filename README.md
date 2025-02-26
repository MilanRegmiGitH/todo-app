**Todo App: A Full-Stack Todo Application with Next.js and FastAPI**

Features

-Task Creation: Add new tasks easily.

-Task Management: Mark tasks as completed or delete them.

-Real-time Updates: See tasks instantly with seamless frontend-backend communication.

Full-Stack Architecture: Leverages FastAPI as the backend API and Next.js for the frontend.

Tech Stack
Frontend:

Next.js: React framework for building modern web apps.
TailwindCSS: Utility-first CSS framework for fast UI design.
ShadCN/UI: Pre-designed UI components for rapid prototyping.
Backend:

FastAPI: High-performance web framework for building APIs with Python.
SQLite: Lightweight database to store tasks (for simplicity)

INSTALLATION
1. Clone the repository
```
git clone https://github.com/MilanRegmiGitH/todo-app
cd todo-app
```
3. Install frontend dependencies
```
cd frontend/frontend
npm install
```
3. Install backend dependencies
```
cd backend
pip install -r requirements.txt
```
RUNNING THE APPLICATION
1. Start the Backend
```
cd backend
uvicorn main:app --reload
```
3. Start the Frontend (Next.js)
```
cd frontend
npm run dev
```
The frontend will run on http://localhost:3000.
