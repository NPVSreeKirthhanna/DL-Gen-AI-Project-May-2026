import streamlit as st
from google import genai


st.set_page_config(page_title="Smart MCQ Solver")

st.title("Smart MCQ Solver")
st.write("Enter a question and the five answer choices.")


client = genai.Client(
    api_key=st.secrets["GEMINI_API_KEY"]
)


question = st.text_area("Question")

options = {}

for option in ["A", "B", "C", "D", "E"]:
    options[option] = st.text_input(f"Option {option}")


if st.button("Predict"):

    if not question.strip():
        st.warning("Please enter a question.")

    elif any(not value.strip() for value in options.values()):
        st.warning("Please enter all five options.")

    else:

        prompt = f"""
You are solving a multiple-choice question.

Question:
{question}

Options:
A. {options["A"]}
B. {options["B"]}
C. {options["C"]}
D. {options["D"]}
E. {options["E"]}

Choose the three best answers and rank them from most likely correct
to least likely correct.

Return ONLY in this exact format:
A, B, C

Do not give explanations.
"""

        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

            result = response.text.strip()

            ranked = [
                option.strip()
                for option in result.split(",")
                if option.strip() in ["A", "B", "C", "D", "E"]
            ]

            ranked = list(dict.fromkeys(ranked))

            if len(ranked) >= 3:

                st.subheader("Top 3 Predictions")

                for option in ranked[:3]:
                    st.write(
                        f"**{option}** — {options[option]}"
                    )

            else:
                st.error("Could not get valid predictions.")

        except Exception as e:
            st.error(f"Prediction failed: {e}")