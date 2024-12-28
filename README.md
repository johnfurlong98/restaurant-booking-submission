# Improved Restaurant Booking System

A Django-based web application allowing customers to:
- Register, log in, and log out
- Create, view, update, and delete restaurant bookings
- View, add, and delete reviews (custom second model)
- Receive immediate feedback messages on all CRUD operations

## Table of Contents
1. [Project Purpose](#project-purpose)
2. [Features](#features)
3. [User Stories](#user-stories)
4. [Agile Approach](#agile-approach)
5. [Technologies](#technologies)
6. [Data Models](#data-models)
7. [Testing](#testing)
8. [Deployment](#deployment)
9. [Credits](#credits)

---

## Project Purpose
- **External Users**: Quickly book a table and provide feedback/review.
- **Restaurant Owner**: Manage bookings & see user reviews in real-time.

## Features
1. **User Registration & Auth**: Based on Django’s built-in system.
2. **CRUD Bookings**: Create, read, update, delete booking records from the front-end.
3. **CRUD Reviews**: Create & delete simple reviews about the restaurant.
4. **Bootstrap**-styled templates.
5. **Success/Failure** messages for user feedback.

## User Stories
- “As a new visitor, I can register an account so that I can log in and create a booking.”
- “As a logged-in user, I can create a booking so that I can reserve a table.”
- “As a logged-in user, I can edit or cancel my booking if my plans change.”
- “As any user, I can leave a quick review so that I can share my experience with others.”
- “As an admin, I can access the admin panel to manage everything behind the scenes.”

## Agile Approach
- We used a [GitHub Project Board](https://github.com/USERNAME/improved_restaurant_booking/projects/1) with Epics (Bookings, Reviews, Deployment), user stories, and tasks.
- Tasks are broken down into sub-issues or checklists inside stories.

## Technologies
- Django 4.2
- Python 3.9+
- Bootstrap 5 (CDN)
- Gunicorn (production server)
- SQLite (dev)
- Heroku / Other (optional deployment)

## Data Models
1. **Booking**: (id, user, name, email, phone, reservation_date, number_of_guests, special_requests, created_on)
2. **Review**: (id, user, title, content, rating, created_on)

## Testing
- We have basic Django unit tests in `reservations/tests.py`.
- Manual testing includes verifying success messages upon creating/updating/deleting bookings and reviews.

## Deployment
1. Use `requirements.txt` and `Procfile` if deploying to Heroku.
2. Set `DEBUG=False` in environment for production.
3. Document your steps for the assessor.

## Credits
- [Django docs](https://docs.djangoproject.com/)
- Code Institute walkthroughs and community tips
- Bootstrap 5 from [https://getbootstrap.com](https://getbootstrap.com)
