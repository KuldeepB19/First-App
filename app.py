import streamlit as st
import math

st.set_page_config(
    page_title="Multi Calculator",
    page_icon="🧮",
    layout="centered",
)

# ---------- Minimal styling (faster, still modern) ----------
st.markdown(
    """
    <style>
    .stApp {
        background: #0f172a;
        color: #e5e7eb;
        font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }
    .card {
        padding: 1.5rem 1.5rem 1.2rem 1.5rem;
        border-radius: 1.2rem;
        background: #020617;
        border: 1px solid #1f2937;
        max-width: 500px;
        margin: 2rem auto;
        box-shadow: 0 18px 40px rgba(0,0,0,0.7);
    }
    .title {
        text-align: center;
        font-size: 1.6rem;
        font-weight: 600;
        margin-bottom: 0.2rem;
    }
    .subtitle {
        text-align: center;
        font-size: 0.85rem;
        color: #9ca3af;
        margin-bottom: 1.2rem;
    }
    .display-main {
        width: 100%;
        padding: 0.65rem 0.9rem;
        border-radius: 0.9rem;
        background: #020617;
        border: 1px solid #374151;
        font-size: 1.5rem;
        text-align: right;
        font-variant-numeric: tabular-nums;
        margin-bottom: 0.2rem;
    }
    .display-sub {
        width: 100%;
        font-size: 0.8rem;
        text-align: right;
        color: #9ca3af;
        min-height: 1rem;
        margin-bottom: 0.8rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- BASIC CALCULATOR STATE ----------
if "basic_expr" not in st.session_state:
    st.session_state.basic_expr = "0"
if "basic_last" not in st.session_state:
    st.session_state.basic_last = ""


def safe_eval_basic(expr: str) -> str:
    expr = expr.replace("×", "*").replace("÷", "/")
    expr = expr.replace(" ", "")

    allowed_chars = "0123456789.+-*/()%"
    if any(c not in allowed_chars for c in expr):
        return "Error"

    if not expr:
        return "0"
    try:
        val = eval(expr, {"__builtins__": {}}, {})
    except Exception:
        return "Error"

    if isinstance(val, float) and val.is_integer():
        return str(int(val))
    return str(val)


def basic_press(key: str):
    exp = st.session_state.basic_expr

    # Clear
    if key == "C":
        st.session_state.basic_expr = "0"
        st.session_state.basic_last = ""
        return

    # Backspace
    if key == "⌫":
        if len(exp) <= 1:
            st.session_state.basic_expr = "0"
        else:
            st.session_state.basic_expr = exp[:-1]
        return

    # Toggle sign
    if key == "±":
        if exp.startswith("-"):
            st.session_state.basic_expr = exp[1:]
        else:
            if exp != "0":
                st.session_state.basic_expr = "-" + exp
        return

    # Evaluate
    if key == "=":
        result = safe_eval_basic(exp)
        st.session_state.basic_last = exp + " ="
        st.session_state.basic_expr = result
        return

    # Append normal key
    if exp == "0" and key not in [".", "%"]:
        exp = ""
    st.session_state.basic_expr = exp + key


# ---------- SCIENTIFIC CALC ----------
if "sci_expr" not in st.session_state:
    st.session_state.sci_expr = ""
if "sci_result" not in st.session_state:
    st.session_state.sci_result = ""

allowed_funcs = {
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "log": math.log,    # natural log
    "log10": math.log10,
    "sqrt": math.sqrt,
    "pi": math.pi,
    "e": math.e,
    "abs": abs,
}


def safe_eval_sci(expr: str) -> str:
    if not expr.strip():
        return ""
    try:
        val = eval(expr, {"__builtins__": None}, allowed_funcs)
    except Exception:
        return "Error"

    if isinstance(val, float) and val.is_integer():
        return str(int(val))
    return str(val)


# ---------- CURRENCY CONVERTER ----------
RATES = {
    "USD": 1.0,
    "INR": 83.0,
    "EUR": 0.93,
    "GBP": 0.79,
    "JPY": 156.0,
    "AED": 3.67,
}


def convert_currency(amount: float, from_curr: str, to_curr: str) -> float:
    base = amount / RATES[from_curr]
    return base * RATES[to_curr]


# ---------- BMI ----------
def bmi_category(bmi: float) -> str:
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obese"


# ================= MAIN UI =================
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="title">Multi Calculator</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Basic • Scientific • Currency • BMI</div>',
    unsafe_allow_html=True,
)

tabs = st.tabs(["Basic", "Scientific", "Currency", "BMI"])

# ---------- TAB 1: BASIC ----------
with tabs[0]:
    st.markdown("**Basic Calculator**")

    # Display
    st.markdown(
        f"<div class='display-main'>{st.session_state.basic_expr}</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"<div class='display-sub'>{st.session_state.basic_last}</div>",
        unsafe_allow_html=True,
    )

    # Buttons layout
    rows = [
        ["C", "⌫", "±", "÷"],
        ["7", "8", "9", "×"],
        ["4", "5", "6", "-"],
        ["1", "2", "3", "+"],
        ["0", ".", "%", "="],
    ]

    for i, row in enumerate(rows):
        cols = st.columns(4)
        for j, label in enumerate(row):
            with cols[j]:
                if st.button(label, key=f"basic_{i}_{j}_{label}", use_container_width=True):
                    key = label
                    if key == "÷":
                        key = "/"
                    elif key == "×":
                        key = "*"
                    basic_press(key)

# ---------- TAB 2: SCIENTIFIC ----------
with tabs[1]:
    st.markdown("**Scientific Calculator**")
    st.caption("Example: sin(pi/2) + log(10)")

    st.session_state.sci_expr = st.text_input(
        "Expression",
        value=st.session_state.sci_expr,
        placeholder="Type expression using sin, cos, tan, log, sqrt, pi, e, ...",
    )

    func_cols = st.columns(4)
    sci_buttons = ["sin(", "cos(", "tan(", "sqrt("]
    for i, b in enumerate(sci_buttons):
        if func_cols[i].button(b, key=f"sci_btn_{b}"):
            st.session_state.sci_expr += b

    func_cols2 = st.columns(4)
    more_buttons = ["log(", "log10(", "pi", "e"]
    for i, b in enumerate(more_buttons):
        if func_cols2[i].button(b, key=f"sci_more_{b}"):
            st.session_state.sci_expr += b

    if st.button("Calculate", key="sci_calc"):
        st.session_state.sci_result = safe_eval_sci(st.session_state.sci_expr)

    if st.session_state.sci_result != "":
        st.markdown("**Result:**")
        st.code(str(st.session_state.sci_result))

# ---------- TAB 3: CURRENCY ----------
with tabs[2]:
    st.markdown("**Currency Converter**")
    st.caption("Static demo rates (not live forex).")

    amount = st.number_input("Amount", min_value=0.0, value=100.0, step=1.0)
    col1, col2 = st.columns(2)
    with col1:
        from_curr = st.selectbox("From", list(RATES.keys()), index=1)  # INR default
    with col2:
        to_curr = st.selectbox("To", list(RATES.keys()), index=0)      # USD default

    if st.button("Convert", key="convert_btn"):
        if from_curr == to_curr:
            result = amount
        else:
            result = convert_currency(amount, from_curr, to_curr)
        st.markdown(f"**{amount:.2f} {from_curr} ≈ {result:.2f} {to_curr}**")

# ---------- TAB 4: BMI ----------
with tabs[3]:
    st.markdown("**BMI Calculator**")
    st.caption("Body Mass Index (kg/m²)")

    c1, c2 = st.columns(2)
    with c1:
        weight = st.number_input("Weight (kg)", min_value=0.0, value=60.0, step=0.5)
    with c2:
        height_cm = st.number_input("Height (cm)", min_value=0.0, value=170.0, step=0.5)

    if st.button("Calculate BMI", key="bmi_btn"):
        if weight <= 0 or height_cm <= 0:
            st.error("Please enter valid height and weight.")
        else:
            h_m = height_cm / 100.0
            bmi = weight / (h_m ** 2)
            st.markdown(f"**BMI:** {bmi:.1f}")
            st.markdown(f"**Category:** {bmi_category(bmi)}")

st.markdown("</div>", unsafe_allow_html=True)

st.markdown(
    "<p style='text-align:center; font-size:0.75rem; color:#6b7280;'>Built with Streamlit</p>",
    unsafe_allow_html=True,
)
