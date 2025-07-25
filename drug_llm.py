from openai import OpenAI
import os

# 🔌 Connect to OpenRouter
client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

# 💊 Drug Explainer Module
def generate_drug_llm(user_input: dict, verification_result: dict, product_url: str = None):
    verdict = verification_result.get("verdict", "unfamiliar")
    reason = verification_result.get("reason", "Reason not specified.")

    prompt = ""

    if verdict == "fake":
        prompt += (
            f"A drug product submitted by the user is suspected to be fake.\n"
            f"Use the following fields to guide your explanation:\n"
            f"- Drug Name: {user_input['drug_name']}\n"
            f"- Dosage: {user_input['dosage']}\n"
            f"- Form: {user_input['form']}\n"
            f"- Medicine Type: {user_input['medicine_type']}\n"
            f"- Pack Size: {user_input['pack_size']}\n"
            f"- Brand Name: {user_input['brand_name']}\n"
            f"- Indications: {user_input['indications']}\n"
            f"- Packaging Description: {user_input['package_description']}\n"
            f"- Expiry Date Visible: {user_input['expiry_date_available']}\n"
            f"- NAFDAC Number Present: {user_input['nafdac_number_present']}\n"
            f"Use a calm but serious tone to warn the user.\n"
            f"Explain clearly and stay under 300 characters.\n\n"
            f"Explain:\n"
            f"1. Why this product may be counterfeit\n"
            f"2. What health risks could arise from using it\n"
            f"3. Suggest a verified alternative that treats the same condition\n"
        )

    elif verdict == "real":
        prompt += (
            f"A drug product submitted by the user has been verified as authentic.\n"
            f"Use the following fields to guide your explanation:\n"
            f"- Drug Name: {user_input['drug_name']}\n"
            f"- Dosage: {user_input['dosage']}\n"
            f"- Form: {user_input['form']}\n"
            f"- Medicine Type: {user_input['medicine_type']}\n"
            f"- Indications: {user_input['indications']}\n"
            f"- Packaging Description: {user_input['package_description']}\n"
            f"- NAFDAC Number Present: {user_input['nafdac_number_present']}\n"
            f"Speak in simple, reassuring language — like explaining to a friend.\n"
            f"Keep the explanation under 300 characters.\n\n"
            f"Include:\n"
            f"- Short product summary\n"
            f"- One key benefit\n"
            f"- Two basic safety tips\n"
            f"- One packaging clue\n"
            f"- Two FAQs and answers (keep general)\n"
        )

    else:
        prompt += (
            f"We couldn’t confirm if this drug is real or fake.\n"
            f"Reason: {reason}\n"
            f"Advise the user to inspect the packaging, NAFDAC number, and expiry date.\n"
            f"Stay under 100 characters. Keep it cautious, calm, and helpful.\n"
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
