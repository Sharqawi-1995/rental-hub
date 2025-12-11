Rental-hub
- A Django platform connecting landlords and tenants with trust and simplicity.

Tech Stack:-
- Backend: Django, Django ORM
- Frontend: Bootstrap utilities (custom CSS)
- Database: SQL
- Deployment: AWS

🔑 Key Features:-
- Property Listings: Landlords can add detailed property information with images, pricing, and availability.
- Search & Filters: Tenants can easily find properties using location, price range, and amenities filters.
- Role-Based Access: Separate dashboards for landlords and tenants, ensuring tailored functionality.
- Wishlist & Favorites: Tenants can save properties they’re interested in for quick access later.
- Booking & Lease Management: Streamlined workflows for rental applications, approvals, and lease tracking.
- Reviews & Ratings: Tenants can leave feedback on properties, while landlords can view but not submit reviews.
- Responsive UI: Built with Bootstrap utilities for a clean, mobile-friendly interface without custom CSS.
- Secure Authentication: Robust registration, login, and role management with Django’s built-in auth system.

Usage:-

. Landlord Workflow:
  - Register/Login as landlord
  - Navigate to dashboard → "Add Property"
  - Fill in details (title, price, images, availability)
  - Submit → Property appears in listings

.Tenant Workflow:
  - Register/Login as tenant
  - Browse listings with filters
  - Add properties to Wishlist
  - Apply for booking → landlord receives request

Future Improvements
- Payment integration
- Map-based property search
- Notifications system

🎯 Purpose

The goal of this project is to create a professional-grade rental marketplace that balances usability, scalability, and trust. It empowers landlords to showcase their properties while giving tenants a smooth, transparent renting experience.

# Clone the repo
git remote add origin https://github.com/Sharqawi-1995/rental-hub.git

cd rental-hub

# Create virtual environment
py -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
py manage.py migrate

# Start server
py manage.py runserver

## 🤝 Contributing
Contributions are welcome! Please fork the repo and submit a pull request.

## 📜 License
This project is licensed under the MIT License.

Prental-hub: Simplifying rentals with trust, transparency, and technology.
