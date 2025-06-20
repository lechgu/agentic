import json

import gradio as gr
import requests

from integrations.salesforce import Salesforce
from integrations.shippo import Shippo
from integrations.shopify import Shopify
from integrations.stripe import Stripe
from integrations.zendesk import Zendesk
from integrations.netsuite import Netsuite

INTEGRATIONS = {
    "Stripe": Stripe(),
    "Zendesk": Zendesk(),
    "Shopify": Shopify(),
    "Shippo": Shippo(),
    "Salesforce": Salesforce(),
    "Netsuite": Netsuite(),
}

OLLAMA_URL = "http://localhost:11434/api/generate"


def format_available_actions(integrations):
    lines = []
    for name, integration in integrations.items():
        lines.append(f"### {name}")
        for full_name, sig in integration.describe_methods().items():
            lines.append(f"- `{full_name}{sig}`")
        lines.append("")
    return "\n".join(lines)


def build_prompt(user_request):
    available = format_available_actions(INTEGRATIONS)
    parts = [
        "You are a workflow generation assistant.",
        "",
        "Here are the available integrations and their methods:",
        "",
        available,
        "",
        "The user will describe a workflow in natural language.",
        "You must return a JSON object like:",
        "",
        "{",
        '  "workflow": [',
        "    {",
        '      "action": "stripe.create_charge",',
        '      "params": {',
        '        "amount": 100,',
        '        "customer": "Jane Doe"',
        "      }",
        "    }",
        "  ]",
        "}",
        "",
        "Only use the available integrations and methods listed above.",
        "Respond with valid JSON only.",
        "Do not include any explanation or comments.",
        "",
        "User request:",
        user_request.strip(),
    ]
    return "\n".join(parts)


def call_llm(prompt):
    payload = {
        "model": "llama3.2",
        "prompt": prompt,
        "stream": False,
    }
    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=30)
        response.raise_for_status()
        raw = response.json()["response"]
        start = raw.find("{")
        end = raw.rfind("}") + 1
        json_block = raw[start:end]
        return json.loads(json_block)
    except Exception as e:
        return {"error": str(e)}


def generate_workflow(description):
    prompt = build_prompt(description)
    result = call_llm(prompt)
    return json.dumps(result, indent=2)


def run_workflow(workflow):
    log = []
    for step in workflow:
        action = step.get("action", "")
        params = step.get("params") or {}
        if "." not in action:
            log.append(f"[error] Invalid action: {action}")
            continue
        service, method = action.split(".", 1)
        integration = INTEGRATIONS.get(service.capitalize())
        if not integration:
            log.append(f"[error] Unknown integration: {service}")
            continue
        try:
            result = integration.call(method, **params)
            log.append(f"[ok] {action} → {result}")
        except Exception as e:
            log.append(f"[error] {action}: {e}")
    return "\n".join(log)


def parse_workflow(raw_json):
    try:
        data = json.loads(raw_json)
        return run_workflow(data.get("workflow", []))
    except Exception as e:
        return f"[error] Workflow parsing failed: {e}"


def main():
    with gr.Blocks(title="Agentic") as app:
        gr.Markdown("# Agentic Workflow Designer")

        with gr.Accordion("Available Integrations and Methods", open=False):
            gr.Markdown(format_available_actions(INTEGRATIONS))

        with gr.Group():
            gr.Markdown("### Describe your workflow")
            placeholder = "eg. charge John Doe $42"
            workflow_prompt = gr.Textbox(lines=3, placeholder=placeholder)

            generate_btn = gr.Button("Generate Workflow")
            workflow_editor = gr.Code(
                label="Workflow",
                language="json",
                value=json.dumps({"workflow": []}, indent=2),
            )

        with gr.Group():
            execute_btn = gr.Button("Execute Workflow")
            execution_log = gr.Textbox(label="Execution Log", lines=10)

        generate_btn.click(
            fn=generate_workflow,
            inputs=[workflow_prompt],
            outputs=[workflow_editor],
        )

        execute_btn.click(
            fn=parse_workflow,
            inputs=[workflow_editor],
            outputs=[execution_log],
        )

    app.launch(share=False)


if __name__ == "__main__":
    main()
