# FastAPI Login System

## Overview
A backend login system built using FastAPI with secure password hashing and an account lock mechanism.

## Features
- User login API  
- Password hashing using bcrypt  
- Password validation (min 6 characters)  
- Account lock after 3 failed attempts  
- Automatic unlock after a short duration  

## Tech Stack
- FastAPI  
- Passlib (bcrypt)  

## Run Locally
pip install -r requirements.txt  
uvicorn main:app --reload  

## Live Demo
https://login-api-ifx5.onrender.com/docs  

## Test Credentials
username: admin  
password: 123456  

##  Endpoint
POST /login  
