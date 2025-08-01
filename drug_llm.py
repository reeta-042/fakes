import os
from google import genai
from google.genai import types
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# 💊 Drug Explainer Module
def generate_drug_llm(user_input: dict, verification_result: dict, product_url: str = None,language: str = "English"):
    verdict = verification_result.get("verdict", "unfamiliar")
    reason = verification_result.get("reason", "Reason not specified.")

    prompt = ""

    if verdict == "fake":
        prompt += (
            f"- Respond using the selected  Language:{user_input['language']}\n"
            f"- Let your reponse be in html format \n"
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
            f"Explain clearly and stay on exactly 300 characters,Let your responses also be informative.\n\n"
            f"Explain:\n"
            f"1. Why this product may be counterfeit\n"
            f"2. What health risks could arise from using it\n"
            f"3. Suggest a verified alternative that treats the same condition\n"
            
        )

    elif verdict == "real":
        prompt += (

            f"- Respond using the selected Language:{user_input['language']}\n"
            f"- Let your response be in html format \n"
            f"A drug product submitted by the user has been verified as authentic.\n"
            f"Use the following fields to guide your explanation:\n"
            f"- Drug Name: {user_input['drug_name']}\n"
            f"- Dosage: {user_input['dosage']}\n"
            f"- Form: {user_input['form']}\n"
            f"- Medicine Type: {user_input['medicine_type']}\n"
            f"- Indications: {user_input['indications']}\n"
            f"- Packaging Description: {user_input['package_description']}\n"
            f"- NAFDAC Number Present: {user_input['nafdac_number_present']}\n"
            f"Speak in simple, reassuring language — like explaining to a friend,let your responss be informative.\n"
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
            f"- Respond using the selected  Language:{user_input['language']}\n"
            f"- Let your response be in html format \n"
            f"We couldn’t confirm if this drug is real or fake.\n"
            f"Reason: {reason}\n"
            f"Advise the user to inspect the packaging, NAFDAC number, and expiry date.\n"
            f"Stay under 100 characters. Keep it cautious, calm, and helpful.\n"
            
        )

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(thinking_budget=0) # Disables thinking
        ),
    )

    # It's good practice to return the response from the function
    if response and hasattr(response, 'text'):
        return response.text
    else:
        return "⚠️ No valid response received from AI ASSISTANT "


