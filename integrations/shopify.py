from .integration import Integration


class Shopify(Integration):
    def get_new_orders(self):
        return "Shopify: fetched new orders"

    def update_inventory(self, product_id, quantity):
        return f"Shopify: updated inventory for product {product_id} to {quantity} units"
