from .integration import Integration


class Zendesk(Integration):
    def create_ticket(self, subject, description):
        return f"Zendesk: created ticket '{subject}' with description '{description}'"

    def update_ticket(self, ticket_id, message):
        return f"Updated ticket {ticket_id} with message '{message}'"

    def close_ticket(self, ticket_id: str):
        return f"Zendesk: closed ticket with ID {ticket_id}"
