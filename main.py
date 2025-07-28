from fastapi import FastAPI
from pydantic import BaseModel
from pinecone import Pinecone
from pymongo import MongoClient
import os
import uvicorn
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware
from baby_llm import generate_baby_llm
from drug_llm import generate_drug_llm
import re  # ✅ added for regex

# ✅ Load environment variables
pinecone_api_key = os.getenv("PINECONE_API_KEY")
pinecone_env = os.getenv("PINECONE_ENVIRONMENT")
mongo_uri = os.getenv("MONGODB_URI")

if not pinecone_api_key:
    raise ValueError("⚠️ PINECONE_API_KEY is not set!")
if not pinecone_env:
    raise ValueError("⚠️ PINECONE_ENVIRONMENT is not set!")
if not mongo_uri:
    raise ValueError("⚠️ MONGODB_URI is not set!")

# ✅ Initialize Pinecone client
pc = Pinecone(api_key=pinecone_api_key, environment=pinecone_env)
drug_index = pc.Index("fake-drugs")
baby_index = pc.Index("fake-baby")

# ✅ MongoDB client setup
client = MongoClient(mongo_uri)
db = client.VeriTrue
drug_collection = db.drug_verifications
baby_collection = db.baby_verifications

# ✅ FastAPI app
app = FastAPI(
    title="Fake Product Checker API",
    description="Verify if a drug or baby product is real or fake using Pinecone semantic search.",
    version="2.0.0"
)

origins = [
    "http://localhost:3000",
    "https://veritrue.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Schemas
class BabyProductInput(BaseModel):
    name: str
    brand_name: str
    price_in_naira: int
    platform: str
    product_type: str
    age_group: str
    package_description: str
    visible_expiriry_date: str
    language: str

class DrugProductInput(BaseModel):
    drug_name: str
    price: int
    dosage: str
    form: str
    brand_name: str
    medicine_type: str
    pack_size: str
    indications: str
    side_effects: str
    expiry_date_available: str
    platform: str
    nafdac_number_present: str
    package_description: str
    language: str

# ✅ Utility: Extract product_url from text
def extract_product_url(text):
    match = re.search(r'Product_url\s*:\s*(https?://[^\s]+)', text)
    return match.group(1).strip() if match else ""

# ✅ Classify function
def classify_product(user_text, index, threshold=0.8):
    try:
        response = pc.inference.embed(
            model="llama-text-embed-v2",
            inputs=[{"text": user_text}],
            parameters={"input_type": "passage"}
        )
        vector = response[0]["values"]
        result = index.query(vector=vector, top_k=3, include_metadata=True)
    except Exception as e:
        return {
            "verdict": "error",
            "score": None,
            "reason": f"❌ Error during embedding/query: {str(e)}",
            "Product_url": ""
        }

    if not result["matches"]:
        return {
            "verdict": "no_match",
            "score": None,
            "reason": "⚠️ No similar product found in the database.",
            "Product_url": ""
        }

    for match in result["matches"]:
        score = match["score"]
        metadata = match["metadata"]
        text = metadata.get("text", "")
        product_url = metadata.get("Product_url", "") or extract_product_url(text)

        if score >= threshold:
            reason = text.split("Reason:")[-1].strip() if "Reason:" in text else "Reason not specified."
            verdict = "fake" if "fake" in text.lower() else "real" if "real" in text.lower() else "unfamiliar"
            return {
                "verdict": verdict,
                "score": round(score, 2),
                "reason": reason,
                "Product_url": product_url
            }

    fallback = result["matches"][0]["metadata"]
    fallback_text = fallback.get("text", "")
    reason = fallback_text.split("Reason:")[-1].strip() if "Reason:" in fallback_text else "Reason not specified."
    product_url = fallback.get("Product_url", "") or extract_product_url(fallback_text)
    return {
        "verdict": "unfamiliar",
        "score": round(result["matches"][0]["score"], 2),
        "reason": reason,
        "Product_url": product_url
    }

# ✅ Endpoint: Baby Product
@app.post("/verify-baby-product")
def verify_baby_product(data: BabyProductInput):
    description_only_text = f"""
    Product: {data.name}
    Brand: {data.brand_name}
    Price: {data.price_in_naira} NGN
    Platform: {data.platform}
    Type: {data.product_type}
    Age Group: {data.age_group}
    Package: {data.package_description}
    Expiry Visible: {data.visible_expiriry_date}
    """

    result = classify_product(description_only_text, baby_index)
    product_url = result.get("Product_url", "")
    reason = result.get("reason", "")

    explanation = generate_baby_llm(user_input=data.dict(), verification_result=result, product_url=product_url)

    baby_collection.insert_one({
        "description_only_text": data.dict(),
        "verification_result": {
            "verdict": result["verdict"],
            "score": result["score"],
            "reason": reason,
            "Product_url": product_url
        },
        "timestamp": datetime.utcnow(),
        "verified": {"status": "pending"}
    })

    return {
        "verdict": result["verdict"],
        "score": result["score"],
        "What_vero_has_to_say": explanation if explanation else "Vero has nothing to say",
        "product_url": product_url
    }

# ✅ Endpoint: Drug Product
@app.post("/verify-drug-product")
def verify_drug_product(data: DrugProductInput):
    description_only_text = f"""
    Drug Name: {data.drug_name}
    Price: {data.price} NGN
    Dosage: {data.dosage}
    Form: {data.form}
    Brand: {data.brand_name}
    Medicine Type: {data.medicine_type}
    Pack Size: {data.pack_size}
    Indications: {data.indications}
    Side Effects: {data.side_effects}
    Expiry Date Visible: {data.expiry_date_available}
    Platform: {data.platform}
    NAFDAC Number Present: {data.nafdac_number_present}
    Package Description: {data.package_description}
    """

    result = classify_product(description_only_text, drug_index)
    product_url = result.get("Product_url", "")
    reason = result.get("reason", "")

    explanation = generate_drug_llm(user_input=data.dict(), verification_result=result, product_url=product_url)

    drug_collection.insert_one({
        "description_only_text": data.dict(),
        "verification_result": {
            "verdict": result["verdict"],
            "score": result["score"],
            "reason": reason,
            "Product_url": product_url
        },
        "timestamp": datetime.utcnow(),
        "verified": {"status": "pending"}
    })

    return {
        "verdict": result["verdict"],
        "score": result["score"],
        "What_vero_has_to_say": explanation if explanation else "Vero has nothing to say",
        "product_url": product_url
    }

# ✅ Run on Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
