from openai import OpenAI
import os

# 🔌 Connect to OpenRouter
client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

# 🍼 Baby Explainer Module
def generate_baby_llm(user_input: dict, verification_result: dict, product_url: str = None):
    verdict = verification_result.get("verdict", "unfamiliar")
    label = verification_result.get("label", "unknown")
    reason = verification_result.get("reason", "Reason not specified.")

    prompt = ""

    if verdict == "fake":
        prompt += (
            f"A baby product submitted by the user is suspected to be fake.\n"
            f"Use the following fields to guide your response:\n"
            f"- Name: {user_input['name']}\n"
            f"- Product Type: {user_input['product_type']}\n"
            f"- Age Group: {user_input['age_group']}\n"
            f"- Platform: {user_input['platform']}\n"
            f"- Package Description: {user_input['package_description']}\n"
            f"Use a calm, reassuring tone — but also issue a clear warning if the product is potentially unsafe.\n"
            f"Explain the suspected issue clearly and gently.\n"
            f"Please keep the total explanation within 300 characters.\n\n"
            f"Explain:\n"
            f"- Why this product may be counterfeit (compare with how a real version looks or behaves)\n"
            f"- Health risks based on baby age group and packaging type\n"
            f"- Suggest one or two safe, verified products suitable for similar use\n"
        )

    elif verdict == "real":
        prompt += (
            f"A baby product submitted by the user is verified as authentic.\n"
            f"Use the following fields to guide your response:\n"
            f"- Name: {user_input['name']}\n"
            f"- Product Type: {user_input['product_type']}\n"
            f"- Age Group: {user_input['age_group']}\n"
            f"- Platform: {user_input['platform']}\n"
            f"- Package Description: {user_input['package_description']}\n"
            f"Please keep the total explanation within 300 characters.\n"
            f"Please share a calm and reassuring response to the user like you are a caregiver.\n\n"
            f"Include:\n"
            f"- A very brief product summary\n"
            f"- One gentle key benefit of the product\n"
            f"- Two bullet-point safety precautions\n"
            f"- Two short frequently asked questions with helpful answers\n"
        )

    else:
        prompt += (
            f"This product’s authenticity could not be confidently verified.\n"
            f"Keep the total explanation within 100 characters.\n"
            f"Reason: {reason}\n"
            f"Advise the user to double-check the packaging, NAFDAC number and expiry date. Consult support if unsure.\n"
        )

    response = client.chat.completions.create(
        model="qwen/qwen3-coder:free",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=500
    )

    if response and response.choices and response.choices[0].message:
        return response.choices[0].message.content
    else:
        return "Sorry, we couldn’t generate an explanation at the moment."
