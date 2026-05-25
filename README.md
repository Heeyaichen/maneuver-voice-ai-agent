# Talk to Founder Voice AI Agent for Maneuver

This project is a local web app for the Maneuver intern assignment. It lets a visitor have a real-time voice conversation with an AI version of the founder, capture discovery information during the call, and render synchronized frontend visuals as the conversation changes.

## What It Does

- Runs a natural discovery call for name, company, role, challenge, current tools, timeline, budget, and related notes.
- Answers questions about Maneuver services, process, pricing, team, and positioning from a local markdown knowledge base.
- Persists captured discovery data as JSON files under `agent/leads/`.
- Updates the frontend in real time through LiveKit RPC calls:
  - Live lead panel during discovery
  - Services slide
  - Five-step process diagram
  - Discovery summary at the end of the call
  - Agent listening, thinking, and speaking state

## Local Setup

Prerequisites:

- Python 3.10 or newer
- `uv`
- Node.js
- `pnpm`
- LiveKit Cloud project credentials
- OpenAI, Deepgram, and Cartesia API keys

Create environment files:

```bash
cp agent/.env.example agent/.env.local
cp frontend/.env.example frontend/.env.local
```

Set these values in `agent/.env.local`:

```env
LIVEKIT_URL=wss://your-livekit-project.livekit.cloud
LIVEKIT_API_KEY=your_livekit_api_key
LIVEKIT_API_SECRET=your_livekit_api_secret
OPENAI_API_KEY=your_openai_api_key
DEEPGRAM_API_KEY=your_deepgram_api_key
CARTESIA_API_KEY=your_cartesia_api_key
```

Set these values in `frontend/.env.local`:

```env
LIVEKIT_URL=wss://your-livekit-project.livekit.cloud
LIVEKIT_API_KEY=your_livekit_api_key
LIVEKIT_API_SECRET=your_livekit_api_secret
AGENT_NAME=maneuver-founder
```

Install and prepare the agent:

```bash
cd agent
uv sync
uv run python src/agent.py download-files
```

Install the frontend:

```bash
cd frontend
pnpm install
```

Run the app in two terminals.

Terminal 1:

```bash
cd agent
uv run python src/agent.py dev
```

Terminal 2:

```bash
cd frontend
pnpm dev
```

Open `http://localhost:3000`, start the call, allow microphone access, and speak with the agent.

## Models and Providers

- **LiveKit Agents Python SDK**: Handles the real-time voice agent session, room connection, audio pipeline, and RPC calls to the frontend.
- **OpenAI GPT-4o**: Used as the main LLM because it gives strong conversational quality, tool-calling reliability, and enough reasoning ability to switch naturally between discovery and Maneuver Q&A.
- **Deepgram nova-3**: Used for speech-to-text because it is low-latency, accurate, and supports multilingual speech recognition.
- **Cartesia sonic-3**: Used for text-to-speech because it gives fast, natural voice output suitable for a founder-style sales/discovery call.
- **Silero VAD and LiveKit multilingual turn detector**: Used for voice activity and turn detection so the agent can respond to natural pauses and interruptions.
- **LiveKit RPC**: Used to synchronize frontend visuals with backend tool calls as soon as relevant information is captured or a visual should appear.

## Demo Flow

A short demo can use this sequence:

1. "Hi, I'm Jenna, CTO at EMEA Corp."
2. "We're trying to automate customer support to improve response time."
3. "We currently use Zendesk with basic chatbots."
4. "Our timeline is three months and our budget is around twenty-five thousand dollars."
5. "What services does Maneuver offer?"
6. "What's your process for building AI systems?"
7. "Can you summarize what you captured and tell me the next steps?"

The expected result is that the lead panel updates live, the services slide appears, the process diagram appears, the discovery summary appears, and a JSON lead file is saved in `agent/leads/`.

## Verification

Frontend:

```bash
cd frontend
pnpm lint
pnpm build
```

Agent:

```bash
cd agent
uv run ruff format --check
uv run ruff check
```

## What I Would Build Next With Another Week

- Add a persistent transcript view next to the visual layer so reviewers can inspect the full conversation.
- Implement `show_service_detail(service_name)` for focused service-specific visuals.
- Add a founder/admin view for browsing past captured leads.
- Trigger a follow-up email or Slack notification when discovery ends.
- Add stronger automated tests for the Maneuver-specific agent tools, lead capture, and frontend RPC payload handling.
- Improve responsive polish for small screens and add production deployment instructions.
