"""
LAYER 2: 7 SPECIALIZED AGENTS - EACH TAB HAS UNIQUE PURPOSE
"""

import requests
from layer1_tools import LegalTools

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2"

def call_ollama(prompt, document_text):
    """Call Ollama API"""
    
    if not document_text or len(document_text) < 50:
        return get_fallback_response(prompt, document_text)
    
    doc_short = document_text[:3000]
    
    full_prompt = f"""You are a legal document analyzer. Answer based ONLY on the document.

DOCUMENT:
{doc_short}

TASK: {prompt}

Be direct and helpful. Use the document content."""

    payload = {
        "model": MODEL_NAME,
        "prompt": full_prompt,
        "stream": False,
        "temperature": 0.3,
        "max_tokens": 800
    }
    
    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=60)
        if response.status_code == 200:
            return response.json()["response"]
        else:
            return get_fallback_response(prompt, document_text)
    except:
        return get_fallback_response(prompt, document_text)


def get_fallback_response(prompt, document_text):
    """Fallback responses - EACH TAB UNIQUE"""
    
    doc_lower = document_text.lower() if document_text else ""
    prompt_lower = prompt.lower()
    
    # Detect risks
    has_noncompete = "non-compete" in doc_lower or "noncompete" in doc_lower
    has_indemnity = "indemnification" in doc_lower or "indemnify" in doc_lower
    has_arbitration = "arbitration" in doc_lower
    has_delaware = "delaware" in doc_lower
    has_ip = "intellectual property" in doc_lower or "ip" in doc_lower
    has_termination = "termination" in doc_lower
    has_payment = "pay" in doc_lower or "fee" in doc_lower or "rate" in doc_lower
    
    risk_score = 25
    if has_noncompete:
        risk_score += 30
    if has_indemnity:
        risk_score += 30
    if has_arbitration and has_delaware:
        risk_score += 20
    if has_ip:
        risk_score += 10
    risk_score = min(risk_score, 95)
    
    # ============================================
    # TAB 1: SUMMARY - Document overview
    # ============================================
    if "summarize" in prompt_lower or "summary" in prompt_lower:
        # Find first few sentences as preview
        preview = document_text[:500] if document_text else "No document loaded"
        
        return f"""📄 **DOCUMENT SUMMARY**

**Document Type:** {'Service/Employment Agreement' if 'agreement' in doc_lower or 'contract' in doc_lower else 'Legal Document'}

**What this document is about:**
This document outlines the terms and conditions between parties for professional services.

**Key Sections Found:**
{'- Termination clause' if has_termination else ''}
{'- Payment terms' if has_payment else ''}
{'- Non-compete clause' if has_noncompete else ''}
{'- Indemnification clause' if has_indemnity else ''}
{'- Arbitration clause' if has_arbitration else ''}
{'- Intellectual Property clause' if has_ip else ''}

**Document Preview:**
> {preview[:300]}...

**Overall Risk Level:** {'HIGH' if risk_score >= 70 else 'MEDIUM' if risk_score >= 50 else 'LOW'} ({risk_score}/100)

**Quick Verdict:** {'⚠️ Review carefully before signing' if risk_score >= 50 else '✅ Generally acceptable'}

💡 **Next:** Click "RISK ASSESSMENT" tab for detailed risk analysis."""

    # ============================================
    # TAB 1: RISK ASSESSMENT - Detailed risks with scores
    # ============================================
    elif "risk" in prompt_lower:
        risks = []
        if has_noncompete:
            risks.append("🔴 **Non-compete Clause** - Score: 9/10\n   - Problem: Restricts your future work\n   - Law: Section 27, Indian Contract Act (may be void)\n   - Action: Demand removal or reduce to 6 months\n")
        if has_indemnity:
            risks.append("🔴 **Indemnification Clause** - Score: 9/10\n   - Problem: You pay their legal fees\n   - Law: Section 124, Indian Contract Act\n   - Action: Limit to your own fault only\n")
        if has_arbitration and has_delaware:
            risks.append("🟠 **Foreign Arbitration** - Score: 7/10\n   - Problem: Disputes in Delaware, USA\n   - Law: Arbitration Act, 1996\n   - Action: Change to Indian jurisdiction\n")
        if has_ip:
            risks.append("🟡 **IP Assignment** - Score: 6/10\n   - Problem: You lose ownership of your work\n   - Law: Copyright Act, 1957 - Section 17\n   - Action: Change to license instead of assignment\n")
        
        if risks:
            return f"""⚠️ **DETAILED RISK ASSESSMENT**

**OVERALL RISK SCORE: {risk_score}/100**

**RISKS IDENTIFIED:**

{chr(10).join(risks)}

**FINAL VERDICT:** {'❌ DO NOT SIGN - Too many high-risk clauses' if risk_score >= 60 else '⚠️ SIGN WITH CHANGES - Negotiate the risks above'}

**RECOMMENDED ACTION:** {'Demand removal of non-compete and indemnification clauses before signing.' if has_noncompete or has_indemnity else 'Review all clauses carefully before signing.'}"""
        else:
            return f"""⚠️ **RISK ASSESSMENT**

**RISK SCORE: {risk_score}/100** - LOW RISK

**RISKS FOUND:** No major risks detected in this document.

**VERDICT:** ✅ SAFE TO SIGN

**ACTION:** Sign after verifying all dates, payment terms, and blank fields are filled correctly."""

    # ============================================
    # TAB 2: NEGOTIATION - What to change
    # ============================================
    elif "negotiation" in prompt_lower:
        response = "🤝 **NEGOTIATION STRATEGY**\n\n"
        
        if has_noncompete:
            response += """**1. NON-COMPETE CLAUSE - MUST DELETE**

**Current Problem:** You cannot work for competitors for an extended period.

**Legal Basis:** Section 27 of Indian Contract Act, 1872 - "Agreements in restraint of trade are void"

**What to Demand:**
> "Delete the non-compete clause entirely. Under Section 27 of the Indian Contract Act, this clause is likely void and unenforceable."

**Alternative Proposal:** Limit to 6 months and only clients you personally worked with.

---
"""
        
        if has_indemnity:
            response += """**2. INDEMNIFICATION CLAUSE - MUST CHANGE**

**Current Problem:** You must pay for the other party's legal fees.

**Legal Basis:** Section 124 of Indian Contract Act, 1872 - One-sided indemnity is unfair

**What to Demand:**
> "Change the indemnification clause so each party bears its own legal fees. Indemnification should only apply for gross negligence."

**Alternative Proposal:** Limit indemnity to claims arising directly from your own fault only.

---
"""
        
        if has_arbitration and has_delaware:
            response += """**3. ARBITRATION CLAUSE - CHANGE LOCATION**

**Current Problem:** Disputes to be resolved in Delaware, USA (expensive for you)

**Legal Basis:** Arbitration and Conciliation Act, 1996 - Section 7

**What to Demand:**
> "Change the arbitration venue to [Your City], India. Foreign arbitration is impractical and expensive."

**Alternative Proposal:** Use local courts in your city instead of arbitration.

---
"""
        
        if not has_noncompete and not has_indemnity:
            response += "✅ **No Major Issues Found**\n\nThis document appears fair. You can sign after verifying:\n- All dates are correct\n- Payment terms match what was discussed\n- All blank fields are filled\n"
        
        response += """
**💬 EXACT WORDS TO SAY IN NEGOTIATION:**

"After reviewing the agreement, I have concerns with a few clauses that are problematic under Indian law. Specifically:

1. The non-compete clause - Under Section 27 of the Indian Contract Act, this is likely void.
2. The indemnification clause - This is one-sided and unfair.

Please remove these clauses or we cannot proceed."

**🚪 WALK AWAY IF:** They refuse to remove the non-compete or indemnification clauses."""
        
        return response

    # ============================================
    # TAB 3: COMPARISON - Handled by ComparisonAgent
    # ============================================
    
    # ============================================
    # TAB 4: LEGAL LAWS - Specific laws for this document
    # ============================================
    elif "laws" in prompt_lower:
        response = "⚖️ **INDIAN LAWS APPLICABLE TO YOUR DOCUMENT**\n\n"
        
        if has_noncompete:
            response += """**📜 Indian Contract Act, 1872 - Section 27**
- **What it says:** "Every agreement by which anyone is restrained from exercising a lawful profession, trade or business is void."
- **How it applies:** The non-compete clause in your document may be completely VOID if it's unreasonable.
- **Your right:** You can ignore unreasonable non-compete clauses.

"""
        
        if has_indemnity:
            response += """**📜 Indian Contract Act, 1872 - Section 124**
- **What it says:** Defines a contract of indemnity as a promise to save another from loss.
- **How it applies:** One-sided indemnity clauses are considered unfair.
- **Your right:** You should only indemnify for losses caused by YOUR actions, not theirs.

"""
        
        if has_arbitration:
            response += """**📜 Arbitration and Conciliation Act, 1996 - Section 7**
- **What it says:** Arbitration agreements must be in writing.
- **How it applies:** The arbitration clause must be clear and agreed by both parties.
- **Your right:** You can challenge unfair arbitration locations.

"""
        
        if has_ip:
            response += """**📜 Copyright Act, 1957 - Section 17**
- **What it says:** The author is the first owner of copyright.
- **How it applies:** You own what you create unless you explicitly sign it away.
- **Your right:** You can negotiate to keep ownership and give only a license.

"""
        
        if not has_noncompete and not has_indemnity and not has_arbitration and not has_ip:
            response += "✅ No specific laws triggered. Your document appears standard.\n\n"
        
        response += """
**⚠️ IMPORTANT:** These laws protect you. Use them in negotiation. If a clause violates these laws, it may be unenforceable."""
        
        return response
    
    # ============================================
    # CHAT: Answer any question
    # ============================================
    else:
        return f"""📋 **ANSWER**

Based on your document analysis:

- **Risk Score:** {risk_score}/100
- **Main Issues:** {', '.join([r for r in ['Non-compete' if has_noncompete else '', 'Indemnification' if has_indemnity else '', 'Foreign Arbitration' if has_arbitration and has_delaware else ''] if r]) or 'None'}

**Specific Answer to Your Question:**

{prompt}

💡 **Try these specific commands:**
- Click "SUMMARIZE" for document overview
- Click "RISK ASSESSMENT" for detailed risks
- Click "NEGOTIATION" for what to change
- Click "LEGAL LAWS" for applicable laws"""


# ============================================
# AGENT CLASSES
# ============================================

class SummarizerAgent:
    def summarize(self, text, doc_name="Document"):
        """TAB 1: Document summary"""
        return call_ollama("summarize", text)


class RiskAgent:
    def analyze(self, text, doc_name="Document"):
        """TAB 1: Risk assessment"""
        return call_ollama("risk assessment", text)


class DecisionAgent:
    def decide(self, text, question=""):
        """CHAT: Answer questions"""
        return call_ollama(question, text)


class NegotiationAgent:
    def __init__(self):
        self.tools = LegalTools()
    
    def get_advice(self, document_text, doc_name="Document"):
        """TAB 2: Negotiation strategy"""
        return call_ollama("negotiation advice", document_text)


class ComparisonAgent:
    def compare(self, doc1, doc2, name1, name2):
        """TAB 3: Compare two documents"""
        def score(text):
            s = 25
            if "non-compete" in text.lower():
                s += 30
            if "indemnification" in text.lower():
                s += 30
            if "arbitration" in text.lower() and "delaware" in text.lower():
                s += 20
            return min(s, 95)
        
        s1 = score(doc1)
        s2 = score(doc2)
        
        # Get document previews
        preview1 = doc1[:300] if len(doc1) > 300 else doc1
        preview2 = doc2[:300] if len(doc2) > 300 else doc2
        
        if s1 < s2:
            winner = name1
            reason = f"Lower risk score ({s1}/100 vs {s2}/100)"
            winner_score = s1
            loser_score = s2
        else:
            winner = name2
            reason = f"Lower risk score ({s2}/100 vs {s1}/100)"
            winner_score = s2
            loser_score = s1
        
        return f"""## 🏆 DOCUMENT COMPARISON

### Winner: **{winner}**

| Document | Risk Score | Verdict |
|----------|------------|---------|
| {name1} | {s1}/100 | {'❌ High Risk' if s1 >= 60 else '✅ Low Risk'} |
| {name2} | {s2}/100 | {'❌ High Risk' if s2 >= 60 else '✅ Low Risk'} |

### Why {winner} is better:
{reason}

### Document Previews:

**{name1}:** {preview1}...

**{name2}:** {preview2}...

### Final Recommendation:
Choose **{winner}** for signing. It has {'fewer' if winner_score < loser_score else 'better'} terms for you.

💡 **Next Step:** Go to the NEGOTIATION tab for specific changes needed for the losing document."""


class LawsAgent:
    def __init__(self):
        self.tools = LegalTools()
    
    def get_relevant_laws(self, document_text, doc_name="Document"):
        """TAB 4: Legal laws"""
        return call_ollama("laws", document_text)