from .integration import Integration


class Netsuite(Integration):
    def create_invoice(self, customer, amount, due_date):
        return (
            f"Invoice created for {customer}: ${amount}, " f"due by {due_date}"
        )

    def update_inventory(self, product_id, quantity):
        return (
            f"Inventory for product {product_id} updated "
            f"to quantity {quantity}"
        )
