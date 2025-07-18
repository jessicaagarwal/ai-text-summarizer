import os
import textwrap
import streamlit as st
from dotenv import load_dotenv
from groq import Groq
from PyPDF2 import PdfReader


load_dotenv()
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    st.error("❌ Missing GROQ_API_KEY. Add to .env or Streamlit Secrets.")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)

st.set_page_config(page_title="AI Text Summarizer", page_icon="📝")
st.title("📝 AI Text Summarizer")

st.write("Paste text below and choose summary length. Model: `llama-3.3-70b-versatile`.")

st.sidebar.header("⚙️ Settings")

length_choice = st.sidebar.radio(
    "Summary Length",
    ["Short", "Medium", "Detailed"],
    index=0,
    help="Controls how much detail appears in the summary."
)

tone_choice = st.sidebar.selectbox(
    "Tone",
    ["Neutral", "Simple", "Professional", "Casual", "Kid-friendly"],
    index=0
)

format_choice = st.sidebar.selectbox(
    "Output Format",
    ["Bullets", "Paragraph", "Bullets + Paragraph", "TL;DR"],
    index=0
)

temperature = st.sidebar.slider("Creativity (temperature)", 0.0, 1.0, 0.4)

def build_length_instruction(length: str) -> str:
    if length == "Short":
        return "Give a very short summary in 3 bullet points. Max ~40 words total."
    if length == "Medium":
        return "Give 5 concise bullet points followed by a short paragraph (~100 words)."
    return "Give a detailed summary: key bullet points, a short paragraph (~150 words), and a 1-line takeaway."

def build_tone_instruction(tone: str) -> str:
    mapping = {
        "Neutral": "Use a neutral, informative tone.",
        "Simple": "Use plain language, easy to understand.",
        "Professional": "Use clear, professional language suitable for a report.",
        "Casual": "Use a friendly, conversational tone.",
        "Kid-friendly": "Explain in very simple words, like to a 10-year-old.",
    }
    return mapping.get(tone, "Use a neutral tone.")

def build_format_instruction(fmt: str) -> str:
    mapping = {
        "Bullets": "Output bullet points only.",
        "Paragraph": "Output one short paragraph only.",
        "Bullets + Paragraph": "Start with bullet points, then a short paragraph.",
        "TL;DR": "Output a single TL;DR line.",
    }
    return mapping.get(fmt, "Output bullet points only.")

def truncate_text(txt: str, max_chars: int = 8000) -> str:
    """Prevent overly long payloads. Trim and warn."""
    if len(txt) <= max_chars:
        return txt
    st.warning(f"Input truncated to {max_chars} characters to fit model context.")
    return txt[:max_chars]

def count_words_tokens(text: str) -> tuple[int, int]:
    """Estimate words and tokens for user text."""
    words = len(text.split())
    # Rough token estimate: 1 token ≈ 0.75 words for English text
    tokens = int(words / 0.75)
    return words, tokens

# --- Input Source: upload OR paste ---------------------------------------------------
uploaded_file = st.file_uploader(
    "Or upload a text/PDF file",
    type=["txt", "pdf"],
    help="Upload a .txt or .pdf; we’ll extract the text for you."
)

file_text = ""
if uploaded_file is not None:
    if uploaded_file.type == "text/plain":
        file_text = uploaded_file.read().decode("utf-8", errors="ignore")
    elif uploaded_file.type == "application/pdf":
        try:
            reader = PdfReader(uploaded_file)
            extracted_pages = []
            for page in reader.pages:
                extracted_pages.append(page.extract_text() or "")
            file_text = "\n".join(extracted_pages).strip()
        except Exception as e:
            st.error(f"Could not read PDF: {e}")

# Always show text area (pre-filled if file uploaded)
user_text = st.text_area(
    "Paste text to summarize (or upload a file above):",
    value=file_text if file_text else "",
    height=300,
    placeholder="Paste an article, blog, report, or notes here..."
)
# Show word/token count live
if user_text.strip():
    words, tokens = count_words_tokens(user_text)
    st.caption(f"📊 **Word Count:** {words} | **Estimated Tokens:** {tokens}")


summarize_clicked = st.button("Summarize")

if summarize_clicked:
    clean_text = user_text.strip()
    if not clean_text:
        st.error("Please paste some text to summarize.")
        st.stop()

    # Build instructions
    length_instr = build_length_instruction(length_choice)
    tone_instr = build_tone_instruction(tone_choice)
    format_instr = build_format_instruction(format_choice)

    # Final prompt
    prompt = textwrap.dedent(f"""
    You are a helpful summarization assistant.
    {length_instr}
    {tone_instr}
    {format_instr}

    Text to summarize:
    {truncate_text(clean_text)}
    """).strip()

    with st.spinner("Summarizing..."):
        resp = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            temperature=temperature,
            messages=[
                {"role": "system", "content": "You summarize text accurately and follow formatting instructions exactly."},
                {"role": "user", "content": prompt},
            ],
        )
        summary = resp.choices[0].message.content or "[No response]"

    st.subheader("📘 Summary")
    st.markdown(summary)

    # Download button for summary
    st.download_button(
        label="📥 Download Summary",
        data=summary,
        file_name="summary.txt",
        mime="text/plain"
    )

    # # Show raw prompt (debug toggle)
    # with st.expander("See Prompt Sent to Model"):
    #     st.code(prompt)

    # Usage metadata (if available)
    usage = getattr(resp, "usage", None)
    if usage:
        st.caption(f"Tokens → prompt: {usage.prompt_tokens}, completion: {usage.completion_tokens}, total: {usage.total_tokens}")
