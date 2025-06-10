import streamlit as st
from textwrap import dedent

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.giphy import GiphyTools

def render_sidebar():
    st.sidebar.title("🔐 API Configuration")
    st.sidebar.markdown("---")

    # OpenAI API Key input
    openai_api_key = st.sidebar.text_input(
        "OpenAI API Key",
        type="password",
        help="Don't have an API key? Get one [here](https://platform.openai.com/account/api-keys)."
    )
    if openai_api_key:
        st.session_state.openai_api_key = openai_api_key
        st.sidebar.success("✅ OpenAI API key updated!")

    # GiphyAPI Key input
    giphy_api_key = st.sidebar.text_input(
        "Giphy API Key",
        type="password",
        help="Don't have an API key? Get one [here](https://developers.giphy.com/dashboard/)."
    )
    if giphy_api_key:
        st.session_state.giphy_api_key = giphy_api_key
        st.sidebar.success("✅ Giphy API key updated!")

    st.sidebar.markdown("---")

def render_stress_inputs():
    st.markdown("---")

    st.subheader("📝 Describe What’s Bothering You")
    user_entry = st.text_area(
        "Write a short reflection, journal entry, or describe a situation that made you feel stressed or overwhelmed.",
        height=300,
        placeholder="e.g. I had a tough meeting today and felt like I couldn’t express myself clearly..."
    )

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("😣 Stress Category")
        stress_type = st.selectbox(
            "What type of stress are you currently facing?",
            [
                "Work or performance pressure",
                "Relationship or emotional conflict",
                "Health-related anxiety",
                "Decision fatigue or overwhelm",
                "Loneliness or isolation",
                "No specific category"
            ]
        )

    with col2:
        st.subheader("🎧 Response Tone")
        response_tone = st.selectbox(
            "What tone would feel most helpful right now?",
            [
                "Gentle and reassuring",
                "Encouraging and uplifting",
                "Soothing and calm",
                "Neutral and grounding"
            ]
        )

    return {
        "user_entry": user_entry,
        "stress_type": stress_type,
        "response_tone": response_tone
    }

def generate_stress_relief_report(user_stress_inputs):
    user_entry = user_stress_inputs["user_entry"]
    stress_type = user_stress_inputs["stress_type"]
    response_tone = user_stress_inputs["response_tone"]

    # Agent 1: Emotional Reframe Agent
    reframer_agent = Agent(
        model=OpenAIChat(id="gpt-4o", api_key=st.session_state.openai_api_key),
        name="Emotional Reframe Agent",
        role="Helps users mentally reframe stressful experiences using CBT principles and affirming language.",
        description=dedent(f"""
            You are a stress relief assistant. Your task is to take a user's journal-style entry about a stressful experience
            and break it into 5 separate, cognitively reframed response paragraphs. These should:
            - Reflect empathy and understanding of the user’s situation (specifically related to "{stress_type}")
            - Use gentle, positive, and supportive phrasing
            - Offer emotional reframing, new perspectives, or affirmations
            - Write in a tone that feels {response_tone}
            Just return 5 distinct, supportive paragraphs in markdown format.
        """),
        instructions=[
            "Break your response into exactly 5 paragraphs.",
            "Each paragraph should address one emotional concern or theme from the user's entry.",
            f"Maintain a consistent tone that is {response_tone} throughout the response.",
            f"Adapt your support and reframing to match the stress type: '{stress_type}'.",
            "Avoid generic advice—tailor your wording to reflect the user’s emotional context.",
        ],
        markdown=True
    )

    reframe_prompt = f"""
    User Input:
    {user_entry}

    Stress Category: {stress_type}
    Response Tone: {response_tone}

    Break this into cognitively supportive and emotionally helpful paragraphs.
    """

    reframe_response = reframer_agent.run(reframe_prompt).content

    # Split into list of paragraphs
    paragraphs = [para.strip() for para in reframe_response.strip().split("\n\n") if para.strip()][:5]

    # Agent 2: GIF Enricher Agent
    enricher_agent = Agent(
        model=OpenAIChat(id="gpt-4o", api_key=st.session_state.openai_api_key),
        name="Visual Enricher Agent",
        tools=[GiphyTools(api_key=st.session_state.giphy_api_key, limit=5)],
        description=dedent("""
            You are a visual enrichment assistant for a mental wellness application. Your task is to take a supportive paragraph and its emotional tone,
            then generate a relevant, emotionally safe Giphy search query, and return the most appropriate GIF URL to complement the paragraph.

            This application helps users experiencing anxiety, sadness, or emotional distress. Your output must reflect compassion and sensitivity.
        """),
        instructions=[
            "Carefully read the support paragraph and identify its emotional tone or core supportive message.",
            "Create a short Giphy search query (under 10 words) that emphasizes calm, support, or care.",
            "Only use search themes that yield emotionally appropriate, consoling GIFs. Examples include:",
            "- comforting hug",
            "- someone listening quietly",
            "- motivational quote with soft background",
            "- soothing gesture",
            "- gentle nod or smile",
            "- nature calmness",
            "- affirmation text",
            "Avoid: memes, jokes, sarcasm, celebrities, dramatic reactions, or pop-culture humor.",
            "Use the `search_gifs` tool to search based on your query.",
            "Choose the most relevant and emotionally safe result that matches the paragraph’s supportive intent.",
            "Return ONLY the direct URL of the selected GIF. No extra text, commentary, or tags.",
        ],
        show_tool_calls=True,
    )

    # Append GIFs to each paragraph
    final_paragraphs = []
    for para in paragraphs:
        gif_prompt = f"""
        Paragraph: {para}
        Tone: {response_tone}

        Generate a relevant GIF for the paragraph and return only the URL.
        """
        gif_url = enricher_agent.run(gif_prompt).content.strip()
        para_with_gif = f"{para}\n\n![gif]({gif_url})"
        final_paragraphs.append(para_with_gif)

    # Join all into one markdown-formatted report
    final_report = "\n\n".join(final_paragraphs)

    return final_report


def main() -> None:
    # Page config
    st.set_page_config(page_title="Instant Stress Reliever Bot", page_icon="🌿", layout="wide")

    # Custom styling
    st.markdown(
        """
        <style>
        .block-container {
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }
        div[data-testid="stTextInput"] {
            max-width: 1200px;
            margin-left: auto;
            margin-right: auto;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Header and intro
    st.markdown("<h1 style='font-size: 2.5rem;'>🌿 Instant Stress Reliever Bot</h1>", unsafe_allow_html=True)
    st.markdown(
        "Welcome to Instant Stress Reliever Bot — a therapeutic Streamlit companion that interprets your mood, applies cognitive reframing, and delivers uplifting responses with soothing visuals to ease anxiety and restore emotional balance.",
        unsafe_allow_html=True
    )

    render_sidebar()
    user_stress_inputs = render_stress_inputs()

    st.markdown("---")

    if st.button("💆 Generate My Stress Relief Report"):
        if not hasattr(st.session_state, "openai_api_key"):
            st.error("Please provide your OpenAI API key in the sidebar.")
        elif not hasattr(st.session_state, "giphy_api_key"):
            st.error("Please provide your Giphy API key in the sidebar.")
        else:
            with st.spinner("Crafting your personalized emotional support..."):
                report = generate_stress_relief_report(user_stress_inputs)
                st.session_state.stress_report = report

    if "stress_report" in st.session_state:
        st.markdown(st.session_state.stress_report, unsafe_allow_html=True)

        st.download_button(
            label="📥 Download Stress Report",
            data=st.session_state.stress_report,
            file_name="stress_relief_report.md",
            mime="text/markdown"
        )


if __name__ == "__main__":
    main() 