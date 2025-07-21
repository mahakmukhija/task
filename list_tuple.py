import streamlit as st

st.set_page_config(page_title="Tuple vs List in Python", layout="centered")
st.title("📊 Technical Difference Between Tuple and List in Python")

st.markdown("Python provides both **lists** and **tuples** as sequence data types, but they differ in important ways.")

# Comparison Table
st.subheader("🔍 Comparison Table")

st.markdown("""
| Feature              | List (`[]`)                          | Tuple (`()`)                          |
|----------------------|--------------------------------------|---------------------------------------|
| **Mutability**       | ✅ Mutable (can change values)       | ❌ Immutable (cannot be changed)      |
| **Syntax**           | `my_list = [1, 2, 3]`               | `my_tuple = (1, 2, 3)`               |
| **Performance**      | Slower (more flexible)               | Faster (optimized for immutability)  |
| **Memory Usage**     | Uses more memory                     | Uses less memory                     |
| **Methods Available**| Many (`append()`, `remove()`, etc.)  | Few (`count()`, `index()`)           |
| **Use Case**         | Dynamic, changeable collections      | Fixed data, integrity assurance       |
""")

# Examples
st.subheader("🧪 Examples")

with st.expander("🔁 List Example"):
    st.code("""
my_list = [10, 20, 30]
my_list.append(40)
print(my_list)  # Output: [10, 20, 30, 40]
""")

with st.expander("🔒 Tuple Example"):
    st.code("""
my_tuple = (10, 20, 30)
my_tuple[0] = 100  # ❌ Error: 'tuple' object does not support item assignment
""")

# When to use which?
st.subheader("💡 When to Use What?")

st.markdown("""
- ✅ Use **List** when:
  - You need to **add, remove, or update** items.
  - Your data is **dynamic** or frequently changing.

- ✅ Use **Tuple** when:
  - You need to **ensure data integrity**.
  - The collection should remain **constant** or is used as a **dictionary key**.
""")

st.success("✅ Conclusion: Use Tuples for safety and performance, Lists for flexibility.")
