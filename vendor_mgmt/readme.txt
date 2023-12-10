Vendor Management System
1. Installation:

   - Clone the repository:
     git clone https://github.com/yourusername/vendor_mgmt.git
     cd vendor_mgmt

   - Install dependencies:
     pip install -r requirements.txt

   - Apply migrations:
     python manage.py migrate

   - Run the development server:
     python manage.py runserver

2. Endpoints:

   - Retrieve all vendors:
     curl http://localhost:8000/api/vendors/

   - Create a new vendor:
     curl -X POST -H "Content-Type: application/json" -d '{"name": "Vendor ABC", "location": "City XYZ"}' http://localhost:8000/api/vendors/

   - Retrieve performance metrics for a vendor:
     curl http://localhost:8000/api/vendors/1/performance/

   - Retrieve all purchase orders:
     curl http://localhost:8000/api/purchase-orders/

   - Create a new purchase order:
     curl -X POST -H "Content-Type: application/json" -d '{"vendor": 1, "amount": 100.00, "status": "pending"}' http://localhost:8000/api/purchase-orders/

   - Retrieve details of a purchase order:
     curl http://localhost:8000/api/purchase-orders/1/details/

   - Retrieve purchase orders for a vendor:
     curl http://localhost:8000/api/vendors/1/purchase-orders/

