# Agentic

**Agentic** is a prototype of an AI-powered e-commerce workflow designer. It integrates with 3rd-party SaaS platforms such as Stripe, Shopify, Zendesk, Shippo, Salesforce, and more.

---

## 🚀 Prerequisites

- **NVIDIA GPU with CUDA support** is highly recommended for running local LLMs efficiently.
- [Ollama](https://ollama.com/download) must be installed and running.

To download the `llama3.2` model:

```bash
ollama pull llama3.2
```

Set up the Python environment (tested with Python 3.10.16):

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run Agentic:

```bash
python main.py
```

Then open your browser and go to: [http://localhost:7860](http://localhost:7860)

---

## 🧠 Using Agentic

Describe your desired workflow in natural language. For example:

```
Sell John Doe from Microsoft 1000 widgets for 3 dollars each, adjust the inventory and prepare a shipment from Bellevue to Albuquerque.
Create a lead for that user. Fill other details with some realistic data.
```

Click `Generate workflow` to generate a structured workflow. Agentic will use the Ollama-hosted LLM to produce a human-readable JSON like this:

```json
{
  "workflow": [
    {
      "action": "shopify.update_inventory",
      "params": {
        "product_id": 12345,
        "quantity": -1000
      }
    },
    {
      "action": "netsuite.create_invoice",
      "params": {
        "customer": "John Doe",
        "amount": 3000,
        "due_date": "2023-02-20"
      }
    },
    {
      "action": "netsuite.update_inventory",
      "params": {
        "product_id": 12345,
        "quantity": 0
      }
    },
    {
      "action": "shippo.create_shipment",
      "params": {
        "address_from": {
          "name": "John Doe",
          "address_line1": "123 Main St",
          "city": "Bellevue",
          "state": "WA",
          "zip": "98101"
        },
        "address_to": {
          "name": "Albuquerque Inc.",
          "address_line1": "456 Elm St",
          "city": "Albuquerque",
          "state": "NM",
          "zip": "87102"
        },
        "package_weight": 1000
      }
    },
    {
      "action": "salesforce.create_lead",
      "params": {
        "name": "John Doe",
        "company": "Microsoft",
        "email": "johndoe@microsoft.com"
      }
    }
  ]
}
```

You can edit and tweak this workflow manually and supply your own synthetic data.

To simulate the workflow, click `Execute workflow`.  
In production, this would call the actual 3rd-party services. In this prototype, the integrations are mocked and will only log the actions.

---

## 🧩 Extending Agentic

To add support for a new 3rd-party service:

1. Create a new Python class that inherits from the `Integration` base class.
2. Define methods in that class to represent available actions for the service.
3. Add an instance of this class to the `INTEGRATIONS` dictionary in `main.py`.

---

## 📜 License

BSD 3-Clause License