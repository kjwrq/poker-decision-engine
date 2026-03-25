RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]
SUITS = ["♦", "♣", "♥", "♠"]
EMPTY = "--"

DECK = []
for r in RANKS:
    for s in SUITS:
        DECK += [r + s]

DECISIONS = ["Fold", "Call", "Raise"]

SYSTEM_PROMPT = (
    "You are a poker decision agent. "
    "You must choose exactly one action: Fold, Call, or Raise. "
    "Use the simulation probabilities AND table context (position, stack size, and number of opponents). "
    "Provide a breif explanation of your choice (2-3 sentences), along with a confidence score"
)

RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "decision": {"type": "string", "enum": DECISIONS},
        "reasoning": {"type": "string", "minLength": 1},
        "confidence": {"type": "number", "minimum": 0, "maximum": 1}
    },
    "required": ["decision", "reasoning", "confidence"]
}