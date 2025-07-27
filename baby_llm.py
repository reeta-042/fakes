import os
from google import genai
from google.genai import types
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


# 🍼 Baby Explainer Module
def generate_baby_llm(user_input: dict, verification_result: dict, product_url: str = None,language: str = "English"):
    verdict = verification_result.get("verdict", "unfamiliar")
    label = verification_result.get("label", "unknown")
    reason = verification_result.get("reason", "Reason not specified.")

    prompt = ""

    if verdict == "fake":
        prompt += (
            f"- Respond using the selected Language:{user_input['language']}\n"
            f"- Let your response also be in an html format \n"
            f"A baby product submitted by the user is suspected to be fake.\n"
            f"Use the following fields to guide your response:\n"
            f"- Name: {user_input['name']}\n"
            f"- Product Type: {user_input['product_type']}\n"
            f"- Age Group: {user_input['age_group']}\n"
            f"- Platform: {user_input['platform']}\n"
            f"- Package Description: {user_input['package_description']}\n"
            f"Use a calm, reassuring tone — but also issue a clear warning if the product is potentially unsafe.\n"
            f"Explain the suspected issue clearly and gently, your responses should also be informative.\n"
            f"Please keep the total explanation exactly on  300 characters.\n\n"
            f"Explain:\n"
            f"- Why this product may be counterfeit (compare with how a real version looks or behaves)\n"
            f"- Health risks based on baby age group and packaging type\n"
            f"- Suggest one or two safe, verified products suitable for similar use\n"
            
        
            
        )

    elif verdict == "real":
        prompt += (
            f"- Respond using the selected  Language:{user_input['language']}\n"
            f" - Let your response be in an html format\n"
            f"A baby product submitted by the user is verified as authentic.\n"
            f"Use the following fields to guide your response:\n"
            f"- Name: {user_input['name']}\n"
            f"- Product Type: {user_input['product_type']}\n"
            f"- Age Group: {user_input['age_group']}\n"
            f"- Platform: {user_input['platform']}\n"
            f"- Package Description: {user_input['package_description']}\n"
            f"Please keep the total explanation within 300 characters.\n"
            f"Please share a calm and reassuring response to the user like you are a caregiver,let your responses be informative\n\n"
            f"Include:\n"
            f"- A very brief product summary\n"
            f"- One gentle key benefit of the product\n"
            f"- Two bullet-point safety precautions\n"
            f"- Two short frequently asked questions with helpful answers\n"
            
        
        )

    else:
        prompt += (
            f"- Respond using the selected Nigerian Language:{user_input['language']}\n"
            f"This product’s authenticity could not be confidently verified.\n"
            f"Keep the total explanation within 100 characters.\n"
            f"Reason: {reason}\n"
            f"Advise the user to double-check the packaging, NAFDAC number and expiry date. Consult support if unsure.\n"
            
        
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
        return "⚠️ No valid response received from AI ASSISTANT."



