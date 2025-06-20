from .integration import Integration


class Salesforce(Integration):
    def create_lead(self, name, company, email):
        return f"Salesforce: created lead {name} at {company} ({email})"

    def update_opportunity(self, opportunity_id, stage):
        return f"Salesforce: updated opportunity {opportunity_id} to stage '{stage}'"
