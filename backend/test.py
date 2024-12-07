import unittest
from unittest.mock import patch
from your_app import app
from your_app.models import Product

class TestGetAllProducts(unittest.TestCase):

    # Test case 1: Test successful retrieval of all products
    @patch('your_app.Product.query.all', return_value=[Product(productID=1, productName="Product A", brandName="Brand X")])
    def test_get_all_products_success(self, mock_query):
        with app.test_client() as client:
            response = client.get('/your-endpoint')  # เปลี่ยนเป็น URL ของ API ที่เรียกใช้ get_all_products()
            self.assertEqual(response.status_code, 200)
            self.assertIn('Product A', response.get_json())  # ตรวจสอบว่าได้รับข้อมูลผลิตภัณฑ์ที่คาดไว้

    # Test case 2: Test error handling when database is down
    @patch('your_app.Product.query.all', side_effect=Exception("Database error"))
    def test_get_all_products_error(self, mock_query):
        with app.test_client() as client:
            response = client.get('/your-endpoint')  # เปลี่ยนเป็น URL ของ API ที่เรียกใช้ get_all_products()
            self.assertEqual(response.status_code, 500)
            self.assertEqual(response.get_json(), {'error': 'Error to retrieve the data'})

if __name__ == '__main__':
    unittest.main()
