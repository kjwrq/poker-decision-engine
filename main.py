import streamlit as st
from config import EMPTY, DECK
from poker_sim import chances
from llm_agent import get_llm_decision
from typing import List, Tuple, Optional

def validate(selected_cards: List[Optional[str]]) -> Tuple[bool, str]:
    cards = [c for c in selected_cards if c != EMPTY]
    if len(cards) == 0:
        return False, "Please select at least the hole cards"
    if len(cards) != len(set(cards)):
        return False, "Duplicate cards detected. Each card can only be used once"
    return True, ""

def main():
    st.set_page_config(page_title="AI Poker Decision Maker")
    st.title("AI Poker Decision Maker")

    with st.form("poker_inputs"):
        st.header("Game setup")
        g1, g2, g3 = st.columns(3)
        with g1:
            position = st.selectbox("Position", ["Early", "Middle", "Late", "Blind"], index=0)
        with g2:
            stack = st.selectbox("Stack size", ["Small", "Medium", "Big"], index=1)
            # [small] <40bb, [medium] 41-90bb, [big] >91bb
        with g3:
            opponents = st.slider("Opponents", min_value=1, max_value=8, value=5)

        st.divider()

        st.subheader("Your hole cards")
        h1, h2 = st.columns(2)
        with h1:
            hole_1 = st.selectbox("Hole 1", options=DECK, index=51)
        with h2:
            hole_2 = st.selectbox("Hole 2", options=DECK, index=50)
        
        st.divider()

        st.subheader("Community cards (Flop)")
        c1, c2, c3, c4, c5 = st.columns(5)
        with c1:
            flop_1 = st.selectbox("Flop 1", options=[EMPTY]+DECK, index=0)
        with c2:
            flop_2 = st.selectbox("Flop 2", options=[EMPTY]+DECK, index=0)
        with c3:
            flop_3 = st.selectbox("Flop 3", options=[EMPTY]+DECK, index=0)
        with c4:
            turn = st.selectbox("Turn", options=[EMPTY]+DECK, index=0)
        with c5:
            river = st.selectbox("River", options=[EMPTY]+DECK, index=0)

        st.divider()

        risk = st.selectbox("Risk level", options=["Tight", "Balanced", "Aggressive"], index=1)

        submitted = st.form_submit_button("Analyze hand")

    if submitted:
        selected = [hole_1, hole_2, flop_1, flop_2, flop_3, turn, river]
        ok, err = validate(selected)

        if not ok:
            st.error(err)
            st.stop()

        board = [c for c in [flop_1, flop_2, flop_3, turn, river] if c != EMPTY]

        game_state = {
            "hole": [hole_1, hole_2],
            "board": board,
            "position": position,
            "stack": stack,
            "opponents": opponents
        }
        sim = chances(game_state, n_sims=3000)

        decision = get_llm_decision(game_state, sim, risk)
        if decision["decision"] == "Fold":
            st.error(decision["decision"])
        else:
            st.success(decision["decision"])
        st.write(decision["reasoning"])
        st.progress(float(decision["confidence"]))

        st.subheader("Game state")
        st.json(game_state)

        st.subheader("Simulation results")
        st.json(sim)

if __name__ == "__main__":
    main()