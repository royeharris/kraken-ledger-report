# Accessing Previous Conversation History

If you have exceeded your model quota or changed models and need to access context from previous discussions, follow these methods:

## 1. Local Conversation Logs (The "Brain")
All interactions are stored locally on your machine.
- **Location:** `/Users/royeharris/.gemini/antigravity/brain/`
- **How to use:** Navigate to this directory in your file explorer. Each subfolder (named with a unique ID) represents a conversation. Inside, you'll find `.md` or `.txt` files containing the full dialogue history.
- **Model Compatibility:** All models (Gemini, GPT, Opus) share this same local backend. Swapping models mid-conversation or across sessions does not split the history; it remains unified within the corresponding conversation folder.

## 2. AI Summaries
The AI assistant maintains summaries of the most recent conversations. Even if a specific chat is "closed" or the model is different, the agent can see a list of recent conversation titles and summaries to help it regain context.

## 3. Knowledge Items (KIs)
Strategic project information is distilled into Knowledge Items.
- **Location:** `/Users/royeharris/.gemini/antigravity/knowledge/`
- **Purpose:** These act as long-term memory for specific modules or logic (e.g., "Bank Label Normalization Rules"). They persist across all sessions and model changes.

## 4. Workspaces & Artifacts
Key technical decisions are often recorded in `implementation_plan.md` or `walkthrough.md` artifacts within the specific conversation's brain folder. You can also find them if they were moved to the project's `docs/` folder.
