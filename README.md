# OneGold

OneGold is a modern e-commerce web application designed specifically for a jewelry store. This project combines the power of Django for backend management and React for a sleek, dynamic frontend interface. It provides a seamless shopping experience for customers while ensuring robust management for store administrators.

---

## Features

### Customer-Facing Features:

- **User Authentication**: Sign up, log in, log out, and password recovery functionalities.
- **Product Browsing**: View products with detailed descriptions, images, and prices.
- **Category Filtering**: Search and filter products based on categories, price range, or offers.
- **Shopping Cart**: Add/remove items, update quantities, and view total costs.
- **Wishlist**: Save favorite items for later.
- **Checkout System**: Secure order placement with payment gateway integration.

### Admin-Facing Features:

- **Product Management**: Add, update, and delete product details.
- **Order Management**: View and update the status of orders.
- **Customer Management**: View registered customers and their purchase history.
- **Analytics Dashboard**: Track sales, popular products, and customer activities.

---

## Tech Stack

### Backend:

- **Django**: Core backend framework for handling business logic and APIs.
- **Django REST Framework (DRF)**: For building RESTful APIs.
- **PostgreSQL**: Database for storing product and user information.

### Frontend:

- **React.js**: For building a responsive and dynamic user interface.
- **Material-UI (MUI)**: For styling and pre-built UI components.
- **Axios**: For making API requests to the backend.

### Additional Tools:

- **Stripe**: For payment processing.
- **Celery**: For handling asynchronous tasks like sending order confirmation emails.
- **Redis**: As a message broker for Celery.
- **Docker**: For containerization of the application.
- **Nginx**: For serving the application in production.

---

## Installation

### Prerequisites

- Python 3.9+
- Node.js 14+
- PostgreSQL
- Docker (optional, for containerized setup)

### Backend Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/onegold.git
   cd onegold/backend
   ```

2. Create a virtual environment and activate it:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Configure the environment variables:

   - Create a `.env` file in the `backend` directory.
   - Add the following variables:
     ```env
     SECRET_KEY=your-django-secret-key
     DEBUG=True
     DATABASE_URL=postgres://username:password@localhost:5432/onegold
     STRIPE_SECRET_KEY=your-stripe-secret-key
     ```

5. Apply database migrations:

   ```bash
   python manage.py migrate
   ```

6. Start the development server:

   ```bash
   python manage.py runserver
   ```

### Frontend Setup

1. Navigate to the frontend directory:

   ```bash
   cd ../frontend
   ```

2. Install dependencies:

   ```bash
   npm install
   ```

3. Start the development server:

   ```bash
   npm start
   ```

---

## Usage

- Visit `http://localhost:8000` to access the backend.
- Visit `http://localhost:3000` to access the React frontend.

---

## Project Structure

### Backend:

```
backend/
|-- onegold/
|   |-- settings.py
|   |-- urls.py
|   |-- wsgi.py
|
|-- products/
|   |-- models.py
|   |-- views.py
|   |-- serializers.py
|
|-- orders/
|   |-- models.py
|   |-- views.py
|   |-- tasks.py
|
|-- users/
|   |-- models.py
|   |-- views.py
```

### Frontend:

```
frontend/
|-- src/
|   |-- components/
|   |-- pages/
|   |-- App.js
|   |-- index.js
```

---

## API Endpoints

### Authentication:

- `POST /api/auth/login/`: User login
- `POST /api/auth/register/`: User registration
- `POST /api/auth/logout/`: User logout

### Products:

- `GET /api/products/`: List all products
- `GET /api/products/:id/`: Get product details

### Cart:

- `POST /api/cart/add/`: Add product to cart
- `DELETE /api/cart/remove/`: Remove product from cart

### Orders:

- `POST /api/orders/`: Place an order
- `GET /api/orders/:id/`: Get order details

---

## Deployment

### Using Docker:

1. Build and run the Docker containers:
   ```bash
   docker-compose up --build
   ```
2. Access the application:
   - Backend: `http://localhost:8000`
   - Frontend: `http://localhost:3000`

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

## Contributors

- [Your Name](https://github.com/your-username)
- Contributions are welcome! Feel free to open issues or submit pull requests.

---

## Acknowledgments

- **Django**: For making backend development seamless.
- **React**: For a dynamic and interactive frontend.
- **Material-UI**: For providing modern UI components.

