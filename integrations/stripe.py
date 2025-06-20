from .integration import Integration


class Stripe(Integration):
    def create_charge(self, amount, customer):
        return f"Stripe: charged {customer} ${amount}"

    def refund_payment(self, transaction_id):
        return f"Stripe: refunded payment {transaction_id}"
