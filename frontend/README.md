Restaurant Intelligence - Developed using Python, React, Vite, Node.js, FastAPI.

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/UmairAnsari17/restaurant-intelligence.git
cd restaurant-intelligence
```

### 2. Backend Setup

```bash
cd backend
python -m venv venv
```

Activate the virtual environment:

**Windows**
```bash
venv\Scripts\activate
```

**macOS/Linux**
```bash
source venv/bin/activate
```

Install dependencies:

```bash
cd backend
pip install -r requirements.txt
```

Run the FastAPI server:

```bash
uvicorn app.main:app --reload
```

### 3. Frontend Setup

Open a new terminal:

```bash
cd frontend
npm install
npm run dev
```

The frontend will be available at:

```
http://localhost:5173
```

The FastAPI backend will be available at:

```
http://localhost:8000
```

Swagger API documentation:

```
http://localhost:8000/docs
```
