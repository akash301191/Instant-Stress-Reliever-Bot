# Instant Stress Reliever Bot

Instant Stress Reliever Bot is a therapeutic Streamlit application designed to help users cope with stress and anxiety in the moment. Powered by [Agno](https://github.com/agno-agi/agno), OpenAI's GPT-4o, and Giphy, this bot uses cognitive reframing techniques to transform emotionally heavy reflections into comforting, supportive paragraphs—each paired with a carefully selected, emotionally safe (well, not so safe. we are still refining this aspect) GIF.

## Folder Structure

```
Instant-Stress-Reliever-Bot/
├── instant-stress-reliever-bot.py
├── README.md
└── requirements.txt
```

* **instant-stress-reliever-bot.py**: The main Streamlit application.
* **requirements.txt**: Required Python packages.
* **README.md**: This documentation file.

## Features

* **Stress Input & Tone Selection**
  Describe your stress or anxiety, choose the type (e.g. relationship, work, health), and pick a response tone (e.g. gentle, uplifting, calm).

* **AI-Powered Emotional Reframing**
  The Emotional Reframe Agent reads your entry and generates 5 distinct, cognitively reframed paragraphs using affirming language and therapeutic tone.

* **Emotionally Safe GIF Suggestions**
  The Visual Enricher Agent enhances each paragraph with a supportive, meme-free GIF using Giphy search. All visuals are sensitive to user distress and intended to soothe, not entertain.

* **Structured Markdown Output**
  The final output is a markdown-formatted support report with paragraphs and embedded calming visuals.

* **Download Option**
  Download your personalized emotional relief report as a `.md` file for future reflection or journaling.

* **Clean Streamlit UI**
  Designed for a focused and safe emotional experience using Streamlit’s wide layout and minimal distractions.


## Prerequisites

* Python 3.11 or higher
* An OpenAI API key ([Get one here](https://platform.openai.com/account/api-keys))
* A Giphy API key ([Get one here](https://developers.giphy.com/dashboard/))


## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/akash301191/Instant-Stress-Reliever-Bot.git
   cd Instant-Stress-Reliever-Bot
   ```

2. **(Optional) Create and activate a virtual environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate        # On macOS/Linux
   # or
   venv\Scripts\activate           # On Windows
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the app**:

   ```bash
   streamlit run instant-stress-reliever-bot.py
   ```

2. **In your browser**:

   * Add your OpenAI and Giphy API keys in the sidebar.
   * Describe what’s stressing you out.
   * Select your stress category and desired emotional tone.
   * Click **💆 Generate My Stress Relief Report**.
   * View and download your personalized AI-generated support response.

3. **Download Option**
   Use the **📥 Download Stress Report** button to save your report as a `.md` file.

## Code Overview

* **`render_stress_inputs()`**: Captures the user’s journal-style reflection and emotional preferences.
* **`render_sidebar()`**: Handles secure input and storage of API keys for OpenAI and Giphy.
* **`generate_stress_relief_report()`**:

  * Uses the Emotional Reframe Agent to generate CBT-style support paragraphs.
  * Enhances each with an emotionally sensitive GIF using the Visual Enricher Agent.
* **`main()`**: Manages layout, user interaction, report generation, and rendering.

## Contributions

Contributions are welcome! Feel free to fork the repo, suggest improvements, or open a pull request. Make sure your updates are thoughtful, emotionally aligned, and well-tested.
