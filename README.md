# 🎹 Rachmaninov Core

Standalone action-proposal and PDCA (Plan-Do-Check-Act) engine.  
"AI handles language; you handle the will."

This is a decoupled version of the Rachmaninov engine used in Aura and Praxis, designed to be used as a CLI tool or a library for agents like Hermes and OpenCode.

## 🚀 Key Features

- **Deterministic Ontology:** Maps life domains to the `ayu` action schema (FABRICATE, STUDY, CONSTRUCT, BOND, HEAL).
- **Contextual Planning:** Proposes high-impact actions based on your current goals and environment.
- **PDCA Loop:** Built-in grading and logging system to track performance and identify stagnant goals.
- **AI-Powered:** Uses `opencode` for high-quality, non-consensus proposal synthesis.

## 🛠️ Installation

```bash
cd rachmaninov
pip install -e .
```

## 📖 Usage

### 1. Plan your day
Propose actions based on a `goals.json` file:
```bash
rachmaninov plan --goals goals.json --context "Working from home, morning focus block."
```

### 2. Record an action
Log a completed task with a grade (0.0 to 1.0) and rationale:
```bash
rachmaninov act --goal-id "learn-rust" --text "Completed Chapter 3 of the Rust Book" --grade 0.8 --rationale "Focused well, but got distracted by coffee." --intellectual 0.8
```

## 📂 Data Schema

Rachmaninov uses the Praxis/Aura shared ontology:
- **Physical:** Health, fitness, rest.
- **Economic:** Wealth, financial security.
- **Intellectual:** Career, skills, gaming.
- **Psychological:** Mental balance, relationships, spirit.

---
Built for the sovereign individual.
