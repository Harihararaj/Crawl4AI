# Enterprise Security:
Enterprise security is about protecting enterprise systems, applications, networks, and data from unauthorized access, misuse, or threats. It focuses on safeguarding the organization against both external and internal risks (hackers, malware, data breaches, insider misuse, etc.).
### Scope:
- Implement identity and access management (IAM)
- Use encryption in transit and at rest
- Deploy firewalls, intrusion detection, and prevention systems
- Conduct regular security audits, monitoring, and incident response

# Enterprise Privacy:
Enterprise privacy concerns how the organization collects, stores, processes, and shares personal or sensitive data, in compliance with laws, regulations, and user expectations. It focuses on protecting the rights of individuals whose data is being handled (employees, customers, partners).
### Scope:
- Ensure compliance with regulations (GDPR, HIPAA, CCPA, etc.)
- Apply data minimization (collect only what is necessary)
- Enforce purpose limitation (use data only for agreed purposes)
- Use anonymization, pseudonymization, and consent management

# Privacy-First AI:
Large Language Models (LLMs) are reshaping how enterprises work, making it possible to automate tasks at a scale never seen before. But with great power comes great responsibility, especially when it comes to protecting data privacy and security.

When leveraging third-party hosted LLM APIs, organizations must proceed with caution. The first step is to carefully review the provider’s privacy notice to understand how submitted data will be stored, processed, and potentially shared. From a development perspective, engineers must integrate privacy safeguards early in the design phase. At the enterprise level, it is essential to avoid transmitting customer or client sensitive information directly to external APIs. Instead, enterprises should implement Personally Identifiable Information (PII) masking before data is sent.
## LLM Masking (Protecting sensitive information in AI Application):
LLM Masking is a privacy-preserving technique that detects and replaces sensitive information with placeholder tokens prior to processing text with Large Language Models. Once processing is complete, the original data can be securely reinserted if required. This approach reduces exposure risks while enabling enterprises to safely benefit from LLM capabilities.

## What we acheive with LLM Masking:
- **🔒 Stronger Data Privacy** – Prevents personally identifiable information (PII) from ever reaching third-party LLM services.
- **📜 Regulatory Compliance** – Helps meet data protection requirements under GDPR, HIPAA, CCPA, and other privacy laws.
- **🛡️ Reduced Risk** – Lowers the likelihood of data leaks, breaches, or unauthorized access.
- **🤝 Ethical AI Adoption** – Builds trust by respecting user privacy and showing a commitment to responsible AI practices.
- **🚫 Safer Model Training** – Stops sensitive data from being unintentionally used in future model training.

## Named Entity Recognition (NER):
Named Entity Recognition (NER) is a Natural Language Processing (NLP) technique that can identify entities like names, organizations, locations, dates, or numbers into predefined categories, which is difficult to identify with regex alone.

## NER in LLM Masking
Here is how NER can be used in LLM Masking:
1. **Detect PII** – NER scans the text to find sensitive details like names, phone numbers, or addresses.
2. **Mask Entities** – These entities are replaced with safe placeholder tokens before sending the text to an LLM API.
3. **Process Securely** – The masked text is sent to the model, ensuring no raw PII leaves your system.
4. **Reinsert Data** – Once processing is complete, the original information can be safely restored if required.

## NER Implementation using spaCy:
### Why SpaCy?
`en_core_web_sm` is a small English model from spaCy that you can download and run directly on your local machine. The model is lightweight (around 12 MB) but still capable of handling essential NLP tasks like Named Entity Recognition (NER).

Because it runs entirely offline, your text never leaves your environment — ensuring high privacy and control over sensitive data. This makes spaCy an excellent choice for privacy-first AI workflows, such as masking personally identifiable information (PII) before sending text to an LLM.

### Install:
```python
pip install spacy
python -m spacy download en_core_web_sm
```

### Code Implementation:
```python
import spacy
import re

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Example text
text = "Hi, I’m Alice Johnson from Acme Corp. Email me at alice.j@example.com."

# Step 1: Detect PII and replace with placeholders
doc = nlp(text)
mapping = {}
masked_text = text
for i, ent in enumerate(doc.ents, 1):
    if ent.label_ in {"PERSON", "ORG", "GPE"}:  # mask only key PII
        placeholder = f"<<PII:{ent.label_}:{i}>>"
        mapping[placeholder] = ent.text
        masked_text = masked_text.replace(ent.text, placeholder)

print("Masked text:", masked_text)

# Step 2: Send masked text to LLM (dummy example here)
llm_response = masked_text.replace("Hi", "Hello")  # imagine LLM rewrites

print("LLM response (masked):", llm_response)

# Step 3: Put PII back
def unmask(text, mapping):
    return re.sub(r"<<PII:[A-Z]+:\d+>>", lambda m: mapping.get(m.group(0), m.group(0)), text)

final_output = unmask(llm_response, mapping)
print("Final output:", final_output)
```

### Output:
```
Masked text: Hi, I’m <<PII:PERSON:1>> from <<PII:ORG:2>> Email me at <<PII:ORG:3>>.
LLM response (masked): Hello, I’m <<PII:PERSON:1>> from <<PII:ORG:2>> Email me at <<PII:ORG:3>>.
Final output: Hello, I’m Alice Johnson from Acme Corp. Email me at alice.j@example.com.
```

## NER Implementation using DistilBERT-based model:
### Why distilbert_finetuned_ai4privacy_v2?
`Isotonic/distilbert_finetuned_ai4privacy_v2` is a DistilBERT-based model fine-tuned for privacy and sensitive data detection. It can identify personally identifiable information (PII) such as names, emails, phone numbers, and other private entities in text.

Once downloaded through Hugging Face, the model runs locally in your environment. With a size of around 250 MB, it provides a balance between performance and accuracy, making it practical for real-world enterprise workflows. Because all processing happens on your own system after the initial download, no data needs to leave your environment — ensuring strong privacy and compliance for applications like LLM masking and secure data preprocessing.

### Install:
```python
pip install transformers torch
```

### Code Implementation:
```python
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
import re

# 1) Load the privacy NER model (HF)
model_id = "Isotonic/distilbert_finetuned_ai4privacy_v2"
tok = AutoTokenizer.from_pretrained(model_id)
mdl = AutoModelForTokenClassification.from_pretrained(model_id)
ner = pipeline("token-classification", model=mdl, tokenizer=tok, aggregation_strategy="simple")

# 2) Example text
text = "Hi, I'm Alice Johnson from Acme Corp. Email me at alice.j@example.com or call +1 312-555-0199."

# 3) Run NER → collect spans (mask ALL detected entities; adjust if you want a subset)
ents = ner(text)
spans = sorted([(e["start"], e["end"], e["entity_group"], text[e["start"]:e["end"]]) for e in ents], key=lambda x: x[0])

# 4) Build masked text with stable placeholders
PLACEHOLDER = "<<<PII:{label}:{idx}>>>"
mapping, out, last, counters = {}, [], 0, {}
for s, e, lbl, val in spans:
    if s < last:  # skip overlaps already covered
        continue
    out.append(text[last:s])
    counters[lbl] = counters.get(lbl, 0) + 1
    ph = PLACEHOLDER.format(label=lbl, idx=counters[lbl])
    out.append(ph)
    mapping[ph] = val
    last = e
out.append(text[last:])
masked = "".join(out)

print("Masked:", masked)

# 5) Send to LLM (stub). Important: tell your LLM to KEEP placeholders verbatim.
llm_out_masked = masked.replace("Hi", "Hello")  # pretend LLM rewrite

# 6) Put PII back
PH_RE = re.compile(r"<<<PII:[A-Z0-9_]+:\d+>>>")
unmasked = PH_RE.sub(lambda m: mapping.get(m.group(0), m.group(0)), llm_out_masked)

print("LLM (masked):", llm_out_masked)
print("Final:", unmasked)
```

### Output:
```
Masked: Hi, I'm <<<PII:FIRSTNAME:1>>> <<<PII:LASTNAME:1>>> from <<<PII:COMPANYNAME:1>>>. Email me at <<<PII:EMAIL:1>>> or call <<<PII:PHONENUMBER:1>>>.
LLM (masked): Hello, I'm <<<PII:FIRSTNAME:1>>> <<<PII:LASTNAME:1>>> from <<<PII:COMPANYNAME:1>>>. Email me at <<<PII:EMAIL:1>>> or call <<<PII:PHONENUMBER:1>>>.
Final: Hello, I'm Alice Johnson from Acme Corp. Email me at alice.j@example.com or call +1 312-555-0199.
```

