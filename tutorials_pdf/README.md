# 🏠 Airbnb Clone Project – Full Stack Back End Implementation

## 🚀 Project Overview

This project is a full-stack web application inspired by Airbnb, focused on implementing the core features such as user authentication, property listings, bookings, payments, and user reviews. It emphasizes scalability, security, and modular backend architecture.

---

## 🎯 Project Goals

- Secure user registration and authentication
- Property listing creation and management
- Property reservation and booking system
- Payment processing integration
- Review and rating system
- Optimized data storage with relational integrity

---

## 🛠️ Technology Stack

- **Django** – REST API backend
- **PostgreSQL** – Relational database
- **GraphQL** – Flexible querying
- **Celery** – Asynchronous task queue
- **Redis** – Caching layer for performance
- **Docker** – Containerized development & deployment

---

## 🗃️ Database Design (Normalized: 1NF, 2NF, 3NF)

### 📌 User Table

| Column        | Type      | Constraint                      |
|---------------|-----------|----------------------------------|
| `user_id`     | UUID      | Primary Key, Indexed            |
| `first_name`  | VARCHAR   | Not Null                        |
| `last_name`   | VARCHAR   | Not Null                        |
| `email`       | VARCHAR   | Unique, Not Null                |
| `password_hash` | VARCHAR | Not Null                        |
| `phone_number`| VARCHAR   | Nullable                        |
| `role`        | ENUM      | guest, host, admin – Not Null   |
| `created_at`  | TIMESTAMP | Default: CURRENT_TIMESTAMP      |

### 🏘️ Property Table

| Column         | Type      | Constraint                          |
|----------------|-----------|--------------------------------------|
| `property_id`  | UUID      | Primary Key, Indexed                |
| `host_id`      | UUID      | Foreign Key → User(`user_id`)       |
| `name`         | VARCHAR   | Not Null                            |
| `description`  | TEXT      | Not Null                            |
| `location`     | VARCHAR   | Not Null                            |
| `pricepernight`| DECIMAL   | Not Null                            |
| `created_at`   | TIMESTAMP | Default: CURRENT_TIMESTAMP          |
| `updated_at`   | TIMESTAMP | Auto-updated on record modification|

### 📆 Booking Table

| Column        | Type      | Constraint                          |
|---------------|-----------|--------------------------------------|
| `booking_id`  | UUID      | Primary Key, Indexed                |
| `property_id` | UUID      | Foreign Key → Property(`property_id`)|
| `user_id`     | UUID      | Foreign Key → User(`user_id`)       |
| `start_date`  | DATE      | Not Null                            |
| `end_date`    | DATE      | Not Null                            |
| `total_price` | DECIMAL   | Not Null                            |
| `status`      | ENUM      | pending, confirmed, canceled – Not Null |
| `created_at`  | TIMESTAMP | Default: CURRENT_TIMESTAMP          |

### 💳 Payment Table

| Column         | Type      | Constraint                          |
|----------------|-----------|--------------------------------------|
| `payment_id`   | UUID      | Primary Key, Indexed                |
| `booking_id`   | UUID      | Foreign Key → Booking(`booking_id`) |
| `amount`       | DECIMAL   | Not Null                            |
| `payment_date` | TIMESTAMP | Default: CURRENT_TIMESTAMP          |
| `payment_method` | ENUM    | credit_card, paypal, stripe – Not Null |

### 🌟 Review Table

| Column       | Type    | Constraint                                |
|--------------|---------|--------------------------------------------|
| `review_id`  | UUID    | Primary Key, Indexed                      |
| `property_id`| UUID    | Foreign Key → Property(`property_id`)     |
| `user_id`    | UUID    | Foreign Key → User(`user_id`)             |
| `rating`     | INTEGER | CHECK: 1 <= rating <= 5, Not Null         |
| `comment`    | TEXT    | Not Null                                  |
| `created_at` | TIMESTAMP | Default: CURRENT_TIMESTAMP              |

### 💬 Message Table

| Column         | Type      | Constraint                          |
|----------------|-----------|--------------------------------------|
| `message_id`   | UUID      | Primary Key, Indexed                |
| `sender_id`    | UUID      | Foreign Key → User(`user_id`)       |
| `recipient_id` | UUID      | Foreign Key → User(`user_id`)       |
| `message_body` | TEXT      | Not Null                            |
| `sent_at`      | TIMESTAMP | Default: CURRENT_TIMESTAMP          |

---

## 🔐 API Security

- **Authentication**: JWT tokens for identity verification
- **Authorization**: Role-based access control (guest, host, admin)
- **Rate Limiting**: Prevents abuse with request caps
- **Encryption**: HTTPS + password hashing for data security

---

## 🔁 CI/CD Pipeline

- **GitHub Actions**: Automates test and build processes
- **Docker**: Ensures consistent environments from dev to production

---

## 👥 Team Roles

| Role              | Responsibilities                                         |
|-------------------|----------------------------------------------------------|
| Backend Developer | Builds API endpoints, integrates database logic          |
| Database Admin    | Designs schema, enforces constraints & performance tuning|
| DevOps Engineer   | Manages Docker environments and deployment pipelines     |
| Security Specialist | Implements API and data-layer security best practices  |
| Project Manager   | Organizes team tasks and delivery timelines              |

---

## ✨ Feature Breakdown

- **User Management**: Secure signup, login, profile editing
- **Property Listings**: Host-managed property creation and updates
- **Bookings**: Users reserve properties with date validation
- **Payments**: Connected to bookings with supported payment methods
- **Reviews**: Verified bookers can post one review per property
- **Messaging**: Secure user-to-user communication system

---

## 📈 Indexing Strategy

- **Primary Keys**: Indexed by default
- **Additional Indexes**:
  - `email` in `User`
  - `property_id` in `Property` and `Booking`
  - `booking_id` in `Booking` and `Payment`

---

## 📌 Example Normalization

- **1NF**: All fields contain atomic values (e.g., no multiple phone numbers in one field)
- **2NF**: All non-key attributes depend on the whole primary key (e.g., no partial dependencies)
- **3NF**: No transitive dependencies (e.g., `user` role is not inferred from name or email)

---

## 🔗 Links

- GitHub Profile: [github.com/awaaat](https://github.com/awaaat)  
- LinkedIn Profile: [linkedin.com/in/allan-w-96956a15a](https://www.linkedin.com/in/allan-w-96956a15a/)

---

## 📢 Social Post

> I just revamped my GitHub and LinkedIn to reflect all the amazing backend work I've been doing on the #AirbnbClone project! 🏡 From secure APIs to normalized relational models, this is a full-stack experience in action.  
>  
> Check it out 👉 [GitHub](https://github.com/awaaat) | [LinkedIn](https://www.linkedin.com/in/allan-w-96956a15a/)  
>  
> #ALX_SE #ALX_BE #BackendDevelopment @alx_africa

---

Let me know if you'd like a badge section, live deployment link, or ERD visual!

# link to the ERD
https://drive.google.com/file/d/1PwSq0O0LeBRJF-aFm77_2HeMh6nltJZz/view?usp=sharing 