# SkillBridge: Career & Skill Development Platform

SkillBridge helps a student understand their skills, find skill gaps, follow a learning roadmap, discover matching jobs, practise interviews and track progress.

SY MCA group project (Electives: AIT + React).

## Team and modules

| Member | Name | Module |
| --- | --- | --- |
| Member 1 | Prachi Valanju | Resume Analysis and Skill Gap Detection |
| Member 2 | Pradnya Bodke | Personalized Learning Roadmap and Job Recommendations |
| Member 3 | Nikita Narvekar | Mock Interview, Aptitude Assessment and Progress Tracking |

## Tech stack

- Frontend: React (Vite), React Router, Axios, lucide-react
- Backend: Django, Django REST Framework, JWT login
- Database: MySQL
- Version control: Git and GitHub

## How to run

1. Clone the repo:

```
git clone https://github.com/prachivalanju-23/Skillbridge.git
cd Skillbridge
```

2. Create the MySQL database (run in MySQL Workbench):

```
CREATE DATABASE skillbridge CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

3. Set up the backend:

```
cd backend
python -m venv venv
venv\Scripts\python -m pip install -r requirements.txt
copy .env.example .env
```

Open `backend/.env` and type your own MySQL password after `DB_PASSWORD=`. Never push this file.

```
venv\Scripts\python manage.py migrate
venv\Scripts\python manage.py seed_careers
venv\Scripts\python manage.py seed_jobs
venv\Scripts\python manage.py runserver
```

The backend runs at http://127.0.0.1:8000/

4. Start the frontend in a second terminal:

```
cd frontend
npm install
npm run dev
```

Open http://localhost:5173, register an account and log in.

## Module 2: Career Goal, Roadmap and Jobs (Pradnya Bodke)

### Features

- Career Goal page: choose one of 5 careers; the goal is saved for the logged-in user
- Learning Roadmap: ordered skills with weeks, timeline, progress and learning links; skills the student already knows are marked done
- Job Recommendations: match percentage, matched and missing skills, filter by career
- Job Details page with the skill gap

### Django apps and tables

- `roadmap`: CareerGoal (user, career) and RoadmapStep (career, order, skill, description, weeks, resource link)
- `jobs`: Job (title, company, location, type, level, category, description, apply link) and JobSkill (job, skill)
- `core` (shared by the team): Skill and Career

### API endpoints (all need a logged-in user)

| Method | Endpoint | Purpose |
| --- | --- | --- |
| GET | /api/careers/ | All careers |
| GET | /api/careers/{id}/ | One career |
| GET, POST | /api/roadmap/goal/ | Get or save the logged-in user's career goal |
| GET | /api/roadmap/career/{id}/?skills=HTML,CSS | Roadmap for a career with progress |
| GET | /api/jobs/?skills=React,HTML | All jobs, with match percentage when skills are given |
| GET | /api/jobs/{id}/?skills=React,HTML | One job, with skill gap when skills are given |

Optional filters for /api/jobs/: `category` and `level`.

### How the match percentage works

```
match % = (skills the student has that the job needs / skills the job needs) x 100
```

### Test cases

| ID | Feature | Steps | Expected result |
| --- | --- | --- | --- |
| T1 | Careers list | Log in and open the Career Goal page | 5 careers are shown |
| T2 | Career selection | Click a career card | Card shows a check mark and the choice is saved |
| T3 | Roadmap progress | Choose Full Stack Developer, enter HTML, CSS, JavaScript | 3 of 9 steps done, 33% |
| T4 | Roadmap weeks | Same as T3 | Remaining steps show start and end weeks |
| T5 | Job match | Jobs page, enter React, JavaScript, HTML, CSS, Git | Junior React Developer shows 100% match |
| T6 | Skill gap | Open a job from the match list | Missing skills are shown in red |
| T7 | Career filter | Jobs page, choose a career category | Only jobs of that career are shown |
| T8 | Login required | Open /api/careers/ without logging in | 401 Authentication credentials were not provided |
| T9 | Invalid job id | Log in and open /api/jobs/9999/ in the app | 404 Not found |
| T10 | No career chosen | Open Roadmap before choosing a career | Message asking the student to choose a career |