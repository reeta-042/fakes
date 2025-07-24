from openai import OpenAI
import os

# 🔌 Connect to OpenRouter
client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

# baby_explainer.py
def generate_baby_llm(user_input: dict, verification_result: dict, product_url: str = None):
    verdict = verification_result.get("verdict", "unfamiliar")
    label = verification_result.get("label", "unknown")
    reason = verification_result.get("reason", "Reason not specified.")

    prompt = ""

    if verdict == "fake":
        prompt += (
            f"A baby product has been submitted and is suspected to be counterfeit.\n"
            f"Use a calm, reassuring tone — but also issue a clear warning if the product is potentially unsafe.\n"
            f"Explain the suspected issue clearly and gently.\n"
            f"Please keep the total explanation within 300 characters.\n" 
            f"Here’s what you should explain to the user:\n\n"
            f"1. Fake vs Real Explanation:\n"
            f"- Clearly and briefly explain why this product is flagged as fake, Compare it with a real version of the product,make sure to pinpoint key differnces.\n"
            
        )

        prompt += (
            f"\n3. Health Risk Warnings:\n"
            f"- Based on the product type, age group, or packaging, briefly explain possible dangers of using a fake version.\n"
        )

        prompt += (
            f"\n4. Safer Alternatives:\n"
            f"- Recommend 1–3 similar, verified baby products from trusted brands.\n"
            f"- Briefly Suggest items suitable for the same age group or use-case.\n"
        )

    elif verdict == "real":
        prompt += (
            f"A baby product has been reviewed and verified as authentic.\n"
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
            f"Advise the user to double-check the packaging, NAFDAC number and expiry date consult support if unsure.\n"
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
