import streamlit as st
from google import genai


st.set_page_config(
    page_title="Smart MCQ Solver",
    page_icon="✦",
    layout="centered",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');

    :root {
        --ink: #e8eaf4;
        --muted: #9298ad;
        --line: rgba(179, 190, 255, .13);
        --violet: #9c83ff;
        --cyan: #66e4ed;
    }

    html, body, [data-testid="stAppViewContainer"] {
        background:
            radial-gradient(ellipse at 12% 9%, rgba(80, 57, 145, .28), transparent 34%),
            radial-gradient(ellipse at 90% 37%, rgba(29, 119, 139, .15), transparent 32%),
            linear-gradient(145deg, #090a10 0%, #10121c 48%, #090b12 100%);
        color: var(--ink);
        font-family: 'DM Sans', sans-serif;
    }
    [data-testid="stAppViewContainer"] {
        min-height: 100vh;
        overflow: hidden;
    }
    [data-testid="stAppViewContainer"]::before {
        content: "";
        position: fixed;
        inset: 0;
        pointer-events: none;
        z-index: 0;
        opacity: .14;
        background-image:
            linear-gradient(rgba(185, 190, 255, .08) 1px, transparent 1px),
            linear-gradient(90deg, rgba(185, 190, 255, .08) 1px, transparent 1px);
        background-size: 58px 58px;
        mask-image: linear-gradient(to bottom, black, transparent 75%);
    }
    [data-testid="stHeader"] { background: transparent; }
    [data-testid="stToolbar"], #MainMenu, footer { visibility: hidden; }
    [data-testid="stMainBlockContainer"] {
        max-width: 860px;
        padding-top: 3.2rem;
        padding-bottom: 4rem;
        position: relative;
        z-index: 1;
    }

    .brand {
        display: flex;
        align-items: center;
        gap: 14px;
        margin: 0 0 2.2rem;
    }
    .brand-mark {
        width: 46px;
        height: 46px;
        display: grid;
        place-items: center;
        border: 1px solid rgba(163, 143, 255, .42);
        border-radius: 15px;
        color: #d3c8ff;
        font-size: 23px;
        background: linear-gradient(145deg, rgba(151, 117, 255, .23), rgba(71, 203, 222, .08));
        box-shadow: 0 0 28px rgba(139, 112, 255, .18), inset 0 0 16px rgba(195, 175, 255, .08);
    }
    .brand-name {
        color: #f0efff;
        font: 600 15px 'Space Grotesk', sans-serif;
        letter-spacing: .01em;
    }
    .brand-caption {
        color: var(--muted);
        font-size: 12px;
        margin-top: 3px;
    }
    .hero { margin: 0 0 1.8rem; }
    .eyebrow {
        color: var(--cyan);
        text-transform: uppercase;
        font-size: 10px;
        letter-spacing: .19em;
        font-weight: 700;
        margin-bottom: 11px;
    }
    .hero h1 {
        color: #f1f0fa;
        font: 600 clamp(2.1rem, 6vw, 3.2rem)/1.08 'Space Grotesk', sans-serif;
        letter-spacing: -.055em;
        margin: 0;
    }
    .hero p {
        color: #a4a8ba;
        font-size: 15px;
        margin: 13px 0 0;
    }
    .status-pill {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        border: 1px solid var(--line);
        border-radius: 99px;
        background: rgba(20, 23, 35, .76);
        color: #b6bed0;
        font-size: 11px;
        padding: 8px 12px;
        margin: 0 0 1.2rem;
    }
    .status-dot {
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background: #71e6c1;
        box-shadow: 0 0 10px rgba(113, 230, 193, .8);
    }
    [data-testid="stChatMessage"] {
        border: 1px solid var(--line);
        border-radius: 18px;
        background: linear-gradient(145deg, rgba(25, 28, 42, .84), rgba(16, 18, 28, .9));
        padding: 1.05rem 1.15rem;
        box-shadow: 0 12px 40px rgba(0, 0, 0, .14);
        animation: rise-in .45s ease both;
    }
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
        border-color: rgba(145, 127, 255, .24);
    }
    [data-testid="stChatMessage"] p { color: #e3e5ef; }
    .composer-title {
        color: #eeedfa;
        font: 600 17px 'Space Grotesk', sans-serif;
        margin: 1rem 0 .25rem;
    }
    .composer-hint { color: var(--muted); font-size: 12px; margin-bottom: 1rem; }
    [data-testid="stForm"] {
        border: 1px solid rgba(172, 180, 236, .16);
        border-radius: 22px;
        padding: 1.3rem 1.35rem 1.15rem;
        background:
            linear-gradient(140deg, rgba(29, 32, 48, .9), rgba(16, 18, 28, .9));
        box-shadow: 0 18px 65px rgba(0, 0, 0, .26), 0 0 42px rgba(115, 93, 193, .07);
        position: relative;
        overflow: hidden;
    }
    [data-testid="stForm"]::before {
        content: "";
        position: absolute;
        height: 1px;
        left: 10%;
        right: 10%;
        top: 0;
        background: linear-gradient(90deg, transparent, rgba(133, 216, 241, .55), rgba(170, 140, 255, .65), transparent);
    }
    [data-testid="stWidgetLabel"] p {
        color: #bcc1d2;
        font-size: 12px;
        font-weight: 600;
    }
    [data-testid="stTextArea"] textarea, [data-testid="stTextInput"] input {
        color: #eff0fa;
        background: rgba(9, 11, 18, .66);
        border: 1px solid rgba(174, 181, 222, .16);
        border-radius: 12px;
        transition: border-color .2s ease, box-shadow .2s ease, background .2s ease;
    }
    [data-testid="stTextArea"] textarea:focus, [data-testid="stTextInput"] input:focus {
        border-color: rgba(145, 128, 255, .76);
        box-shadow: 0 0 0 3px rgba(145, 128, 255, .13), 0 0 22px rgba(95, 190, 224, .08);
        background: rgba(11, 13, 22, .92);
    }
    [data-testid="stTextInput"] input::placeholder,
    [data-testid="stTextArea"] textarea::placeholder { color: #747b91; }
    [data-testid="stFormSubmitButton"] button {
        width: 100%;
        min-height: 46px;
        color: #10111a;
        border: 0;
        border-radius: 12px;
        background: linear-gradient(100deg, #a895ff, #78dce7);
        font-weight: 700;
        box-shadow: 0 7px 25px rgba(130, 133, 255, .22);
        transition: transform .2s ease, box-shadow .2s ease, filter .2s ease;
    }
    [data-testid="stFormSubmitButton"] button:hover {
        color: #090b12;
        transform: translateY(-2px);
        filter: brightness(1.08);
        box-shadow: 0 10px 34px rgba(130, 170, 255, .34);
    }
    [data-testid="stAlert"] { border-radius: 12px; }
    hr { border-color: rgba(179, 190, 255, .1); }
    @keyframes rise-in {
        from { opacity: 0; transform: translateY(9px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @media (max-width: 640px) {
        [data-testid="stMainBlockContainer"] { padding: 1.5rem 1rem 3rem; }
        [data-testid="stForm"] { padding: 1rem; }
        .brand { margin-bottom: 1.7rem; }
    }
    @media (prefers-reduced-motion: reduce) {
        *, *::before, *::after { animation-duration: .01ms !important; transition-duration: .01ms !important; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="brand">
        <div class="brand-mark">✦</div>
        <div>
            <div class="brand-name">SMART MCQ SOLVER</div>
            <div class="brand-caption">A little clarity in the noise</div>
        </div>
    </div>
    <div class="hero">
        <div class="eyebrow">Your answer, found</div>
        <h1>Think it through.<br>Find the answer.</h1>
        <p>Drop in a question and its choices. I’ll help you find the strongest answer.</p>
    </div>
    <div class="status-pill"><span class="status-dot"></span> Solver ready</div>
    """,
    unsafe_allow_html=True,
)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

st.markdown('<div class="composer-title">Ask a question</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="composer-hint">Add your question and all five answer choices to get started.</div>',
    unsafe_allow_html=True,
)

with st.form("mcq_form", clear_on_submit=True):
    question = st.text_area(
        "Question",
        placeholder="Type or paste your question here...",
        height=110,
    )

    first_row = st.columns(2)
    options = {}
    for column, option in zip(first_row, ["A", "B"]):
        with column:
            options[option] = st.text_input(
                f"Option {option}",
                placeholder=f"Enter choice {option}",
            )

    second_row = st.columns(2)
    for column, option in zip(second_row, ["C", "D"]):
        with column:
            options[option] = st.text_input(
                f"Option {option}",
                placeholder=f"Enter choice {option}",
            )

    options["E"] = st.text_input("Option E", placeholder="Enter choice E")
    submitted = st.form_submit_button("✦  Find the answer")

if submitted:
    if not question.strip():
        st.warning("Please enter a question.")
    elif any(not value.strip() for value in options.values()):
        st.warning("Please enter all five options.")
    elif "GEMINI_API_KEY" not in st.secrets:
        st.error(
            "Gemini API key is not configured. In Streamlit Cloud, open your app's "
            "Settings → Secrets and add `GEMINI_API_KEY = \"your-api-key\"`, then "
            "save the settings and restart the app."
        )
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

Choose the single best answer.

Return ONLY in this exact format:
A

Do not give explanations.
"""

        try:
            client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
            with st.spinner("Thinking through the choices..."):
                response = client.models.generate_content(
                    model="gemini-3.5-flash",
                    contents=prompt,
                )

            result = (response.text or "").strip()
            answers = [
                item.strip()
                for item in result.split(",")
                if item.strip() in ["A", "B", "C", "D", "E"]
            ]
            answer = answers[0] if answers else None

            question_summary = "**Question**\n\n" + question.strip() + "\n\n"
            question_summary += "\n".join(
                f"- **{option}.** {options[option].strip()}"
                for option in ["A", "B", "C", "D", "E"]
            )
            st.session_state.messages.append(
                {"role": "user", "content": question_summary}
            )
            assistant_response = (
                f"**Answer: {answer}** — {options[answer].strip()}"
                if answer
                else "I couldn’t get a valid answer this time. Please try again."
            )
            st.session_state.messages.append(
                {"role": "assistant", "content": assistant_response}
            )
            st.rerun()
        except Exception as error:
            st.error(f"Couldn’t complete the prediction: {error}")
