#!/bin/bash
pip install -r backend/requirements.txt
cd frontend
npm install
npm run build
cd ..
PYTHONPATH=backend uvicorn backend.main:app --host 0.0.0.0 --port 8000
