import streamlit as st
import re
import math
import google.generativeai as genai

def password_strength(password):
    score = 0
    feedback = []

    if len(password) >= 12:
        score += 2
    elif len(password) >= 8:
        score += 1
    else:
        feedback.append("Password should be at least 8 characters long.")

    if re.search(r"[A-Z]", password):
        score += 1
    else:
        feedback.append("Add at least one uppercase letter.")

    if re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("Add at least one lowercase letter.")

    if re.search(r"\d", password):
        score += 1
    else:
        feedback.append("Add at least one number.")

    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        score += 1
    else:
        feedback.append("Add at least one special character.")

    if score <= 2:
        strength = "Weak"
    elif score <= 4:
        strength = "Medium"
    elif score == 5:
        strength = "Strong"
    else:
        strength = "Very Strong"

    return strength, score, feedback


# -----------------------------
# Entropy Calculator
# -----------------------------
def calculate_entropy(password):
    charset = 0

    if re.search(r"[a-z]", password):
        charset += 26

    if re.search(r"[A-Z]", password):
        charset += 26

    if re.search(r"\d", password):
        charset += 10

    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        charset += 32

    if charset == 0:
        return 0

    entropy = len(password) * math.log2(charset)
    return round(entropy, 2)


# -----------------------------
# Risk Analyzer
# -----------------------------
def risk_analyzer(password):
    risks = []

    common_passwords = [
        "password",
        "123456",
        "12345678",
        "qwerty",
        "admin",
        "welcome",
        "abc123"
    ]

    if password.lower() in common_passwords:
        risks.append("Common password detected.")

    if re.search(r"(.)\1{2,}", password):
        risks.append("Repeated characters detected.")

    patterns = [
        "1234",
        "2345",
        "3456",
        "4567",
        "5678",
        "6789",
        "abcd",
        "bcde",
        "cdef"
    ]

    for p in patterns:
        if p.lower() in password.lower():
            risks.append("Sequential pattern detected.")
            break

    return risks


# -----------------------------
# Recommendation Engine
# -----------------------------
def recommendation_engine(password):
    recommendations = []

    if len(password) < 12:
        recommendations.append("Use at least 12 characters.")

    if not re.search(r"[A-Z]", password):
        recommendations.append("Add uppercase letters.")

    if not re.search(r"[a-z]", password):
        recommendations.append("Add lowercase letters.")

    if not re.search(r"\d", password):
        recommendations.append("Add numbers.")

    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        recommendations.append("Add special characters.")

    return recommendations


# -----------------------------
# Security Score
# -----------------------------
def security_score(score, entropy, risks):
    final_score = score * 15

    if entropy > 60:
        final_score += 20
    elif entropy > 40:
        final_score += 10

    final_score -= len(risks) * 10

    return max(0, min(100, final_score))


# -----------------------------
# Gemini Policy Generator
# -----------------------------
def generate_password_policy(org_type, employees, security_level, api_key):
    try:
        genai.configure(api_key=api_key)

        model = genai.GenerativeModel(
            "gemini-3.5-flash-lite"
        )

        prompt = f"""
Generate a professional password security policy.

Organization Type: {org_type}
Number of Employees: {employees}
Security Level: {security_level}

Include:
1. Minimum Password Length
2. Complexity Requirements
3. Password Expiry Policy
4. Password History Policy
5. Multi-Factor Authentication
6. Account Lockout Policy
7. Security Best Practices

Format the response professionally.
"""

        response = model.generate_content(prompt)

        return response.text

    except Exception as e:
        return f"Error: {str(e)}"


# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(
    page_title="Password Security Advisor",
    page_icon="🔐",
    layout="wide"
)

st.title("🔐 Password Security Advisor")

tab1, tab2 = st.tabs(
    ["Password Analysis", "Policy Generator"]
)

# =============================
# TAB 1
# =============================
with tab1:

    password = st.text_input(
        "Enter Password",
        type="password"
    )

    if st.button("Analyze Password"):

        strength, score, feedback = password_strength(password)

        entropy = calculate_entropy(password)

        risks = risk_analyzer(password)

        recommendations = recommendation_engine(password)

        sec_score = security_score(
            score,
            entropy,
            risks
        )

        st.subheader("Security Report")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Strength", strength)

        with col2:
            st.metric("Entropy", f"{entropy} bits")

        with col3:
            st.metric("Security Score", f"{sec_score}/100")

        st.progress(sec_score / 100)

        st.subheader("Risks")

        if risks:
            for risk in risks:
                st.warning(risk)
        else:
            st.success("No major risks detected.")

        st.subheader("Recommendations")

        if recommendations:
            for rec in recommendations:
                st.info(rec)
        else:
            st.success("Excellent Password!")


# =============================
# TAB 2
# =============================
with tab2:

    st.subheader(
        "Organization Password Policy Generator"
    )

    org_type = st.text_input(
        "Organization Type"
    )

    employees = st.number_input(
        "Number of Employees",
        min_value=1
    )

    security_level = st.selectbox(
        "Security Level",
        ["Low", "Medium", "High"]
    )

    api_key = st.text_input(
        "Gemini API Key",
        type="password"
    )

    if st.button("Generate Policy"):

        if api_key:

            with st.spinner(
                "Generating Password Policy..."
            ):

                policy = generate_password_policy(
                    org_type,
                    employees,
                    security_level,
                    api_key
                )

                if policy.startswith("Error:"):
                    st.error(policy)
                else:
                    st.markdown(policy)

        else:
            st.error(
                "Please enter your Gemini API Key."
            )
