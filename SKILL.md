---
name: novel-character-consistency-checker
description: Checks character personality and action consistency in novel writing. Used when users need to verify if characters' reactions and behaviors align with their established traits in specific situations.
---

# Novel Character Consistency Checker

## Core Workflow

For **each character** in a scene, perform the following four-step analysis:

### Step 1: Confirm Environmental Information Reception

**Objective**: Identify what environmental information the character has received from the narrative

Analysis Points:
- What the character **actually sees/hears** (perceived information)
- What the character **misunderstands** (if narrative hints at this)
- What information the character **lacks but other characters have** (information gap)
- The character's **perception limitations** (e.g., distance, attention blind spots)

**Output Format**:
```
【Character X's Environmental Information Reception】
- Received information: [list]
- Unreceived information: [list]
- Potential misunderstandings: [list]
```

### Step 2: Confirm Personality Traits, Past Experiences & Goals

**Objective**: Based on environmental information and received information, determine the character's priorities at this moment

Analysis Points:
- **Core personality traits**: The 3-5 traits most relevant to this situation
- **Past experiences**: Memories related to the current situation (trauma, achievements, lessons)
- **Short-term goals**: The character's specific goals for the next few minutes to hours
- **Long-term goals**: The character's overall life pursuits/values
- **Weight adjustment**: According to Step 1 info, more relevant information gets higher weight

**Weight Priority Rules**:
- Experiences directly related to current situation > general personality traits
- Urgent short-term goals > vague long-term goals
- Strong emotional triggers > rational long-term planning

**Output Format**:
```
【Character X's Personality & Goals Analysis】
- Core traits (ordered by relevance): [trait1, trait2...]
- Relevant past experiences: [list]
- Short-term goals (current priority): [goal1 > goal2 > goal3]
- Long-term goals: [list]
```

### Step 3: Behavior Deduction

**Objective**: Based on the first two steps, predict behaviors consistent with the character's short-term goals

Deduction Rules:
- Behavior must **serve short-term goals**
- Behavior must **align with character traits**
- Behavior can **break conventions**, but must have personality support
- Behavior should consider **information limitations** (not omniscient perspective)

**Output Format**:
```
【Character X's Behavior Deduction】
- Predicted behavior: [describe behavior]
- Behavior motivation: [explain why this behavior serves goals]
- Behavior risks: [anticipate possible consequences]
- Alternative plans: [if main behavior is blocked, what's the character's second choice]
```

### Step 4: Consistency Check

**Objective**: Verify if the deduced behavior truly aligns with the character setup

Check Dimensions:
1. **Personality consistency**: Does the behavior conflict with core traits?
2. **Experience consistency**: Does it utilize or avoid relevant past experiences?
3. **Goal consistency**: Does the behavior truly serve short-term goals?
4. **Logic consistency**: Is this behavior reasonable given the available information?

**Judgment Results**:
- ✅ **Consistent**: Behavior matches character setup
- ⚠️ **Needs explanation**: Behavior has deviations but can have reasonable justification
- ❌ **Inconsistent**: Behavior has fundamental contradiction with character setup

**Output Format**:
```
【Character X's Consistency Check】
- Personality consistency: [✅/⚠️/❌] + reason
- Experience consistency: [✅/⚠️/❌] + reason
- Goal consistency: [✅/⚠️/❌] + reason
- Logic consistency: [✅/⚠️/❌] + reason
- Overall judgment: [✅ Consistent / ⚠️ Needs explanation / ❌ Inconsistent]
```

---

## Auto-Repair Loop (When Inconsistencies Detected)

When ❌ **Inconsistent** is detected, automatically execute the following loop:

### Loop Phase 1: Generate Fix Options

For each inconsistency, generate 3 alternative fixes ranked by preservation of author intent:

**Fix Option A: Context Adjustment** (Least invasive)
- Modify the situation/environment to make the original behavior reasonable
- Preserve: original dialogue, character actions, emotional beats
- Change: situational details, external factors

**Fix Option B: Motivation Injection** (Moderate)
- Add internal thoughts or subtle cues to justify the behavior
- Preserve: original behavior, scene structure
- Change: add parenthetical thoughts, adjust adjacent actions

**Fix Option C: Behavior Replacement** (Most invasive)
- Replace the inconsistent behavior with a behavior that fits the character
- Preserve: scene goals, emotional arc
- Change: specific actions, dialogue choices

### Loop Phase 2: Apply Fix

If user approves auto-fix OR `auto_fix: true` was set:
- Apply the highest-ranked acceptable fix
- Generate the modified passage
- Automatically re-run Steps 1-4 on the modified version

### Loop Phase 3: Verification

Re-check the modified passage:
- If ✅ **Consistent**: End loop, output "Fixed successfully"
- If still ⚠️/❌: Generate next fix option, repeat Phase 1-2

**Maximum iterations**: 3 (after 3 failed attempts, halt and report the persistent inconsistency)

---

## Consistency Score Calculation

After each check, calculate a **Consistency Score** (0-100):

```
Score = (Personality_Weight × Personality_Result) +
        (Experience_Weight × Experience_Result) +
        (Goal_Weight × Goal_Result) +
        (Logic_Weight × Logic_Result)
```

Where:
- `Result`: ✅ = 1.0, ⚠️ = 0.5, ❌ = 0.0
- `Weight`: Each dimension defaults to 0.25, but can be adjusted by user priority

**Score Thresholds**:
- 90-100: Excellent consistency
- 70-89: Good, minor adjustments possible
- 50-69: Needs attention
- Below 50: Significant revision required

---

## Input Format

When users provide novel excerpts, should include:
1. **Scene description**: Current plot background
2. **Character list**: All characters to check
3. **Character setup** (ask if not provided): personality traits, past experiences, goals
4. **Creative excerpt**: Text to be checked
5. **Optional flags**:
   - `auto_fix: true` - Automatically apply fixes (default: false)
   - `priority_weights: {personality, experience, goal, logic}` - Custom dimension weights

---

## Output Format

### Standard Output (No Fix Required)
```
Final report includes:
1. Four-step analysis for each character
2. Consistency check results summary table
3. Conflict points list (if any)
4. Consistency Score
```

### With Auto-Repair Enabled
```
Final report includes:
1. Original four-step analysis
2. Detected inconsistencies with severity
3. Generated fix options (A/B/C ranked)
4. Applied fix (if approved or auto_fix: true)
5. Post-fix verification results
6. Final Consistency Score (before → after)
```

---

## Usage Scenarios

- Check character reactions after writing a dialogue
- Verify behavior logic after completing a scene
- Ensure style consistency in multi-author collaboration
- Reference when facing challenges in character development
- **Auto-repair**: When you want the skill to not only detect but also suggest/apply fixes
