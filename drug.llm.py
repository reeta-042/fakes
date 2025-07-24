from openai import OpenAI
import os

# 🔌 Connect to OpenRouter
client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)
# drug_explainer.py
def generate_drug_llm(user_input: dict, verification_result: dict, product_url: str = None):
    verdict = verification_result.get("verdict", "unfamiliar")
    label = verification_result.get("label", "unknown")
    reason = verification_result.get("reason", "Reason not specified.")

    prompt = ""

    if verdict == "fake":
        prompt += (
            f"A drug was submitted and is suspected to be fake.\n"
            f"Explain the issue in clear, simple terms — avoid medical jargon.\n"
            f"Use a calm but serious tone to warn the user.\n"
            f"Keep the entire explanation within 300 characters.\n\n"
            f"1. Fake vs Real Explanation:\n"
            f"- Briefly state what's wrong and how it differs from a real version,make sure to pinpoint the key differnces.\n"
        
        )

        prompt += (
            f"\n2. Health Risk Warnings:\n"
            f"- Describe briefly in plain language what can happen if someone uses a fake version.\n"
        )

        prompt += (
            f"\n3. Safer Alternatives:\n"
            f"- Recommend one verified, safer drug that treat the same condition.\n"
            f"- Keep suggestions short and practical.\n"
        )

    elif verdict == "real":
        prompt += (
            f"This drug has been checked and confirmed to be genuine.\n"
            f"Use a calm and reassuring tone to talk to the user, avoid medical jargon,speak like a layman.\n"
            f"Explain this clearly in simple terms, and stay under 300 characters total.\n\n"
            f"Include:\n"
            f"- A short product summary\n"
            f"- One clear benefit (e.g., relieves pain, lowers fever)\n"
            f"- Two safety tips (e.g., when to take it, what to avoid)\n"
            f"- Packaging highlights (e.g., sealed cap, printed expiry)\n"
            f"- Two common FAQs with answers the average person might ask\n"
        )

    else:
        prompt += (
            f"We couldn’t confirm if this drug is real or fake.\n"
            f"Reason: {reason}\n"
            f"Tell the user to check the seal, expiry date, and NAFDAC registration.\n"
        )

    
    response = client.chat.completions.create(
        model="meta-llama/llama-3.3-70b-instruct:free",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=500
    )

    if response and response.choices and response.choices[0].message:
        return response.choices[0].message.content
    else:
        return "Sorry, we couldn’t generate an explanation at the moment."
