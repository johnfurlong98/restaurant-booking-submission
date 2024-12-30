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
- Heroku (deployment)

## Data Models
1. **Booking**: (id, user, name, email, phone, reservation_date, number_of_guests, special_requests, created_on)
2. **Review**: (id, user, title, content, rating, created_on)

## Testing
- We have basic Django unit tests in `reservations/tests.py`.
- Manual testing includes verifying success messages upon creating/updating/deleting bookings and reviews.

## End-to-End (E2E) Tests with Jest & Puppeteer

### Overview

This project utilizes **Jest** and **Puppeteer** to perform automated end-to-end (E2E) tests. These tests ensure that key functionalities of the restaurant booking application work as expected, enhancing both usability and reliability.

### Prerequisites

- **Node.js** (version 18 or higher recommended)
- **npm** (comes with Node.js)
- **Django server** running locally (`http://localhost:8000`)

### Installation

1. **Install Node Dependencies**:
    ```bash
    npm install
    ```

2. **Install Jest and Puppeteer**:
    ```bash
    npm install --save-dev jest puppeteer
    ```

### Running the Tests

1. **Start the Django Server**:
    ```bash
    python manage.py runserver
    ```

2. **Run Jest Tests** (in a separate terminal):
    ```bash
    npm test
    ```

### What the Tests Do

- **Load the Homepage**: Verifies that the homepage loads successfully and checks the page title.
- **Check Navigation Links**: Confirms the presence of essential links like "Make a Booking."
- **Responsive Design**: Tests the application's responsiveness by simulating different viewport sizes.

### Troubleshooting

- **No Tests Found**:
  - Ensure your test files are named with `.test.js` or `.spec.js` extensions.
  - Place test files inside a `__tests__` directory or configure Jest to recognize your test paths.

- **Timeout Errors**:
  - Increase Jest’s default timeout by adding `jest.setTimeout(30000);` at the top of your test file.

- **Server Issues**:
  - Make sure the Django server is running before executing the tests.
  - Verify that the base URL in your tests (`http://localhost:8000`) matches your server’s address.

### Customizing Tests

For debugging purposes, you can run Puppeteer in non-headless mode by modifying the `puppeteer.launch` options in your test file:

```javascript
browser = await puppeteer.launch({
  headless: false, // Set to false to see the browser
  slowMo: 50,       // Slows down Puppeteer operations by 50ms
});


## Deployment
1. Use `requirements.txt` and `Procfile` if deploying to Heroku.
2. Set `DEBUG=False` in environment for production.
3. Document your steps for the assessor.

## Credits
- [Django docs](https://docs.djangoproject.com/)
- Code Institute walkthroughs and community tips
- Bootstrap 5 from [https://getbootstrap.com](https://getbootstrap.com)
