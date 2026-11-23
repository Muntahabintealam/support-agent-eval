# Support Agent with Evaluation Suite

A customer support agent for a fictional online shop, built with the Claude API.
It answers from a help centre knowledge base (retrieval), looks up orders and
creates tickets (tool calling), and escalates when it does not know.
An evaluation suite measures tool choice, grounding and safety so versions can be compared.

## Setup
    python -m venv .venv && source .venv/bin/activate
    pip install -r requirements.txt
    cp .env.example .env   # add your key, then: export ANTHROPIC_API_KEY=...
    python ingest.py
    python agent.py

## Evaluate
    python run_evals.py --label baseline

## Results
(Add a table here: version, change made, pass rate.)

## Limitations
(Add what the agent cannot do and which test cases still fail, and why.)
