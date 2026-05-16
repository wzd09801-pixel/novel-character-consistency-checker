# Novel Character Consistency Checker

An AI Agent skill for checking character personality and action consistency in novel writing. Includes automatic detection and repair capabilities.

## Features

- 🔍 **Four-Step Analysis**: Environmental Info → Personality/Goals → Behavior Deduction → Consistency Check
- 🔧 **Auto-Repair Loop**: Automatically generate and apply fixes when inconsistencies are detected
- 📊 **Consistency Score**: Quantitative evaluation (0-100)
- 🔄 **Iterative Verification**: Re-verify after fixes

## Workflow

### Step 1: Confirm Environmental Information Reception
Identify what environmental information the character has received from the narrative.

### Step 2: Confirm Personality Traits, Past Experiences & Goals
Analyze the character's core traits, relevant experiences, and priorities based on received information.

### Step 3: Behavior Deduction
Predict behaviors consistent with the character's short-term goals.

### Step 4: Consistency Check
Verify if the deduced behavior aligns with the character setup across 4 dimensions:
- **Personality**: Does behavior conflict with core traits?
- **Experience**: Does it utilize relevant past experiences?
- **Goals**: Does it serve short-term objectives?
- **Logic**: Is it reasonable given available information?

## Auto-Repair Loop

When inconsistency is detected, three fix options are generated:

| Option | Type | Description |
|--------|------|-------------|
| **A** | Context Adjustment | Modify situation to justify original behavior (least invasive) |
| **B** | Motivation Injection | Add internal thoughts to justify behavior (moderate) |
| **C** | Behavior Replacement | Replace with character-consistent behavior (most invasive) |

## Consistency Score

| Score | Rating | Description |
|-------|--------|-------------|
| 90-100 | Excellent | Perfect consistency |
| 70-89 | Good | Minor adjustments possible |
| 50-69 | Attention | Needs review |
| <50 | Revision | Significant issues |

## File Structure

```
novel-character-consistency-checker/
├── SKILL.md              # Main skill definition
├── _meta.json            # Metadata (id, version)
├── scripts/
│   └── validate_skill.py # Validation script
└── references/           # Additional documentation
```

## Usage

This skill is designed for use with AI agents that support skill plugins. Import and invoke the skill when you need to verify character consistency in your novel writing.

## License

MIT
