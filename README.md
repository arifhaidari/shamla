# Shamla - Afghan Clothing Brand E-commerce Platform

**Shamla** is an Afghan clothing brand's official website, created to showcase and sell high-quality Afghan apparel. This Django-based project aims to provide a seamless e-commerce experience while managing the intricate details of running an online clothing business. Whether it's processing orders, managing content, or handling payments, Shamla is designed to be a robust solution tailored for the fashion industry.

Note: some part of the project is omitted for business/sensitive data

---

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Admin Panel](#admin-panel)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

---

## Project Overview

**Shamla** is not just an e-commerce platform; it's the digital representation of the Shamla Atelier, a brand synonymous with traditional Afghan fashion. The website is designed to cater to both customers and administrators by offering a wide range of features from product browsing and payment processing to order management and blog publishing.

---

## Features

### 1. **User-Friendly Interface**

- A clean and intuitive interface for customers to browse through a collection of Afghan clothing.
- Responsive design ensures a seamless shopping experience on both desktop and mobile devices.

### 2. **Newsletter & Mailchimp Integration**

- Built-in newsletter functionality allowing customers to subscribe and stay updated with the latest products and offers.
- Integrated with Mailchimp for managing email campaigns.

### 3. **Order Processing**

- Secure and efficient order processing system.
- Customers can easily add items to the cart, proceed to checkout, and receive confirmation upon successful purchase.

### 4. **Comprehensive Admin Panel**

- A powerful admin panel for managing products, orders, customer data, and website content.
- Features user role management, allowing different levels of access.

### 5. **Blog**

- Integrated blog system to publish articles, news, and updates about Afghan fashion and the Shamla brand.
- Supports rich text and media content.

### 6. **Cart & Payment Gateway**

- A robust cart system where customers can review their selected items before purchasing.
- Integration with multiple payment gateways for secure transactions.
- Option for payment upon submission.

### 7. **Search & Filtering**

- Advanced search functionality allowing users to quickly find products by category, size, color, or price.

### 8. **Analytics**

- Built-in analytics to track user behavior, sales data, and website performance.

---

## Technology Stack

- **Backend:** Django (Python)
- **Frontend:** HTML, CSS, JavaScript, Bootstrap
- **Database:** PostgreSQL (or SQLite for development)
- **Payment Gateway:** Stripe and Custom
- **Email Campaigns:** Mailchimp
- **Analytics:** Custom

---

## Installation

### Prerequisites

Ensure you have the following installed on your system:

- Python 3.x
- pip (Python package installer)
- PostgreSQL (or SQLite for local development)
- Virtualenv (optional but recommended)

### Steps

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/arifhaidari/shamla.git
   cd shamla
   ```

2. **Create a Virtual Environment:**

   ```bash
   python3 -m venv env
   source env/bin/activate
   ```

3. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the Database:**

   Update `settings.py` with your database credentials.

   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'shamla_db',
           'USER': 'your_username',
           'PASSWORD': 'your_password',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

5. **Run Migrations:**

   ```bash
   python manage.py migrate
   ```

6. **Create a Superuser:**

   ```bash
   python manage.py createsuperuser
   ```

7. **Start the Development Server:**

   ```bash
   python manage.py runserver
   ```

8. **Access the Site:**

   Open [http://localhost:8000](http://localhost:8000) in your web browser.

---

## Usage

### Customer View

- **Browse Products:** View the latest Afghan clothing collections.
- **Cart Management:** Add or remove items from the cart.
- **Checkout:** Proceed to checkout and make payments securely.
- **Subscribe to Newsletter:** Stay updated with the latest offers and news from Shamla.

### Admin Panel

- **Manage Products:** Add, update, or remove products.
- **Order Management:** View, process, and update customer orders.
- **Content Management:** Publish and manage blog posts.
- **Analytics:** Monitor sales and website performance.

---

## Configuration

### Environment Variables

Set the following environment variables in your `.env` file for better security:

```bash
SECRET_KEY=your_secret_key
DEBUG=False
ALLOWED_HOSTS=your_domain.com
MAILCHIMP_API_KEY=your_mailchimp_api_key
STRIPE_SECRET_KEY=your_stripe_secret_key
```

### Payment Gateways

- Configure Stripe with your API keys in the `settings.py`.

---

## Admin Panel

The admin panel is the heart of Shamla, where you can manage every aspect of the website:

- **Dashboard:** Overview of orders, sales, and customer data.
- **Product Management:** Create, update, or delete product listings.
- **Order Management:** Track and process customer orders.
- **Blog Management:** Publish new blog posts and manage existing content.
- **User Roles:** Assign different access levels to staff members.

---

## Contributing

We welcome contributions to enhance Shamla. Please follow these steps:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature/your-feature-name`
3. Make your changes.
4. Commit your changes: `git commit -m 'Add new feature'`
5. Push to the branch: `git push origin feature/your-feature-name`
6. Submit a pull request.

---

## License

**Copyright © 2022 Arif Haidari and Shamla Atelier.**

This project was originally a private project and has been made public for educational and portfolio purposes only. **No part of this project, including the code, design, or any other materials, may be used, copied, modified, merged, published, distributed, sublicensed, or sold for production or commercial purposes without explicit permission from the copyright holder.**

Please respect the intellectual property rights and do not use this project for any production or commercial use.

---

## Contact

For inquiries, please contact:

- **Email:** arifhaidari336@gmail.com

---
