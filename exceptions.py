from rest_framework.exceptions import APIException


class ProductOutOfStockException(APIException):
    status_code = 400
    default_detail = 'Sorry the product you have requested is out of stock.'
    default_code = 'product_out_of_stock'
