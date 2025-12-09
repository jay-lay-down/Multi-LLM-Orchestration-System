Plaintext

# 🤖 Multi-LLM Debate Orchestrator

A multi-agent debate system that leverages the unique strengths of three SOTA (State-of-the-Art) models: **GPT-4o**, **Claude 3.5 Sonnet**, and **Gemini 1.5 Pro**.

Instead of relying on a single model, this project implements a **Model Orchestration** pattern, assigning specific "Personas" to the model best suited for that role to create a realistic simulation of a business meeting.

## 🚀 Key Features

- **Strategic Model Routing**:
  - **GPT-4o (OpenAI)**: Acts as the **Statistician**. Chosen for its superior logic, math capabilities, and strict adherence to instructions.
  - **Claude 3.5 Sonnet (Anthropic)**: Acts as the **Client**. Chosen for its human-like nuance, emotional intelligence, and natural tone.
  - **Gemini 1.5 Pro (Google)**: Acts as the **Project Manager**. Chosen for its large context window and creative problem-solving skills to mediate the debate.
- **Context Awareness**: Agents share a conversation history, allowing for dynamic rebuttals and continuity.
- **Extensible Design**: Easy to add more agents or switch model providers.
- **Secure Configuration**: Uses `.env` for API key management.

## 🛠️ Tech Stack

- **Python 3.8+**
- **OpenAI API**
- **Anthropic API**
- **Google Generative AI API**
- **python-dotenv**

## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/multi-llm-debate.git](https://github.com/YOUR_USERNAME/multi-llm-debate.git)
   cd multi-llm-debate
Install dependencies

Bash

pip install -r requirements.txt
Set up API Keys Create a .env file in the root directory and add your keys (Do not commit this file):

Ini, TOML

OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here
GEMINI_API_KEY=your_google_key_here
🏃‍♂️ Usage
Run the simulation script:

Bash

python main.py
📝 Example Output
[Topic]: Should we add an 'AI Chatbot' feature to our new product?

[Client - Claude 3.5]: "Look, I don't care about the tech. Will this actually increase our Q3 revenue, or is it just a gimmick?"

[Statistician - GPT-4o]: "Based on current market data, retention rates for generic chatbots are below 5%. Unless we have a specific use case, the ROI is statistically insignificant."

[PM - Gemini 1.5]: "I see valid points from both sides. How about we test a beta version focused only on customer support to minimize risk while tracking the revenue impact?"

📄 License
MIT
