# Restaurant Booking System

### GitHub Repository

You can find the source code for this project in the GitHub repository:

[**GitHub Repository**](https://github.com/johnfurlong98/restaurant-booking-submission)


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


# Wireframes Documentation

## Overview

This section provides an overview of the wireframes for the **Restaurant Booking System**. Wireframes are essential for visualizing the layout, structure, and user interactions within the application. Below are the key wireframes that outline the primary screens and their functionalities.

## Wireframes Overview

- **Homepage**
- **Booking Creation**
- **User Registration**
- **User Login**
- **Booking List**
- **Reviews Page**

## Wireframe Screens

### 1. Homepage

![Homepage Wireframe](./images/homepage.png)

**Description:**
The homepage serves as the entry point for users. It features the navigation bar with links to key sections such as "Create a Booking," "Reviews," "Login," and "Sign Up." The main area highlights the restaurant's offerings and includes a call-to-action button for creating a new booking.

**Key Elements:**
- Navigation Bar
- Hero Section with Call-to-Action
- Overview of Services

---

### 2. Booking Creation

![Booking Creation Wireframe](./images/bookingcreation.png)

**Description:**
This screen allows users to create a new booking. The form includes fields for name, email, phone number, reservation date, number of guests, special requests, and table selection. Validation messages ensure users provide the necessary information.

**Key Elements:**
- Booking Form
- Input Fields with Labels
- Submit and Cancel Buttons
- Optional Table Selection Dropdown

---

### 3. User Signup

![User Registration Wireframe](./images/signup.png)

**Description:**
The registration page enables new users to sign up for an account. It includes fields for username, email, password, and password confirmation. Clear instructions and validation feedback guide users through the registration process.

**Key Elements:**
- Registration Form
- Input Fields with Labels
- Password Requirements
- Register and Cancel Buttons

---

### 4. My Booking 

![Booking List Wireframe](./images/mybookings.png)

**Description:**
After logging in, users can view a list of their existing bookings. Each booking entry displays key details and provides options to view, edit, or cancel the booking.

**Key Elements:**
- List of Bookings
- Booking Details (Name, Date, Guests, etc.)
- Action Buttons (View, Edit, Cancel)

---

### 5. Reviews Page

![Reviews Page Wireframe](./images/reviews.png)

**Description:**
The reviews page showcases feedback from customers. Users can read existing reviews and, if logged in, submit their own. The layout ensures readability and easy navigation through different reviews.

**Key Elements:**
- List of Customer Reviews
- Review Submission Form
- Pagination or Scroll for Multiple Reviews

---

## How to Use These Wireframes

1. **Reference During Development:** Use these wireframes as a blueprint to guide the development of each page, ensuring consistency and alignment with the initial design vision.
2. **User Feedback:** Share wireframes with stakeholders or potential users to gather feedback and make iterative improvements before full-scale development.
3. **Design Iterations:** Update wireframes as the project evolves to reflect changes in functionality or design preferences.

## Tools Used for Wireframing

- **wireframe.cc:** For creating interactive and collaborative wireframes.

## Conclusion

Documenting wireframes is a crucial step in the development process, providing a clear visual guide for both designers and developers. These wireframes ensure that the **Restaurant Booking System** delivers a user-friendly and efficient experience.

---

*Images are stored in the `./images/` directory. Ensure that all image paths are correct relative to the README file location.*



## Testing

## Django Automated Tests

### Overview

This project includes automated tests using Django's built-in testing framework to ensure the reliability and correctness of the restaurant booking application. The tests cover both **model** and **view** functionalities, verifying that critical components behave as expected.

### Test Structure

- **Model Tests**: Ensure that the data models behave correctly.
- **View Tests**: Verify that views handle requests and responses properly.

### Prerequisites

- **Python** (version 3.8 or higher recommended)
- **Django** installed and properly configured
- **Database** migrations applied

### Running the Tests

1. **Navigate to the Project Directory**:
    ```bash
    cd C:\Users\furlo\Documents\booking-system
    ```

2. **Run the Tests Using Django's Test Runner**:
    ```bash
    python manage.py test
    ```
    - This command discovers and runs all tests within your Django applications.

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
```

## Deployment on Heroku

This section provides step-by-step instructions for deploying the **Restaurant Booking System** on Heroku. Follow these steps to set up and deploy your Django application successfully.

### Prerequisites

Before deploying to Heroku, ensure the following:

- [**Heroku**] (https://booking-system-deployment-eda028bd58dc.herokuapp.com/)

- Heroku CLI is installed on your system.
- Project is fully configured and tested locally.

---

### Step-by-Step Guide

#### 1. Install Required Packages

Add necessary packages for Heroku deployment:

```bash
pip install gunicorn dj-database-url psycopg2-binary django-heroku
```

## Creating a Superuser

A **superuser** in Django has full access to the admin interface, allowing you to manage all aspects of the **Restaurant Booking System**. This includes managing users, bookings, reviews, and other critical data.

### Prerequisites

Before creating a superuser, ensure that:

- **Python** (version 3.8 or higher) is installed on your system.
- **Django** is installed and your project is properly set up.
- **Database Migrations** have been applied to set up the necessary database tables.

### Step-by-Step Guide

#### 1. Navigate to Your Project Directory

Open your terminal or command prompt and navigate to the root directory of your Django project (where `manage.py` is located).

```bash
cd C:\Users\furlo\Documents\booking-system
```

### Open terminal and run 
Step 1 
```bash
cd C:\Users\furlo\Documents\booking-system
```
Step 2 
```bash
python manage.py migrate
```
Step 3
```bash
python manage.py createsuperuser
```

- You will be prompted to enter the following information:

Username: (e.g., admin)
Email address: (e.g., admin@example.com)
Password: (Enter a strong password)
Password confirmation: (Re-enter the password)

## Known Issues and Future Improvements


## Credits
- [Django docs](https://docs.djangoproject.com/)
- Code Institute walkthroughs and community tips
- Bootstrap 5 from [https://getbootstrap.com](https://getbootstrap.com)
- chatgpt
