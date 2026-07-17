"""
Document classification + information extraction, powered entirely by the
local Ollama model (see llm_service.py). No cloud LLM calls.
"""
from app.services.llm_service import generate_json, generate

DOC_CLASSES = [
    "invoice", "contract", "resume", "receipt", "id_document",
    "medical_record", "legal_notice", "purchase_order", "report", "other",
]


def classify_document(text: str) -> dict:
    prompt = f"""
Classify the following document into exactly one of these categories:
{', '.join(DOC_CLASSES)}

Document text (truncated):
\"\"\"{text[:3000]}\"\"\"

Return JSON: {{"category": "<one of the categories>", "confidence": <0-1 float>, "reasoning": "<short reason>"}}
"""
    result = generate_json(prompt, system="You are a precise document classification engine.")
    if "category" not in result:
        result["category"] = "other"
    return result


def extract_fields(text: str, doc_class: str) -> dict:
    """Pull structured key-value fields depending on the detected document type."""
    field_hints = {
        "invoice": "invoice_number, invoice_date, due_date, vendor_name, total_amount, line_items",
        "contract": "parties_involved, effective_date, expiration_date, key_obligations, governing_law",
        "resume": "candidate_name, email, phone, skills, years_experience, education",
        "receipt": "merchant_name, date, total_amount, payment_method, items",
        "purchase_order": "po_number, order_date, supplier, total_amount, items",
        "id_document": "full_name, id_number, date_of_birth, issue_date, expiry_date",
    }.get(doc_class, "key_dates, key_amounts, key_entities, summary")

    prompt = f"""
Extract these fields from the document if present: {field_hints}

Document text (truncated):
\"\"\"{text[:4000]}\"\"\"

Return a flat JSON object with the field names above as keys.
Use null for any field you cannot find. Do not invent values.
"""
    return generate_json(prompt, system="You are a precise information-extraction engine.")


def answer_question(question: str, context_chunks: list[str]) -> str:
    context = "\n---\n".join(context_chunks)
    prompt = f"""
Answer the question using ONLY the context below. If the answer isn't in the
context, say you don't have enough information.

Context:
\"\"\"{context}\"\"\"

Question: {question}
Answer:
"""
    return generate(prompt, system="You are a helpful, precise document Q&A assistant.")
