# Smart Blender NPK - Django E-commerce

A production-ready Django web application for selling agricultural fertilizers and NPK blends.

## Features

- Product catalog with categories and NPK ratios
- Session-based shopping cart
- User authentication and order history
- Checkout system with order processing
- Django Admin dashboard for managing products, orders, and users
- Responsive design with Tailwind CSS
- Green eco-agriculture theme

## Tech Stack

- Django 5+
- Python 3.10+
- SQLite (default) / PostgreSQL (configurable)
- Tailwind CSS (via CDN)
- Django Templates

## Installation

### 1. Create a virtual environment

\`\`\`bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
\`\`\`

### 2. Install dependencies

\`\`\`bash
pip install -r requirements.txt
\`\`\`

### 3. Run migrations

\`\`\`bash
python manage.py makemigrations
python manage.py migrate
\`\`\`

### 4. Create a superuser

\`\`\`bash
python manage.py createsuperuser
\`\`\`

Follow the prompts to create an admin account.

### 5. Load sample data (optional)

\`\`\`bash
python manage.py loaddata fixtures/sample_data.json
\`\`\`

This will create sample categories and products to get you started.

### 6. Run the development server

\`\`\`bash
python manage.py runserver
\`\`\`

### 7. Access the application

- **Website**: http://localhost:8000
- **Admin Dashboard**: http://localhost:8000/admin

## Configuration

### Database

By default, the project uses SQLite. To use PostgreSQL:

1. Uncomment the PostgreSQL configuration in `config/settings.py`
2. Set environment variables:

\`\`\`bash
export DB_NAME=smart_blender_npk
export DB_USER=postgres
export DB_PASSWORD=your_password
export DB_HOST=localhost
export DB_PORT=5432
\`\`\`

### Environment Variables

Create a `.env` file in the project root (optional):

\`\`\`
DJANGO_SECRET_KEY=your-secret-key-here
DEBUG=True
DB_NAME=smart_blender_npk
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
\`\`\`

**Important**: Never commit your `.env` file or expose your secret key in production!

## Project Structure

\`\`\`
smart-blender-npk/
├── config/              # Project configuration
│   ├── settings.py      # Django settings
│   ├── urls.py          # Root URL configuration
│   └── wsgi.py          # WSGI configuration
├── shop/                # Main e-commerce app
│   ├── models.py        # Database models (Category, Product, Order, OrderItem)
│   ├── views.py         # View functions for pages
│   ├── cart_views.py    # Shopping cart views
│   ├── checkout_views.py # Checkout and registration views
│   ├── urls.py          # App URL patterns
│   ├── admin.py         # Admin configuration
│   ├── cart.py          # Shopping cart logic
│   ├── forms.py         # Forms (checkout, registration)
│   └── context_processors.py # Template context processors
├── templates/           # HTML templates
│   ├── base.html        # Base template with navigation
│   └── shop/            # Shop-specific templates
├── static/              # Static files (CSS, JS, images)
├── media/               # User-uploaded files (product images)
├── fixtures/            # Sample data
│   └── sample_data.json # Sample categories and products
├── requirements.txt     # Python dependencies
└── manage.py            # Django management script
\`\`\`

## Database Models

### Category
- Product categories for organizing fertilizers
- Fields: name, slug, description, created_at

### Product
- Fertilizer products with NPK information
- Fields: name, slug, category, description, npk_ratio, dosage_info, price, stock, image, available, created_at, updated_at

### Order
- Customer orders with status tracking
- Fields: user, first_name, last_name, email, phone, address, city, postal_code, total_price, status, created_at, updated_at
- Status options: Pending, Processing, Shipped, Delivered, Cancelled

### OrderItem
- Individual items in orders
- Fields: order, product, quantity, price

## Admin Dashboard

Access the Django Admin at `/admin` to:

- **Manage Products**: Add, edit, delete products with CRUD operations
- **Manage Categories**: Organize products into categories
- **Update Order Status**: Track orders from Pending → Processing → Shipped → Delivered
- **Manage Users**: View and manage customer accounts
- **View Analytics**: See product counts, stock levels, and order summaries

The admin interface includes:
- Color-coded stock status indicators
- Order status badges
- Inline order item editing
- Search and filter capabilities
- Detailed order summaries

## Usage

### For Customers

1. **Browse Products**: View all products or filter by category
2. **View Product Details**: See NPK ratios, dosage information, and pricing
3. **Add to Cart**: Select quantity and add products to cart
4. **Checkout**: Fill in shipping information and place order
5. **Track Orders**: View order history and status updates

### For Administrators

1. **Login to Admin**: Go to `/admin` and login with superuser credentials
2. **Add Products**: Create new fertilizer products with NPK information
3. **Manage Inventory**: Update stock levels and pricing
4. **Process Orders**: Update order status as they progress
5. **View Reports**: Monitor sales and inventory through the admin dashboard

## Production Deployment

Before deploying to production:

1. **Set DEBUG to False** in `config/settings.py`
2. **Generate a new SECRET_KEY** and store it securely
3. **Configure ALLOWED_HOSTS** with your domain
4. **Use PostgreSQL** instead of SQLite
5. **Set up static file serving** with WhiteNoise or a CDN
6. **Configure email backend** for order confirmations
7. **Enable HTTPS** and security middleware
8. **Set up backup strategy** for database

## License

MIT License

## Support

For issues or questions, please open an issue on the project repository.
