import requests

OLLAMA_URL = "http://localhost:11434/api/generate"

SYSTEM_PROMPT = """
You are a workflow generation assistant. Given a user prompt and a list of available integrations (e.g., Stripe, Shopify, Zendesk), generate a JSON workflow plan using those services.

Respond only with a JSON object like this:
{
  "workflow": [
    {"action": "shopify.get_new_orders", "params": {}},
    {"action": "stripe.create_charge", "params": {"amount": "order.total", "customer": "order.customer"}},
    {"action": "zendesk.create_ticket", "params": {"subject": "New order", "description": "Order ID: order.id"}}
  ]
}
Do not explain anything. Output JSON only.
"""


def generate_workflow(prompt: str, connections: list[str]) -> dict:
    connection_str = ", ".join(connections) if connections else "none"
    user_prompt = (
        f"User said: {prompt}. Available integrations: {connection_str}."
    )

    payload = {
        "model": "llama3.2",
        "prompt": f"{SYSTEM_PROMPT}\n{user_prompt}",
        "stream": False,
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=15)
        response.raise_for_status()
        output = response.json().get("response", "")

        # Try to extract JSON block safely
        start = output.find("{")
        end = output.rfind("}") + 1
        json_str = output[start:end]

        return (
            eval(json_str)
            if json_str
            else {"error": "No JSON found in model response"}
        )
    except Exception as e:
        return {"error": str(e)}
