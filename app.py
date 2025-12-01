import streamlit as st
import math

st.set_page_config(
    page_title="Multi Calculator",
    page_icon="🧮",
    layout="centered",
)

# -------------------- SESSION STATE SETUP --------------------
if "basic_expr" not in st.session_state:
    st.session_state.basic_expr = "0"
if "basic_last" not in st.session_state:
    st.session_state.basic_last = ""
if "history" not in st.session_state:
    st.session_state.history = []

if "basic_input" not in st.session_state:
    st.session_state.basic_input = ""

if "sci_input" not in st.session_state:
    st.session_state.sci_input = ""
if "sci_result" not in st.session_state:
    st.session_state.sci_result = ""

# -------------------- SIMPLE STYLING --------------------
st.markdown(
    """
    <style>
    .stApp {
        background: #020617;
        color: #e5e7eb;
        font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }
    .card {
        padding: 1.2rem 1.2rem 1rem 1.2rem;
        border-radius: 1rem;
        background: #020617;
        border: 1px solid #1f2937;
        max-width: 520px;
        margin: 1.8rem auto;
    }
    .title {
        text-align: center;
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 0.2rem;
    }
    .subtitle {
        text-align: center;
        font-size: 0.85rem;
        color: #9ca3af;
        margin-bottom: 1rem;
    }
    .display-main {
        width: 100%;
        padding: 0.55rem 0.8rem;
        border-radius: 0.8rem;
        background: #020617;
        border: 1px solid #374151;
        font-size: 1.4rem;
        text-align: right;
        font-variant-numeric: tabular-nums;
        margin-bottom: 0.2rem;
        color: #e5e7eb;
    }
    .display-sub {
        width: 100%;
        font-size: 0.8rem;
        text-align: right;
        color: #9ca3af;
        min-height: 1rem;
        margin-bottom: 0.5rem;
    }
    .section-label {
        font-weight: 600;
        margin-bottom: 0.3rem;
    }
    .stButton > button {
        background: #111827;
        color: #e5e7eb;
        border-radius: 0.6rem;
        border: none;
        padding-top: 0.35rem;
        padding-bottom: 0.35rem;
        font-size: 1.0rem;
        font-weight: 500;
        min-height: 2.2rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------- BASIC CALCULATOR LOGIC --------------------
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


def add_history(expr: str, result: str):
    if result == "Error" or expr.strip() == "":
        return
    item = f"{expr} = {result}"
    st.session_state.history.insert(0, item)
    st.session_state.history = st.session_state.history[:15]


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

    if key == "±":
        if exp.startswith("-"):
            st.session_state.basic_expr = exp[1:]
        else:
            if exp != "0":
                st.session_state.basic_expr = "-" + exp
        return

    if key == "=":
        result = safe_eval_basic(exp)
        st.session_state.basic_last = exp + " ="
        st.session_state.basic_expr = result
        add_history(exp, result)
        return

    if exp == "0" and key not in [".", "%"]:
        exp = ""
    st.session_state.basic_expr = exp + key


def basic_keyboard_submit():
    expr = st.session_state.basic_input.strip()
    allowed = "0123456789.+-*/()% "
    expr = "".join(ch for ch in expr if ch in allowed)

    if expr == "":
        st.session_state.basic_expr = "0"
        st.session_state.basic_last = ""
        return

    st.session_state.basic_expr = expr
    result = safe_eval_basic(expr)
    st.session_state.basic_last = expr + " ="
    st.session_state.basic_expr = result
    add_history(expr, result)


# -------------------- SCIENTIFIC CALCULATOR LOGIC --------------------
allowed_funcs = {
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "log": math.log,
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


def sci_append(text: str):
    st.session_state.sci_input += text


def sci_calculate():
    st.session_state.sci_result = safe_eval_sci(st.session_state.sci_input)


# -------------------- CURRENCY CONVERTER --------------------
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


# -------------------- BMI --------------------
def bmi_category(bmi: float) -> str:
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal"
    elif bmi < 30:
        return "Overweight"
        # else:
    else:
        return "Obese"


# ================= MAIN UI LAYOUT =================
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="title">Multi Calculator</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Basic • Scientific • Currency • BMI</div>',
    unsafe_allow_html=True,
)

tabs = st.tabs(["Basic", "Scientific", "Currency", "BMI"])

# ---------- TAB 1: BASIC ----------
with tabs[0]:
    st.markdown("<div class='section-label'>Basic Calculator</div>", unsafe_allow_html=True)

    # display
    st.markdown(
        f"<div class='display-main'>{st.session_state.basic_expr}</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"<div class='display-sub'>{st.session_state.basic_last}</div>",
        unsafe_allow_html=True,
    )

    # keyboard input (separate state key)
    st.text_input(
        "Keyboard input (press Enter to evaluate)",
        key="basic_input",
        value=st.session_state.basic_expr if st.session_state.basic_expr != "0" else "",
        on_change=basic_keyboard_submit,
        max_chars=40,
    )

    # on-screen buttons
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

    # history under basic
    st.markdown("**History (Basic):**")
    if not st.session_state.history:
        st.caption("No calculations yet.")
    else:
        for item in st.session_state.history[:8]:
            st.caption(item)

# ---------- TAB 2: SCIENTIFIC ----------
with tabs[1]:
    st.markdown("<div class='section-label'>Scientific Calculator</div>", unsafe_allow_html=True)
    st.caption("Example: sin(pi/2) + log(10), sqrt(16), cos(pi)")

    # text input controlled by sci_input key
    st.text_input(
        "Expression",
        key="sci_input",
        placeholder="Use sin, cos, tan, log, sqrt, pi, e, ...",
    )

    # function buttons (callbacks modify sci_input in session_state)
    func_cols = st.columns(4)
    sci_buttons = ["sin(", "cos(", "tan(", "sqrt("]
    for i, b in enumerate(sci_buttons):
        func_cols[i].button(
            b,
            key=f"sci_btn_{b}",
            use_container_width=True,
            on_click=sci_append,
            args=(b,),
        )

    func_cols2 = st.columns(4)
    more_buttons = ["log(", "log10(", "pi", "e"]
    for i, b in enumerate(more_buttons):
        func_cols2[i].button(
            b,
            key=f"sci_more_{b}",
            use_container_width=True,
            on_click=sci_append,
            args=(b,),
        )

    st.button("Calculate", key="sci_calc_btn", on_click=sci_calculate)

    if st.session_state.sci_result != "":
        st.markdown("**Result:**")
        st.code(str(st.session_state.sci_result))

# ---------- TAB 3: CURRENCY ----------
with tabs[2]:
    st.markdown("<div class='section-label'>Currency Converter</div>", unsafe_allow_html=True)
    st.caption("Static demo rates (not real-time forex).")

    amount = st.number_input("Amount", min_value=0.0, value=100.0, step=1.0)
    col1, col2 = st.columns(2)
    with col1:
        from_curr = st.selectbox("From", list(RATES.keys()), index=1)
    with col2:
        to_curr = st.selectbox("To", list(RATES.keys()), index=0)

    if st.button("Convert", key="convert_btn"):
        if from_curr == to_curr:
            result = amount
        else:
            result = convert_currency(amount, from_curr, to_curr)
        st.markdown(f"**{amount:.2f} {from_curr} ≈ {result:.2f} {to_curr}**")

# ---------- TAB 4: BMI ----------
with tabs[3]:
    st.markdown("<div class='section-label'>BMI Calculator</div>", unsafe_allow_html=True)
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
