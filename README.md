# ArenaGuide

ArenaGuide is a Saudi national digital platform designed to transform the way people experience stadiums, matches, and large-scale sports events. The platform aims to enhance fan engagement, streamline booking processes, and support efficient crowd management through a unified, intelligent system.

## Overview

ArenaGuide provides a modern solution for discovering stadiums, booking matches, and managing event-related services within a single platform. It is built to elevate the overall match-day experience by making it more organized, accessible, and enjoyable for users.

The platform also plays a strategic role in supporting Saudi Arabia’s growing sports sector by improving tourism experiences, optimizing crowd flow, and contributing to the successful hosting of major international events, including the FIFA World Cup 2034.

## Vision and Impact

ArenaGuide aligns with national digital transformation goals by offering a scalable solution that:

- Enhances sports tourism by providing seamless access to stadiums and events  

- Improves crowd management through structured booking and user flow  

- Elevates the fan experience before, during, and after matches  

- Supports large-scale event hosting with organized and efficient systems  

- Contributes to Saudi Arabia’s readiness for global sporting events  

## Core Features

- Multilingual support (Arabic and English) using Django i18n  

- Secure user authentication and account management  

- Stadium discovery with detailed information  

- Booking system for matches and stadium access  

- Administrative dashboard for system control  

- Notification system for updates and alerts  

- Support module for handling user inquiries  

## Architecture

The application is built using Django with a modular architecture. Each functional domain is separated into independent apps, improving scalability, maintainability, and development efficiency.

## Project Structure

ArenaGuide/

│

├── account/        # User authentication and profile management  

├── booking/        # Booking workflows and logic  

├── dashboard/      # Administrative interfaces  

├── match/          # Match management  

├── notification/   # Notifications and alerts  

├── service/        # Additional services  

├── stadium/        # Stadium data and browsing  

├── support/        # User support system  

├── core/           # Shared core functionality  

├── locale/         # Translation files  

├── manage.py

## Installation and Setup

Clone the repository and navigate into the project directory:

git clone https://github.com/Reem-Almezeal/ArenaGuide.git 
cd ArenaGuide  

Create and activate a virtual environment:

python -m venv venv  
source venv/bin/activate  
venv\Scripts\activate  

Install dependencies:

pip install -r requirements.txt  

Apply database migrations:

python manage.py migrate  

Run the development server:

python manage.py runserver  
   
## Future Enhancements

- Deployment to cloud platforms such as Azure or AWS  
- Integration of payment gateways  
- UI/UX improvements for better user experience  
- Implementation of real-time features (e.g., live notifications)  

## Project Documentation

This section includes the main analysis and design documents prepared for ArenaGuide.

- Class Diagram: [View Class Diagram](link)
- Case Study: [View Case Study](link)
- Wireframe: [View Wireframe](link)

## Authors

Eng.Reem Almezeal
Eng.Atheer   
