#!/usr/bin/env python3
"""
tags.py — Practice slot and type tags for all 110 drills.
Add one line per new drill. No layout or diagram logic.

Slots:  "Opener" | "Skill Block" | "Closer"
Types:  "Individual Skill" | "Team Comm." | "Competitive Reps" | "Decision Making"
"""

DRILL_TAGS = {
    # INFIELD
    1:  ("Opener",      "Skill Block",  "Individual Skill",  None),
    2:  ("Opener",      "Skill Block",  "Individual Skill",  "Competitive Reps"),
    14: ("Skill Block", None,           "Team Comm.",        None),
    21: ("Closer",      None,           "Competitive Reps",  "Individual Skill"),
    24: ("Opener",      "Skill Block",  "Competitive Reps",  "Individual Skill"),
    25: ("Closer",      None,           "Competitive Reps",  "Individual Skill"),
    26: ("Skill Block", "Closer",       "Individual Skill",  "Competitive Reps"),
    32: ("Closer",      None,           "Competitive Reps",  "Individual Skill"),
    64: ("Opener",      "Skill Block",  "Individual Skill",  None),
    65: ("Opener",      "Skill Block",  "Individual Skill",  None),
    66: ("Opener",      "Skill Block",  "Individual Skill",  None),
    67: ("Opener",      "Skill Block",  "Individual Skill",  None),
    68: ("Opener",      "Skill Block",  "Individual Skill",  None),
    69: ("Opener",      "Skill Block",  "Individual Skill",  None),
    # OUTFIELD
    5:  ("Opener",      "Skill Block",  "Individual Skill",  None),
    6:  ("Closer",      None,           "Competitive Reps",  "Decision Making"),
    10: ("Opener",      None,           "Individual Skill",  None),
    16: ("Skill Block", None,           "Team Comm.",        None),
    19: ("Opener",      None,           "Individual Skill",  "Competitive Reps"),
    23: ("Opener",      "Skill Block",  "Competitive Reps",  "Individual Skill"),
    43: ("Skill Block", None,           "Team Comm.",        "Decision Making"),
    44: ("Skill Block", None,           "Decision Making",   "Team Comm."),
    55: ("Opener",      "Skill Block",  "Individual Skill",  None),
    56: ("Skill Block", None,           "Individual Skill",  None),
    57: ("Skill Block", None,           "Individual Skill",  None),
    58: ("Skill Block", None,           "Individual Skill",  None),
    59: ("Opener",      "Skill Block",  "Individual Skill",  None),
    60: ("Closer",      None,           "Competitive Reps",  "Individual Skill"),
    61: ("Closer",      None,           "Competitive Reps",  "Individual Skill"),
    62: ("Skill Block", None,           "Individual Skill",  None),
    63: ("Opener",      None,           "Individual Skill",  None),
    # THROWING
    3:  ("Opener",      "Skill Block",  "Team Comm.",        "Competitive Reps"),
    4:  ("Closer",      None,           "Competitive Reps",  None),
    9:  ("Opener",      "Skill Block",  "Individual Skill",  None),
    15: ("Closer",      None,           "Competitive Reps",  "Individual Skill"),
    22: ("Closer",      None,           "Competitive Reps",  "Team Comm."),
    31: ("Closer",      None,           "Competitive Reps",  "Team Comm."),
    45: ("Opener",      None,           "Individual Skill",  "Competitive Reps"),
    46: ("Opener",      "Skill Block",  "Competitive Reps",  "Individual Skill"),
    54: ("Opener",      "Closer",       "Team Comm.",        "Competitive Reps"),
    70: ("Opener",      None,           "Individual Skill",  None),
    71: ("Opener",      "Skill Block",  "Individual Skill",  None),
    72: ("Opener",      "Skill Block",  "Individual Skill",  None),
    73: ("Opener",      "Skill Block",  "Individual Skill",  None),
    # SITUATIONAL
    7:  ("Skill Block", "Closer",       "Team Comm.",        "Decision Making"),
    8:  ("Skill Block", None,           "Individual Skill",  "Team Comm."),
    11: ("Skill Block", "Closer",       "Team Comm.",        "Competitive Reps"),
    18: ("Skill Block", None,           "Team Comm.",        "Decision Making"),
    20: ("Skill Block", None,           "Decision Making",   "Team Comm."),
    29: ("Closer",      None,           "Competitive Reps",  "Team Comm."),
    30: ("Skill Block", "Closer",       "Team Comm.",        "Competitive Reps"),
    33: ("Skill Block", None,           "Team Comm.",        "Decision Making"),
    34: ("Skill Block", "Closer",       "Decision Making",   "Team Comm."),
    37: ("Skill Block", None,           "Team Comm.",        "Decision Making"),
    38: ("Skill Block", None,           "Decision Making",   "Team Comm."),
    39: ("Skill Block", "Closer",       "Team Comm.",        "Competitive Reps"),
    42: ("Closer",      None,           "Decision Making",   "Team Comm."),
    47: ("Skill Block", "Closer",       "Decision Making",   "Competitive Reps"),
    48: ("Skill Block", None,           "Team Comm.",        "Decision Making"),
    49: ("Skill Block", None,           "Team Comm.",        "Individual Skill"),
    53: ("Skill Block", None,           "Decision Making",   "Team Comm."),
    74: ("Opener",      "Closer",       "Team Comm.",        "Competitive Reps"),
    75: ("Skill Block", None,           "Team Comm.",        "Decision Making"),
    76: ("Skill Block", None,           "Team Comm.",        "Decision Making"),
    77: ("Skill Block", None,           "Team Comm.",        "Decision Making"),
    78: ("Skill Block", None,           "Team Comm.",        "Decision Making"),
    # BASERUNNING
    12: ("Closer",      None,           "Competitive Reps",  "Decision Making"),
    13: ("Opener",      "Skill Block",  "Individual Skill",  None),
    27: ("Closer",      None,           "Competitive Reps",  "Individual Skill"),
    28: ("Closer",      "Skill Block",  "Competitive Reps",  "Decision Making"),
    35: ("Skill Block", "Closer",       "Decision Making",   "Competitive Reps"),
    36: ("Skill Block", "Closer",       "Decision Making",   "Competitive Reps"),
    50: ("Skill Block", "Closer",       "Decision Making",   "Competitive Reps"),
    51: ("Skill Block", "Closer",       "Decision Making",   "Competitive Reps"),
    79: ("Opener",      None,           "Individual Skill",  None),
    80: ("Opener",      "Skill Block",  "Individual Skill",  None),
    81: ("Opener",      "Skill Block",  "Individual Skill",  None),
    82: ("Opener",      "Skill Block",  "Individual Skill",  None),
    83: ("Skill Block", "Closer",       "Decision Making",   "Competitive Reps"),
    84: ("Skill Block", None,           "Individual Skill",  None),
    # HITTING
    17: ("Opener",      "Skill Block",  "Individual Skill",  None),
    40: ("Skill Block", "Closer",       "Individual Skill",  "Competitive Reps"),
    41: ("Skill Block", None,           "Decision Making",   "Individual Skill"),
    52: ("Skill Block", "Closer",       "Competitive Reps",  "Decision Making"),
    85: ("Opener",      "Skill Block",  "Individual Skill",  None),
    86: ("Opener",      "Skill Block",  "Individual Skill",  None),
    87: ("Skill Block", None,           "Individual Skill",  None),
    88: ("Skill Block", None,           "Individual Skill",  "Decision Making"),
    89: ("Skill Block", None,           "Individual Skill",  None),
    90: ("Closer",      None,           "Competitive Reps",  "Individual Skill"),
    91: ("Skill Block", None,           "Individual Skill",  "Decision Making"),
    # CATCHING
    92: ("Opener",      "Skill Block",  "Individual Skill",  None),
    93: ("Opener",      "Skill Block",  "Individual Skill",  None),
    94: ("Opener",      "Skill Block",  "Individual Skill",  None),
    95: ("Opener",      "Skill Block",  "Individual Skill",  None),
    96: ("Skill Block", None,           "Individual Skill",  "Team Comm."),
    97: ("Skill Block", None,           "Individual Skill",  None),
    98: ("Skill Block", None,           "Team Comm.",        "Decision Making"),
    # PITCHING
    99:  ("Opener",     "Skill Block",  "Individual Skill",  None),
    100: ("Opener",     "Skill Block",  "Individual Skill",  None),
    101: ("Opener",     "Skill Block",  "Individual Skill",  None),
    102: ("Opener",     "Skill Block",  "Individual Skill",  None),
    103: ("Skill Block",None,           "Individual Skill",  None),
    104: ("Skill Block",None,           "Individual Skill",  None),
    105: ("Skill Block",None,           "Individual Skill",  None),
    106: ("Skill Block",None,           "Individual Skill",  None),
    107: ("Skill Block",None,           "Individual Skill",  None),
    108: ("Skill Block",None,           "Individual Skill",  None),
    109: ("Skill Block",None,           "Individual Skill",  None),
    110: ("Skill Block","Closer",       "Individual Skill",  "Competitive Reps"),
}

SLOT_COLORS = {
    "Opener":      ("#E8F4FD", "#1565C0"),
    "Skill Block": ("#FFF3E0", "#E65100"),
    "Closer":      ("#E8F5E9", "#2E7D32"),
}
TYPE_COLORS = {
    "Individual Skill":  ("#F3E5F5", "#6A1B9A"),
    "Team Comm.":        ("#E3F2FD", "#0D47A1"),
    "Competitive Reps":  ("#FCE4EC", "#880E4F"),
    "Decision Making":   ("#F9FBE7", "#558B2F"),
}

if __name__ == "__main__":
    from drills import DRILLS
    missing = [d for d in DRILLS if d not in DRILL_TAGS]
    print(f"Tags: {len(DRILL_TAGS)} | Missing: {missing or 'none'}")
