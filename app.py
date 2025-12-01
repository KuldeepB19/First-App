import streamlit as st
import math

st.set_page_config(
    page_title="Multi Calculator",
    page_icon="🧮",
    layout="centered",
)

# -------------------- SESSION STATE --------------------
if "basic_expr" not in st.session_state:
    st.session_state.basic_expr = "0"
if "basic_last" not in st.session_state:
    st.session_state.basic_last = ""
if "history" not in st.session_state:
    st.session_state.history = []
if "sci_expr" not in st.session_state:
    st.session_state.sci_expr = ""
if "sci_result" not in st.session_state:
    st.session_state.sci_result = ""
if "theme" not in st.session_state:
    st.session_state.theme = "Dark"

# -------------------- SIDEBAR --------------------
st.sidebar.title("🧮 Multi Calculator")

# Theme toggle
theme_choice = st.sidebar.radio(
    "Theme",
    ["Dark", "Light"],
    index=0 if st.session_state.theme == "Dark" else 1,
)
st.session_state.theme = theme_choice

# History in sidebar
with st.sidebar.expander("History", expanded=False):
    if not st.session_state.history:
        st.write("No calculations yet.")
    else:
        for item in st.session_state.history:
            st.write(item)

# -------------------- THEME COLORS --------------------
if st.session_state.theme == "Dark":
    BG = "#0f172a"
    CARD_BG = "#020617"
    TEXT = "#e5e7eb"
    SUBTEXT = "#9ca3af"
    BORDER = "#1f2937"
    BUTTON_BG = "#111827"
    BUTTON_TEXT = "#e5e7eb"
else:  # Light
    BG = "#f3f4f6"
    CARD_BG = "#ffffff"
    TEXT = "#111827"
    SUBTEXT = "#6b7280"
    BORDER = "#d1d5db"
    BUTTON_BG = "#e5e7eb"
    BUTTON_TEXT = "#111827"

# -------------------- GLOBAL STYLING --------------------
st.markdown(
    f"""
    <style>
    .stApp {{
        background: {BG};
        color: {TEXT};
        font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }}
    .card {{
        padding: 1.5rem 1.5rem 1.2rem 1.5rem;
        border-radius: 1.2rem;
        background: {CARD_BG};
        border: 1px solid {BORDER};
        max-width: 520px;
        margin: 2rem auto;
        box-shadow: 0 18px 40px rgba(0,0,0,0.45);
    }}
    .title {{
        text-align: center;
        font-size: 1.6rem;
        font-weight: 600;
        margin-bottom: 0.2rem;
    }}
    .subtitle {{
        text-align: center;
        font-size: 0.85rem;
        color: {SUBTEXT};
        margin-bottom: 1.2rem;
    }}
    .display-main {{
        width: 100%;
        padding: 0.65rem 0.9rem;
        border-radius: 0.9rem;
        background: {CARD_BG};
        border: 1px solid {BORDER};
        font-size: 1.5rem;
        text-align: right;
        font-variant-numeric: tabular-nums;
        margin-bottom: 0.2rem;
        color: {TEXT};
    }}
    .display-sub {{
        width: 100%;
        font-size: 0.8rem;
        text-align: right;
        color: {SUBTEXT};
        min-height: 1rem;
        margin-bottom: 0.5rem;
    }}
    .section-label {{
        font-weight: 600;
        margin-bottom: 0.4rem;
    }}
    .stButton > button {{
        background: {BUTTON_BG};
        color: {BUTTON_TEXT};
        border-radius: 0.7rem;
        border: none;
        padding-top: 0.45rem;
        padding-bottom: 0.45rem;
        font-size: 1.05rem;
        font-weight: 500;
        transition: all 0.08s ease-out;
    }}
    .stButton > button:hover {{
        transform: translateY(-1px);
        box-shadow: 0 6px 16px rgba(0,0,0,0.35);
    }}
    .stButton > button:active {{
        transform: translateY(0);
        box-shadow: none;
        filter: brightness(0.95);
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# -------- Click sound (simple JS) --------
st.markdown(
    """
    <audio id="click-sound" src="https://actions.google.com/sounds/v1/cartoon/wood_plank_flicks.ogg"></audio>
    <script>
    const snd = document.getElementById("click-sound");
    if (snd) {{
        window.addEventListener("click", function(e) {{
            const tag = e.target.tagName;
            if (tag === "BUTTON") {{
                try {{
                    snd.currentTime = 0;
                    snd.play();
                }} catch(err) {{}}
            }}
        }}, true);
    }}
    </script>
    """,
    unsafe_allow_html=True,
)

# ---------------- BASIC CALCULATOR LOGIC ----------------
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
        add_history(exp, result)
        return

    # Append normal key
    if exp == "0" and key not in [".", "%"]:
        exp = ""
    st.session_state.basic_expr = exp + key


# Keyboard input callback
def keyboard_submit():
    expr = st.session_state.basic_text.strip()
    if expr == "":
        return
    st.session_state.basic_expr = expr
    result = safe_eval_basic(expr)
    st.session_state.basic_last = expr + " ="
    st.session_state.basic_expr = result
    add_history(expr, result)


# ---------------- SCIENTIFIC CALCULATOR ----------------
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


# ---------------- CURRENCY CONVERTER ----------------
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


# ---------------- BMI ----------------
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
    st.markdown("<div class='section-label'>Basic Calculator</div>", unsafe_allow_html=True)

    # Displays
    st.markdown(
        f"<div class='display-main'>{st.session_state.basic_expr}</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"<div class='display-sub'>{st.session_state.basic_last}</div>",
        unsafe_allow_html=True,
    )

    # Keyboard input
    st.text_input(
        "Keyboard: type 2+2 and press Enter",
        value="" if st.session_state.basic_expr == "0" else st.session_state.basic_expr,
        key="basic_text",
        on_change=keyboard_submit,
    )

    st.markdown("")

    # Button grid
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
    st.markdown("<div class='section-label'>Scientific Calculator</div>", unsafe_allow_html=True)
    st.caption("Examples: sin(pi/2) + log(10), sqrt(16), cos(pi)")

    st.session_state.sci_expr = st.text_input(
        "Expression",
        value=st.session_state.sci_expr,
        placeholder="Use sin, cos, tan, log, sqrt, pi, e, ...",
        key="sci_expr_input",
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

    if st.button("Calculate", key="sci_calc_btn"):
        st.session_state.sci_result = safe_eval_sci(st.session_state.sci_expr)

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

st.markdown(
    f"<p style='text-align:center; font-size:0.75rem; color:{SUBTEXT};'>Built with Streamlit • Theme: {st.session_state.theme}</p>",
    unsafe_allow_html=True,
)
