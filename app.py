import streamlit as st
import math
import re

st.set_page_config(
    page_title="Multi Calculator Hub",
    page_icon="🧮",
    layout="centered",
)

# ----------------- GLOBAL STYLING (Modern UI) -----------------
st.markdown(
    """
    <style>
    .stApp {
        background: radial-gradient(circle at top, #1e293b 0, #020617 45%, #000 100%);
        color: #e5e7eb;
        font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }
    .main-card {
        padding: 2rem 2rem 1.8rem 2rem;
        border-radius: 1.5rem;
        background: rgba(15, 23, 42, 0.96);
        box-shadow: 0 24px 60px rgba(0, 0, 0, 0.7);
        border: 1px solid rgba(148, 163, 184, 0.25);
        max-width: 520px;
        margin: 2.5rem auto;
    }
    .app-title {
        font-size: 1.9rem;
        font-weight: 650;
        letter-spacing: 0.08em;
        text-align: center;
        text-transform: uppercase;
        margin-bottom: 0.4rem;
    }
    .app-subtitle {
        text-align: center;
        font-size: 0.9rem;
        color: #9ca3af;
        margin-bottom: 1.8rem;
    }
    .section-title {
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    .display-box {
        width: 100%;
        padding: 0.7rem 1rem;
        border-radius: 0.9rem;
        background: linear-gradient(135deg, #020617, #020617, #0f172a);
        border: 1px solid rgba(148, 163, 184, 0.4);
        font-size: 1.6rem;
        text-align: right;
        color: #e5e7eb;
        box-sizing: border-box;
        margin-bottom: 0.3rem;
        font-variant-numeric: tabular-nums;
    }
    .display-mini {
        width: 100%;
        font-size: 0.8rem;
        text-align: right;
        color: #9ca3af;
        margin-bottom: 1rem;
        min-height: 1.1rem;
    }
    .button-row {
        display: flex;
        gap: 0.6rem;
        margin-bottom: 0.6rem;
    }
    .calc-btn {
        border-radius: 999px !important;
        height: 3rem;
        font-size: 1.05rem;
        font-weight: 500;
        border: none;
    }
    .basic-btn {
        background: #111827;
    }
    .op-btn {
        background: linear-gradient(135deg, #0ea5e9, #6366f1);
    }
    .func-btn {
        background: #020617;
        color: #f97316;
    }
    .eq-btn {
        background: linear-gradient(135deg, #22c55e, #16a34a);
    }
    .css-1v0mbdj p {  /* hacky: reduce default markdown spacing inside card */
        margin-bottom: 0.2rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------- SIDEBAR -----------------
st.sidebar.title("🧮 Calculator Modes")
mode = st.sidebar.radio(
    "Choose calculator type:",
    ["Basic", "Scientific", "Currency Converter", "BMI Calculator"],
)

st.sidebar.markdown("---")
st.sidebar.markdown("**Tip:** Put this repo on GitHub and deploy on Streamlit Cloud 🔥")


# ----------------- BASIC CALCULATOR (BUTTON GRID) -----------------
if "basic_expr" not in st.session_state:
    st.session_state.basic_expr = "0"
if "basic_last" not in st.session_state:
    st.session_state.basic_last = ""


ALLOWED_BASIC = re.compile(r"^[0-9+\-*/().% ]+$")


def safe_eval_basic(expr: str) -> str:
    expr = expr.replace("×", "*").replace("÷", "/")
    expr = expr.replace(" ", "")

    if not expr:
        return "0"

    if not ALLOWED_BASIC.match(expr):
        return "Error"

    try:
        value = eval(expr, {"__builtins__": {}}, {})
    except Exception:
        return "Error"

    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value)


def basic_press(key: str):
    exp = st.session_state.basic_expr

    if key == "C":
        st.session_state.basic_expr = "0"
        st.session_state.basic_last = ""
        return

    if key == "⌫":
        if len(exp) <= 1:
            st.session_state.basic_expr = "0"
        else:
            st.session_state.basic_expr = exp[:-1]
        return

    if key == "=":
        result = safe_eval_basic(exp)
        st.session_state.basic_last = exp + " ="
        st.session_state.basic_expr = result
        return

    if exp == "0" and key not in [".", "%"]:
        exp = ""

    st.session_state.basic_expr = exp + key


# ----------------- SCIENTIFIC CALCULATOR -----------------
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
    "pow": pow,
}


def safe_eval_sci(expr: str) -> str:
    if not expr.strip():
        return ""
    try:
        val = eval(expr, {"__builtins__": None}, allowed_funcs)
    except Exception:
        return "Error"

    try:
        if isinstance(val, float) and val.is_integer():
            return str(int(val))
        return str(val)
    except Exception:
        return "Error"


# ----------------- CURRENCY CONVERTER -----------------
# simple static rates relative to 1 USD (not live!)
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


# ----------------- BMI CALCULATOR -----------------
def bmi_category(bmi: float) -> str:
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal weight"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obese"


# ================= MAIN UI CARD =================
st.markdown('<div class="main-card">', unsafe_allow_html=True)
st.markdown('<div class="app-title">Multi Calculator</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="app-subtitle">Basic • Scientific • Currency • BMI</div>',
    unsafe_allow_html=True,
)

# ----------------- MODE: BASIC -----------------
if mode == "Basic":
    st.markdown('<div class="section-title">Basic Calculator</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="display-box">{st.session_state.basic_expr}</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<div class="display-mini">{st.session_state.basic_last}</div>',
        unsafe_allow_html=True,
    )

    rows = [
        ["C", "⌫", "%", "÷"],
        ["7", "8", "9", "×"],
        ["4", "5", "6", "-"],
        ["1", "2", "3", "+"],
        ["0", ".", "=", ""],
    ]

    for i, row in enumerate(rows):
        cols = st.columns(4, gap="small")
        for j, label in enumerate(row):
            if label == "":
                cols[j].write("")
                continue

            if label in ["C", "⌫"]:
                btn_class = "func-btn"
            elif label in ["÷", "×", "-", "+", "%"]:
                btn_class = "op-btn"
            elif label == "=":
                btn_class = "eq-btn"
            else:
                btn_class = "basic-btn"

            with cols[j]:
                if st.button(
                    label,
                    key=f"basic_{i}_{j}_{label}",
                    use_container_width=True,
                ):
                    key = label
                    if key == "÷":
                        key = "/"
                    elif key == "×":
                        key = "*"
                    basic_press(key)

# ----------------- MODE: SCIENTIFIC -----------------
elif mode == "Scientific":
    st.markdown('<div class="section-title">Scientific Calculator</div>', unsafe_allow_html=True)
    st.caption("Use functions: sin(x), cos(x), tan(x), log(x), log10(x), sqrt(x), pi, e, abs(x)")

    st.session_state.sci_expr = st.text_input(
        "Expression",
        value=st.session_state.sci_expr,
        placeholder="e.g. sin(pi/2) + log(10)",
    )

    func_cols = st.columns(4)
    sci_buttons = ["sin(", "cos(", "tan(", "sqrt("]
    for i, b in enumerate(sci_buttons):
        if func_cols[i].button(b, key=f"sci_func_{b}"):
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

# ----------------- MODE: CURRENCY CONVERTER -----------------
elif mode == "Currency Converter":
    st.markdown('<div class="section-title">Currency Converter</div>', unsafe_allow_html=True)
    st.caption("Static sample rates – not real-time forex data.")

    amount = st.number_input("Amount", min_value=0.0, value=100.0, step=1.0)
    col_from, col_to = st.columns(2)
    with col_from:
        from_curr = st.selectbox("From", list(RATES.keys()), index=1)  # default INR
    with col_to:
        to_curr = st.selectbox("To", list(RATES.keys()), index=0)  # default USD

    if st.button("Convert"):
        if from_curr == to_curr:
            st.info("Both currencies are the same. Result is the same as amount.")
            result = amount
        else:
            result = convert_currency(amount, from_curr, to_curr)

        st.markdown(
            f"**{amount:.2f} {from_curr} ≈ {result:.2f} {to_curr}**"
        )

# ----------------- MODE: BMI CALCULATOR -----------------
elif mode == "BMI Calculator":
    st.markdown('<div class="section-title">BMI Calculator</div>', unsafe_allow_html=True)
    st.caption("Body Mass Index based on height & weight.")

    col_w, col_h = st.columns(2)
    with col_w:
        weight = st.number_input("Weight (kg)", min_value=0.0, value=60.0, step=0.5)
    with col_h:
        height_cm = st.number_input("Height (cm)", min_value=0.0, value=170.0, step=0.5)

    if st.button("Calculate BMI"):
        if height_cm <= 0 or weight <= 0:
            st.error("Please enter valid height and weight.")
        else:
            height_m = height_cm / 100.0
            bmi = weight / (height_m ** 2)
            category = bmi_category(bmi)
            st.markdown(f"**BMI:** {bmi:.1f}")
            st.markdown(f"**Category:** {category}")

st.markdown("</div>", unsafe_allow_html=True)

st.markdown(
    """
    <p style='text-align:center; font-size:0.8rem; color:#64748b; margin-top:0.8rem;'>
    Built with ❤️ using Streamlit
    </p>
    """,
    unsafe_allow_html=True,
)
