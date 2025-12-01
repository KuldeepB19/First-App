import streamlit as st

st.set_page_config(page_title="Simple Calculator", page_icon="🧮")

st.title("🧮 Simple Calculator")

st.write("Enter two numbers and choose an operation:")

# Inputs
num1 = st.number_input("First number", value=0.0)
num2 = st.number_input("Second number", value=0.0)

operation = st.selectbox(
    "Operation",
    ("Add", "Subtract", "Multiply", "Divide")
)

if st.button("Calculate"):
    if operation == "Add":
        result = num1 + num2
    elif operation == "Subtract":
        result = num1 - num2
    elif operation == "Multiply":
        result = num1 * num2
    elif operation == "Divide":
        if num2 == 0:
            result = "❌ Cannot divide by zero"
        else:
            result = num1 / num2
    
    st.success(f"Result : {result}")
