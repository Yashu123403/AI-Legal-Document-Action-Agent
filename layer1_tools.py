"""
LAYER 1: TOOLS & KNOWLEDGE BASE
Legal risk patterns, Indian law references, text utilities
"""

import re
from nltk.tokenize import sent_tokenize
import nltk

try:
    nltk.data.find('tokenizers/punkt')
except:
    nltk.download('punkt', quiet=True)

try:
    nltk.data.find('tokenizers/punkt_tab')
except:
    nltk.download('punkt_tab', quiet=True)


class LegalTools:

    RISK_DATABASE = {
        "indemnification": {
            "risk_score": 9,
            "problem": "You MUST pay for their legal fees",
            "delete_text": "DELETE this entire indemnification clause",
            "replace_with": "Each party bears its own legal fees. No indemnification except for gross negligence.",
            "legal_basis": "Indian Contract Act, 1872 - Section 124"
        },
        "indemnify": {
            "risk_score": 9,
            "problem": "You are liable for their losses",
            "delete_text": "DELETE or narrow indemnify clause",
            "replace_with": "Indemnity limited to direct losses caused by your own fault only.",
            "legal_basis": "Indian Contract Act, 1872 - Section 124"
        },
        "arbitration": {
            "risk_score": 8,
            "problem": "You LOSE your right to sue in court",
            "delete_text": "DELETE the arbitration clause or negotiate seat of arbitration to your city",
            "replace_with": "Disputes resolved in [Your City] courts. Both parties consent to jurisdiction.",
            "legal_basis": "Arbitration and Conciliation Act, 1996 - Section 7"
        },
        "non-compete": {
            "risk_score": 9,
            "problem": "You CANNOT work for competitors — likely void under Indian law",
            "delete_text": "DELETE or drastically narrow this clause",
            "replace_with": "For 6 months, cannot solicit clients you personally worked with.",
            "legal_basis": "Indian Contract Act, 1872 - Section 27"
        },
        "non compete": {
            "risk_score": 9,
            "problem": "You CANNOT work for competitors — likely void under Indian law",
            "delete_text": "DELETE or drastically narrow this clause",
            "replace_with": "For 6 months, cannot solicit clients you personally worked with.",
            "legal_basis": "Indian Contract Act, 1872 - Section 27"
        },
        "limitation of liability": {
            "risk_score": 8,
            "problem": "They CAP what they owe you in damages",
            "delete_text": "DELETE the liability cap or set it to full contract value",
            "replace_with": "Liability limited to total fees paid, except for fraud or gross negligence.",
            "legal_basis": "Indian Contract Act, 1872 - Section 73"
        },
        "termination fee": {
            "risk_score": 7,
            "problem": "You PAY a penalty to cancel the contract",
            "delete_text": "DELETE the termination fee clause",
            "replace_with": "Either party may terminate with 15 days written notice. No penalty.",
            "legal_basis": "Indian Contract Act, 1872 - Section 74"
        },
        "auto-renewal": {
            "risk_score": 7,
            "problem": "Contract RENEWS automatically — you may miss the window to cancel",
            "delete_text": "DELETE auto-renewal or add 30-day cancellation notice window",
            "replace_with": "Contract renews only with written consent from both parties.",
            "legal_basis": "Indian Contract Act, 1872 - Section 10"
        },
        "intellectual property": {
            "risk_score": 8,
            "problem": "You may LOSE ownership of work you create",
            "delete_text": "DELETE the IP assignment clause",
            "replace_with": "You retain all IP. Client gets a license to use deliverables only.",
            "legal_basis": "Copyright Act, 1957 - Section 17"
        },
        "unilateral": {
            "risk_score": 9,
            "problem": "They can CHANGE terms without your consent",
            "delete_text": "DELETE unilateral modification clause",
            "replace_with": "Changes require written consent from BOTH parties.",
            "legal_basis": "Indian Contract Act, 1872 - Section 62"
        },
        "governing law": {
            "risk_score": 6,
            "problem": "Disputes may be in THEIR location, not yours",
            "delete_text": "CHANGE governing law clause to your jurisdiction",
            "replace_with": "Governing law: India. Venue: [Your City] courts.",
            "legal_basis": "Code of Civil Procedure, 1908 - Section 20"
        },
        "penalty": {
            "risk_score": 7,
            "problem": "Penalty clauses can be used against you",
            "delete_text": "LIMIT penalty to actual proven losses only",
            "replace_with": "Penalty shall not exceed actual losses suffered.",
            "legal_basis": "Indian Contract Act, 1872 - Section 74"
        },
        "confidentiality": {
            "risk_score": 5,
            "problem": "Overly broad confidentiality can restrict you unfairly",
            "delete_text": "NARROW scope and add time limit",
            "replace_with": "Confidentiality applies for 2 years and excludes publicly available information.",
            "legal_basis": "Indian Contract Act, 1872 - Section 10"
        },
        "force majeure": {
            "risk_score": 3,
            "problem": "Generally fair but check if it covers your obligations too",
            "delete_text": "Ensure clause applies equally to BOTH parties",
            "replace_with": "Force majeure applies equally to both parties for unforeseeable events.",
            "legal_basis": "Indian Contract Act, 1872 - Section 32"
        },
    }

    INDIAN_LAWS = {
        "Indian Contract Act, 1872": {
            "triggers": ["contract", "agreement", "termination", "breach", "indemnity",
                         "non-compete", "liability", "penalty", "sign", "clause"],
            "key_sections": {
                "S.10": "Valid contract needs free consent, competent parties, lawful object",
                "S.23": "Agreements against public policy are void",
                "S.27": "Restraint of trade (non-compete) is VOID unless reasonable",
                "S.39": "Refusal to perform = other party can terminate",
                "S.62": "Modification needs consent of both parties",
                "S.73": "Damages for breach = actual loss only, not penalty",
                "S.74": "Penalty clause enforced only up to actual loss",
                "S.124": "Contract of indemnity — indemnifier pays loss"
            }
        },
        "Arbitration and Conciliation Act, 1996": {
            "triggers": ["arbitration", "arbitrator", "dispute resolution", "adr"],
            "key_sections": {
                "S.7": "Arbitration agreement must be in writing",
                "S.8": "Court must refer parties to arbitration if agreement exists",
                "S.34": "Award can be set aside for fraud, patent illegality"
            }
        },
        "Copyright Act, 1957": {
            "triggers": ["copyright", "intellectual property", "ip", "ownership", "work product"],
            "key_sections": {
                "S.17": "Author is FIRST owner of copyright",
                "S.18": "Copyright can be assigned",
                "S.19": "Assignment must be in writing and signed"
            }
        },
        "Consumer Protection Act, 2019": {
            "triggers": ["consumer", "service deficiency", "complaint", "refund"],
            "key_sections": {
                "S.2(7)": "Consumer = person who buys goods/services for personal use",
                "S.35": "Complaint can be filed for deficiency in service",
                "S.39": "Forum can order refund, compensation, removal of deficiency"
            }
        },
        "Code of Civil Procedure, 1908": {
            "triggers": ["jurisdiction", "court", "venue", "suit", "governing law"],
            "key_sections": {
                "S.20": "Suit filed where defendant resides or cause of action arose",
                "S.9": "Civil courts have jurisdiction over all civil disputes"
            }
        },
        "Transfer of Property Act, 1882": {
            "triggers": ["rent", "lease", "tenancy", "property", "premises", "landlord", "tenant"],
            "key_sections": {
                "S.105": "Lease = transfer of right to enjoy property for time/consideration",
                "S.106": "Default lease period is month-to-month if not specified",
                "S.108": "Rights and liabilities of lessor and lessee"
            }
        }
    }

    @staticmethod
    def find_risks(text):
        text_lower = text.lower()
        found = []
        for risk_key in LegalTools.RISK_DATABASE:
            if risk_key in text_lower:
                found.append(risk_key)
        return found

    @staticmethod
    def calculate_risk_score(text):
        text_lower = text.lower()
        score = 10  # base
        for risk_key, data in LegalTools.RISK_DATABASE.items():
            if risk_key in text_lower:
                score += data["risk_score"] * 4
        return min(score, 98)

    @staticmethod
    def get_applicable_laws(text):
        text_lower = text.lower()
        applicable = []
        for law, data in LegalTools.INDIAN_LAWS.items():
            if any(kw in text_lower for kw in data["triggers"]):
                applicable.append(law)
        if not applicable:
            applicable = ["Indian Contract Act, 1872"]
        return applicable

    @staticmethod
    def extract_clause(text, keyword):
        try:
            sentences = sent_tokenize(text)
        except Exception:
            sentences = text.split('. ')
        for sent in sentences:
            if keyword.lower() in sent.lower():
                return sent.strip()[:300]
        return f"Clause containing '{keyword}' found in document."

    @staticmethod
    def get_document_type(text):
        text_lower = text.lower()
        if any(w in text_lower for w in ["tenant", "landlord", "rent", "lease", "premises"]):
            return "Rental/Lease Agreement"
        if any(w in text_lower for w in ["employee", "employment", "salary", "designation"]):
            return "Employment Agreement"
        if any(w in text_lower for w in ["service", "vendor", "deliverable", "milestone"]):
            return "Service Agreement"
        if any(w in text_lower for w in ["purchase", "sale", "buyer", "seller", "goods"]):
            return "Sale/Purchase Agreement"
        if any(w in text_lower for w in ["nda", "confidential", "non-disclosure"]):
            return "Non-Disclosure Agreement"
        if any(w in text_lower for w in ["partner", "partnership", "profit sharing"]):
            return "Partnership Agreement"
        return "Legal Contract"