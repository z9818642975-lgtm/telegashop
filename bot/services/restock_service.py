# bot/services/restock_service.py
class RestockService:
    @staticmethod
    def decrease_stock(product, qty: int):
        if product.stock < qty:
            raise ValueError("Недостаточно остатков")
        product.stock -= qty


