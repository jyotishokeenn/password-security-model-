import streamlit as st
import re
import math
import google.generativeai as genai

# PROJECT IMAGE 
st.image(
    "https://humanfocus.co.uk/wp-content/uploads/password-security-800x800.jpg",
    width=350
)

# Password Strength Checker
def password_strength(password):
    score = 0

    if len(password) >= 12:
        score += 2
    elif len(password) >= 8:
        score += 1

    if re.search(r"[A-Z]", password):
        score += 1

    if re.search(r"[a-z]", password):
        score += 1

    if re.search(r"\d", password):
        score += 1

    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        score += 1

    if score <= 2:
        return "Weak", score
    elif score <= 4:
        return "Medium", score
    elif score == 5:
        return "Strong", score
    else:
        return "Very Strong", score

# Entropy Calculator
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

# Risk Analyzer
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
        risks.append("Common password detected")

    if re.search(r"(.)\1{2,}", password):
        risks.append("Repeated characters detected")

    patterns = [
        "1234", "2345", "3456",
        "4567", "5678", "6789",
        "abcd", "bcde", "cdef"
    ]

    for p in patterns:
        if p in password.lower():
            risks.append("Sequential pattern detected")
            break

    return risks

# Recommendations
def recommendation_engine(password):
    rec = []

    if len(password) < 12:
        rec.append("Use at least 12 characters")

    if not re.search(r"[A-Z]", password):
        rec.append("Add uppercase letters")

    if not re.search(r"[a-z]", password):
        rec.append("Add lowercase letters")

    if not re.search(r"\d", password):
        rec.append("Add numbers")

    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        rec.append("Add special characters")

    return rec

# Security Score
def security_score(score, entropy, risks):
    final = score * 15

    if entropy > 60:
        final += 20
    elif entropy > 40:
        final += 10

    final -= len(risks) * 10

    return max(0, min(100, final))

# Gemini Policy Generator
def generate_password_policy(org_type, employees, security_level, api_key):

    try:
        genai.configure(api_key=api_key)

        model = genai.GenerativeModel(
            "gemini-3.5-flash-lite"
        )

        prompt = f"""
Create a professional password security policy.

Organization Type: {org_type}
Employees: {employees}
Security Level: {security_level}

Include:

1. Password Length
2. Password Complexity
3. Password Expiry
4. Password History
5. Multi-Factor Authentication
6. Account Lockout Rules
7. Security Best Practices

Format professionally.
"""

        response = model.generate_content(prompt)

        return response.text

    except Exception as e:
        return f"Error: {e}"

# Streamlit UI
st.set_page_config(
    page_title="Password Security Advisor",
    page_icon="🔐",
    layout="wide"
)

st.title("🔐 Password Security Advisor")

tab1, tab2 = st.tabs(
    ["Password Analysis", "Policy Generator"]
)

# PASSWORD ANALYSIS
with tab1:

    password = st.text_input(
        "Enter Password",
        type="password"
    )

    if st.button("Analyze Password"):

        if not password:
            st.error("Please enter a password.")
            st.stop()

        strength, score = password_strength(password)

        entropy = calculate_entropy(password)

        risks = risk_analyzer(password)

        recommendations = recommendation_engine(password)

        sec_score = security_score(
            score,
            entropy,
            risks
        )

        st.subheader("Security Report")

        c1, c2, c3 = st.columns(3)

        c1.metric("Strength", strength)
        c2.metric("Entropy", f"{entropy} bits")
        c3.metric("Score", f"{sec_score}/100")

        st.progress(sec_score / 100)

        st.subheader("Risks")

        if risks:
            for r in risks:
                st.warning(r)
        else:
            st.success("No major risks detected.")

        st.subheader("Recommendations")

        if recommendations:
            for r in recommendations:
                st.info(r)
        else:
            st.success("Excellent Password")

# POLICY GENERATOR
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

        if not api_key:
            st.error("Please enter Gemini API Key")

        else:

            with st.spinner(
                "Generating Policy..."
            ):

                policy = generate_password_policy(
                    org_type,
                    employees,
                    security_level,
                    api_key
                )

                st.markdown(policy)
