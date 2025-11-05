# VeriTrue — AI-Powered Fake Product Detection System

VeriTrue is an AI-driven verification platform that helps users detect fake baby products instantly. It combines AI similarity search, barcode scanning, and multilingual explanations to make product verification fast, simple, and accessible for everyone.

---

## Key Features

-   **🔍 AI Similarity Detection:** Uses Pinecone’s `llama-text-embed-v2` embeddings to compare product details with verified authentic and counterfeit data.
-   **🧩 Threshold-Based Classification:** Determines whether a product is authentic or fake based on similarity scores.
-   **🌍 Vero (Local Language Feedback):** A smart assistant within VeriTrue that explains why a product is real or fake — in the user’s preferred local language for better understanding.
-   **📱 Barcode Scanning:** Users can scan product barcodes directly for instant verification.
-   **⚡ FastAPI Backend + Custom Frontend:** Lightweight and efficient API built with FastAPI, connected to a responsive frontend designed for both mobile and desktop users.
-   **🚀 Deployed on Render:** Fully cloud-hosted for smooth performance and public access.

---

## Tech Stack

| Component             | Technology                                |
| --------------------- | ----------------------------------------- |
| **Backend**           | FastAPI                                   |
| **Frontend**          | HTML, CSS, JavaScript                     |
| **Database**          | Pinecone Vector DB                        |
| **Embeddings**        | `llama-text-embed-v2`                     |
| **Language Support**  | Vero (Custom Multilingual Feature)        |
| **Deployment**        | Render + Vercel                           |

---

## How It Works

1.  **Input:** The user enters a product name, description, or scans its barcode.
2.  **Search:** VeriTrue embeds the input using `llama-text-embed-v2` and searches in Pinecone for similar items.
3.  **Classification:** The system calculates a similarity score and applies a threshold to classify the product.
4.  **Explanation:** Vero provides an explanation in the user’s chosen language, stating why the product is real or fake.
5.  **Result:** The frontend displays both the classification and the reasoning clearly.

---

## Motivation

Counterfeit baby products are a serious threat — they can cause health risks for infants and financial loss for families. VeriTrue was created to empower consumers, protect infants, and build trust in product markets across Africa and beyond.

---

## Live Demo

🔗 **Try it live:** [https://veritrue.vercel.app/](https://veritrue.vercel.app/)

---

## Future Enhancements

-   [ ] **Image Verification:** Add image-based verification using visual embeddings.
-   [ ] **API Integration:** Integrate with manufacturer/product registry APIs.
-   [ ] **Authenticity Certificates:** Generate verifiable product authenticity certificates.
-   [ ] **Expand Dataset:** Grow the dataset to cover other high-risk product categories.

