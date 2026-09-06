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

### Database
- MongoDB
- Mongoose

### Authentication
- JWT (JSON Web Tokens)
- bcryptjs

## Project Structure

```
CycleCare/
├── client/                 # React frontend
│   ├── src/
│   │   ├── components/    # Reusable components
│   │   ├── pages/         # Page components
│   │   ├── services/      # API services
│   │   ├── context/       # React context
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   ├── index.html
│   ├── vite.config.js
│   └── package.json
│
├── server/                # Express backend
│   ├── models/            # Database models
│   ├── routes/            # API routes
│   ├── controllers/       # Route controllers
│   ├── middleware/        # Custom middleware
│   ├── config/            # Configuration files
│   ├── server.js          # Main server file
│   ├── .env               # Environment variables
│   └── package.json
│
└── README.md
```

## Installation

### Prerequisites
- Node.js (v14 or higher)
- npm or yarn
- MongoDB (local or cloud)

### Backend Setup

```bash
cd server
npm install
npm run dev
```

The backend will run on `http://localhost:5000`

### Frontend Setup

```bash
cd client
npm install
npm run dev
```

The frontend will run on `http://localhost:3000`

## Testing the Health Check

Once both servers are running:

1. Open your browser to `http://localhost:3000`
2. You should see the CycleCare homepage
3. The health check component will automatically test the connection to the backend
4. You can also manually test: `http://localhost:5000/api/health`

## Features (Planned)

- [x] Project Structure
- [x] Basic Backend
- [x] Basic Frontend
- [ ] User Authentication
- [ ] Period Logging
- [ ] Symptom Tracking
- [ ] Calendar View
- [ ] Analytics & Charts
- [ ] Responsive UI

## License

MIT
