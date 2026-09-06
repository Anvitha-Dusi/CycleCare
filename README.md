# CycleCare - Menstrual Cycle Tracker

A beginner-friendly full-stack MERN application for personal menstrual cycle tracking and analytics.

## ⚠️ Health Disclaimer

This application is **only a personal tracking and analytics tool**. It does not provide:
- Medical diagnosis
- Pregnancy diagnosis
- Fertility diagnosis
- PCOS diagnosis
- Medical recommendations

Period predictions are estimates based on your historical data only.

## Tech Stack

### Frontend
- React 18
- Vite
- React Router
- Axios
- CSS
- Recharts

### Backend
- Node.js
- Express.js
- MongoDB
- Mongoose

### Authentication
- JWT (JSON Web Tokens)
- bcryptjs

## Project Structure

```
CycleCare/
├── client/                    # React + Vite frontend
│   ├── src/
│   │   ├── components/        # Reusable React components
│   │   │   ├── Navbar.jsx
│   │   │   └── HealthCheck.jsx
│   │   ├── pages/             # Page components
│   │   ├── services/          # API services
│   │   ├── context/           # React context
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   ├── index.html
│   ├── vite.config.js
│   └── package.json
│
├── server/                    # Express + Node backend
│   ├── config/                # Configuration
│   │   └── database.js        # MongoDB connection
│   ├── models/                # Database models
│   │   ├── User.js            # User schema
│   │   ├── Period.js          # Period schema
│   │   ├── Symptom.js         # Symptom schema
│   │   └── index.js
│   ├── routes/                # API routes (coming soon)
│   ├── controllers/           # Route controllers (coming soon)
│   ├── middleware/            # Custom middleware (coming soon)
│   ├── server.js              # Main server file
│   ├── .env                   # Environment variables
│   └── package.json
│
└── README.md
```

## Installation

### Prerequisites
- Node.js (v14 or higher)
- npm or yarn
- MongoDB (local or cloud)

### MongoDB Installation

**Option 1: Local MongoDB (Windows/Mac/Linux)**
- Download from https://www.mongodb.com/try/download/community
- Follow installation instructions
- Start MongoDB service

**Option 2: MongoDB Atlas (Cloud - Recommended for beginners)**
- Go to https://www.mongodb.com/cloud/atlas
- Create a free account
- Create a cluster
- Get your connection string and update `.env`

### Backend Setup

```bash
cd server
npm install
npm run dev
```

You should see:
```
✅ MongoDB Connected: localhost
🚀 CycleCare Backend Server running on http://localhost:5000
📝 Health check available at http://localhost:5000/api/health
🗄️  Database status available at http://localhost:5000/api/db-status
```

### Frontend Setup

```bash
cd client
npm install
npm run dev
```

You should see:
```
➜  Local:   http://localhost:3000/
```

## Testing

### Health Check
- Open http://localhost:3000 in your browser
- You should see the System Status panel
- It will show Backend and Database connection status

### Backend Endpoints

**Health Check:**
```bash
curl http://localhost:5000/api/health
```

**Database Status:**
```bash
curl http://localhost:5000/api/db-status
```

## Phase Progress

- [x] Phase 1: Project Setup
- [x] Phase 2: MongoDB & Models
- [ ] Phase 3: Authentication (JWT & bcryptjs)
- [ ] Phase 4: Period API Routes & Controllers
- [ ] Phase 5: Symptom API Routes & Controllers
- [ ] Phase 6: Dashboard & Analytics
- [ ] Phase 7: Frontend Components & Pages
- [ ] Phase 8: Styling & Responsive UI

## Features (Planned)

- [ ] User Registration
- [ ] User Login
- [ ] JWT Authentication
- [ ] Protected Routes
- [ ] Period Logging
- [ ] Period Editing/Deleting
- [ ] Symptom Logging
- [ ] Mood & Energy Tracking
- [ ] Personal Notes
- [ ] Calendar View
- [ ] Cycle History
- [ ] Average Cycle Calculation
- [ ] Estimated Next Period
- [ ] Dashboard
- [ ] Analytics & Charts
- [ ] Responsive UI

## License

MIT
