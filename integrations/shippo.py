from .integration import Integration


class Shippo(Integration):
    def create_shipment(self, address_from, address_to, package_weight):
        return f"Shippo: created shipment from {address_from} to {address_to}, weight {package_weight}"

    def track_package(self, tracking_number):
        return f"Shippo: tracking status for {tracking_number} is 'In Transit'"
