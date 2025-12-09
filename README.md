# 🤖 Multi-LLM Debate Orchestrator

A small demo that orchestrates a multi-agent debate using three state-of-the-art language models—**GPT-4o**, **Claude 3.5 Sonnet**, and **Gemini 1.5 Pro**. Each model is assigned a persona that mirrors its strengths to simulate a realistic business meeting.

## 🚀 Key Features
- **Strategic model routing:**
  - **GPT-4o (OpenAI)** as the **Statistician** for logic and math-heavy responses.
  - **Claude 3.5 Sonnet (Anthropic)** as the **Client** for human-like nuance and emotional tone.
  - **Gemini 1.5 Pro (Google)** as the **Project Manager** for mediation and creative solutions.
- **Context awareness:** Agents share a conversation history to enable dynamic rebuttals and continuity.
- **Extensible design:** Add more agents or swap model providers with minimal changes.
- **Secure configuration:** Keep API keys outside of source control via environment variables.

## 🛠️ Requirements
- Python **3.8+**
- Access to the OpenAI, Anthropic, and Google Generative AI APIs

## 📦 Setup
1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/multi-llm-debate.git
   cd multi-llm-debate
   ```
2. **(Recommended) Create a virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
4. **Configure API keys**
   Create a `.env` file (or export environment variables) with your credentials. These names match the variables used in `app.py`:
   ```env
   OPENAI_API_KEY=your_openai_key_here
   CLAUDE_API_KEY=your_anthropic_key_here
   GEMINI_API_KEY=your_google_key_here
   ```
   > Tip: Avoid committing your API keys. If you use a `.env` file, run `export $(cat .env | xargs)` before starting the app.

## 🏃‍♂️ Usage
Run the debate simulation script:
```bash
python app.py
```
The default topic at the bottom of `app.py` is:
```
run_debate("우리 회사 신제품에 'AI 챗봇' 기능을 넣어야 할까?")
```
Update that line to explore different discussion prompts.

## 📝 Example Output
```
[Topic]: Should we add an "AI Chatbot" feature to our new product?
[Client - Claude 3.5]: "Look, I don't care about the tech. Will this actually increase our Q3 revenue, or is it just a gimmick?"
[Statistician - GPT-4o]: "Based on current market data, retention rates for generic chatbots are below 5%. Unless we have a specific use case, the ROI is statistically insignificant."
[PM - Gemini 1.5]: "I see valid points from both sides. How about we test a beta version focused only on customer support to minimize risk while tracking the revenue impact?"
```

## 📄 License
The project is released under the [Apache License 2.0](LICENSE).
