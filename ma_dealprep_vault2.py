import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import feedparser
import random
import json
import streamlit.components.v1 as components

# ==========================================
# PAGE CONFIG
# ==========================================
st.set_page_config(page_title="M&A DealPrep Vault", layout="wide", page_icon="🏆")

st.title("🏆 M&A DealPrep Vault")
st.caption("Live Deal News, Interactive Case Studies & Technical Interview Simulator for Aspiring Investment Bankers")

tab_news, tab_case, tab_qa, tab_math, tab_practice = st.tabs(
    ["📰 Live M&A News", "📊 Interactive Case Studies", "🧠 Technical Q&A Bank",
     "⚡ Mental Math Shortcuts", "🎤 Talking & Video Practice"]
)

with st.sidebar.expander("🔒 Privacy & Permissions — read before using camera/mic"):
    st.write(
        "- This app **never** has a server-side component that stores, uploads, or logs your camera or "
        "microphone. The video preview and live transcript in the Practice tab run entirely inside your "
        "own browser tab and vanish the moment you close it or refresh.\n"
        "- **Exception to know about:** the *live transcript* feature uses Chrome/Edge's built-in Speech "
        "Recognition, which sends your audio to Google's or Microsoft's servers to generate text — that's "
        "a browser feature outside this app's control, not something this app does itself.\n"
        "- If you'd rather not send audio anywhere, use **🔒 Fully offline mode** in the Practice tab — "
        "zero camera/mic permissions requested, just a local timer and a self-rating checklist.\n"
        "- Run this app with `streamlit run` on your own machine rather than deploying it publicly if "
        "you plan to use the camera feature at all."
    )

# ==========================================
# TAB: LIVE M&A NEWS
# ==========================================

NEWS_FEEDS = {
    "All M&A / Global Deals": "https://news.google.com/rss/search?q=mergers+and+acquisitions+when:3d&hl=en-US&gl=US&ceid=US:en",
    "Healthcare & MedTech M&A": "https://news.google.com/rss/search?q=(healthcare+OR+medtech+OR+%22medical+device%22)+(merger+OR+acquisition)+when:5d&hl=en-US&gl=US&ceid=US:en",
    "Tech M&A": "https://news.google.com/rss/search?q=technology+(merger+OR+acquisition)+when:3d&hl=en-US&gl=US&ceid=US:en",
    "Private Equity / Buyouts": "https://news.google.com/rss/search?q=private+equity+buyout+when:3d&hl=en-US&gl=US&ceid=US:en",
    "Cross-Border Deals": "https://news.google.com/rss/search?q=cross-border+acquisition+when:5d&hl=en-US&gl=US&ceid=US:en",
}


@st.cache_data(ttl=1800, show_spinner="Fetching latest deal headlines...")
def fetch_news(feed_url: str):
    feed = feedparser.parse(feed_url)
    return feed.entries


with tab_news:
    st.header("📰 Live Global M&A News Feed")
    st.write("Pulled live from Google News RSS — no API key needed. Pick a category and refresh anytime.")

    col_a, col_b = st.columns([2, 1])
    with col_a:
        category = st.selectbox("Filter by sector", list(NEWS_FEEDS.keys()), index=0, key="news_cat")
    with col_b:
        num_articles = st.slider("Number of headlines", 5, 25, 12)

    if st.button("🔄 Refresh feed now"):
        st.cache_data.clear()

    try:
        entries = fetch_news(NEWS_FEEDS[category])[:num_articles]
        if not entries:
            st.warning("No articles came back. Try refreshing in a moment or switch category.")
        for e in entries:
            published = e.get("published", "Date unavailable")
            source = e.get("source", {}).get("title", "")
            st.markdown(f"**[{e.title}]({e.link})**")
            st.caption(f"{source} · {published}")
            st.divider()
    except Exception as ex:
        st.error(f"Couldn't load news right now ({ex}). Check your internet connection and try again.")

    st.info(
        "💡 Interview tip: bankers love asking 'walk me through a deal you've been following.' "
        "Pick a fresh headline above, then practice explaining the strategic rationale, funding mix, "
        "and whether it looks accretive or dilutive — using the Case Study and Q&A tabs as a refresher."
    )

# ==========================================
# TAB: INTERACTIVE M&A CASE STUDY ENGINE
# ==========================================
with tab_case:
    st.header("Live Deal Analysis: James Hardie (JHX) / The AZEK Company")

    standalone_target_price = 41.39
    target_diluted_shares = 147.48  # Millions
    acquirer_shares = 439.60        # Millions
    acquirer_standalone_eps = 3.50
    target_net_income = 120.0       # Millions
    acquirer_net_income = 1538.6    # Millions
    acquirer_share_price = 28.14

    st.sidebar.header("🎯 Live Deal Adjustments")
    offer_premium = st.sidebar.slider("Offer Premium (%)", min_value=0, max_value=100, value=20) / 100

    st.sidebar.subheader("Funding Structure Mix")
    debt_pct = st.sidebar.slider("Debt Funding (%)", min_value=0, max_value=100, value=46) / 100
    stock_pct = 1.0 - debt_pct
    st.sidebar.info(f"Remaining Stock Funding automatically set to: {stock_pct*100:.1f}%")

    interest_rate = st.sidebar.number_input("New Debt Interest Rate (%)", min_value=1.0, max_value=15.0, value=6.0) / 100
    cost_synergies = st.sidebar.number_input("Estimated Cost Synergies ($ Millions)", min_value=0.0, value=50.0)

    # --- Financial Model Math Engine ---
    offer_price_per_share = standalone_target_price * (1 + offer_premium)
    purchase_equity_value = offer_price_per_share * target_diluted_shares

    debt_issued = purchase_equity_value * debt_pct
    stock_issued_val = purchase_equity_value * stock_pct
    new_shares_issued = stock_issued_val / acquirer_share_price if stock_pct > 0 else 0.0

    after_tax_interest_expense = debt_issued * interest_rate * (1 - 0.25)
    after_tax_synergies = cost_synergies * (1 - 0.25)

    combined_net_income = acquirer_net_income + target_net_income + after_tax_synergies - after_tax_interest_expense
    combined_shares = acquirer_shares + new_shares_issued
    pro_forma_eps = combined_net_income / combined_shares

    eps_accretion_dilution_usd = pro_forma_eps - acquirer_standalone_eps
    eps_accretion_pct = (eps_accretion_dilution_usd / acquirer_standalone_eps) * 100

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Offer Price Per Share", f"${offer_price_per_share:.2f}")
    col2.metric("Purchase Equity Value", f"${purchase_equity_value:,.2f}M")
    col3.metric("Implied Target P/E Multiple", f"{(purchase_equity_value / target_net_income):.1f}x")

    if eps_accretion_pct >= 0:
        col4.metric("Accretion / (Dilution) %", f"+{eps_accretion_pct:.2f}%", delta="Accretive")
    else:
        col4.metric("Accretion / (Dilution) %", f"{eps_accretion_pct:.2f}%", delta="Dilutive", delta_color="inverse")

    st.subheader("Standalone vs. Pro Forma EPS Comparison")
    fig = go.Figure(data=[
        go.Bar(name='Acquirer Standalone EPS', x=['Earnings Per Share'], y=[acquirer_standalone_eps], marker_color='#1f77b4'),
        go.Bar(name='Pro Forma Combined EPS', x=['Earnings Per Share'], y=[pro_forma_eps],
               marker_color='#2ca02c' if eps_accretion_pct >= 0 else '#d62728')
    ])
    fig.update_layout(barmode='group', height=350, yaxis_title="USD ($)")
    st.plotly_chart(fig, use_container_width=True)

    with st.expander("📝 How to talk about this in an interview"):
        st.write(
            "Practice narrating this model out loud in under 60 seconds: state the offer price and premium, "
            "the funding mix, why debt funding helps EPS (cheaper than equity, tax-deductible interest) while "
            "stock funding hurts it (dilution, no tax shield), and conclude with whether the deal is accretive "
            "or dilutive and why. This is the exact structure interviewers expect."
        )

# ==========================================
# TAB: TECHNICAL Q&A BANK
# ==========================================
with tab_qa:
    st.header("🧠 Technical Interview Question Bank")
    st.write("Curated for a fresher IB interview. Filter by topic, then browse or quiz yourself.")

    QUESTION_BANK = [
        {"category": "Accounting", "q": "Walk me through the three financial statements and how they link together.",
         "a": "Net income from the Income Statement flows into Retained Earnings on the Balance Sheet and is the "
              "starting line of the Cash Flow Statement. The Cash Flow Statement adjusts net income for non-cash "
              "items (D&A, stock comp) and working capital changes, then layers in investing and financing "
              "activities. The ending cash balance flows back onto the Balance Sheet, which must balance via "
              "Assets = Liabilities + Equity."},
        {"category": "Accounting", "q": "If depreciation increases by $10, how does each statement change (with a 25% tax rate)?",
         "a": "Income Statement: pre-tax income falls $10, taxes fall $2.5, net income falls $7.5. Cash Flow "
              "Statement: net income down $7.5, but the D&A add-back is up $10, so cash from operations rises "
              "$2.5. Balance Sheet: cash up $2.5, PP&E down $10, so total assets fall $7.5; retained earnings "
              "fall $7.5 from the lower net income — both sides stay balanced."},
        {"category": "Accounting", "q": "What's the difference between accrual and cash accounting?",
         "a": "Accrual accounting records revenue and expenses when they're earned or incurred, regardless of "
              "when cash actually moves. Cash accounting only records a transaction when cash changes hands. "
              "Public companies use accrual accounting under GAAP/IFRS because it matches revenue to the "
              "expenses that generated it."},
        {"category": "Valuation", "q": "Walk me through how you'd value a company.",
         "a": "Three core approaches, usually triangulated together in a 'football field': (1) Comparable "
              "Companies Analysis — apply trading multiples like EV/EBITDA or P/E from similar public peers; "
              "(2) Precedent Transactions Analysis — apply multiples paid in similar past M&A deals, typically "
              "higher due to a control premium; (3) Discounted Cash Flow — project unlevered free cash flows "
              "and discount them, plus a terminal value, back to present value using the WACC."},
        {"category": "Valuation", "q": "Why might a DCF produce a higher valuation than comparable companies analysis?",
         "a": "A DCF is independent of current market sentiment, so depressed public markets, optimistic "
              "growth/margin assumptions, or a low discount rate can push it above what trading comps imply. "
              "It's also very sensitive to terminal value, which often makes up most of total value."},
        {"category": "Valuation", "q": "What's the difference between Enterprise Value and Equity Value?",
         "a": "Equity Value is what shareholders own — share price times diluted shares. Enterprise Value is the "
              "value of the whole operating business to all capital providers: Equity Value + Debt + Preferred "
              "Stock + Minority Interest − Cash. EV is capital-structure-neutral, so it pairs with revenue/EBITDA "
              "multiples, while Equity Value pairs with net-income-based multiples like P/E."},
        {"category": "Valuation", "q": "Why use EV/EBITDA instead of P/E?",
         "a": "EV/EBITDA strips out the effects of capital structure (interest expense) and non-cash items "
              "(D&A), making it easier to compare companies with different debt levels or depreciation "
              "policies. P/E is distorted by leverage and tax rates, so it's less useful across companies with "
              "very different financing choices."},
        {"category": "M&A", "q": "Walk me through a basic merger model / accretion-dilution analysis.",
         "a": "Step 1: project standalone financials for acquirer and target. Step 2: determine purchase price "
              "and the funding mix across cash, debt, and stock. Step 3: combine the income statements — add "
              "the target's net income, subtract after-tax interest on new debt (or lost interest on cash "
              "used), add after-tax synergies, then divide combined net income by the new pro forma share "
              "count. Compare pro forma EPS to the acquirer's standalone EPS to see if the deal is accretive "
              "or dilutive."},
        {"category": "M&A", "q": "Why would an M&A transaction be dilutive to the acquirer's EPS?",
         "a": "It's dilutive when the incremental earnings the target brings in don't fully offset the cost of "
              "funding the deal — interest on new debt, lost interest income on cash used, and/or dilution "
              "from issuing new shares. Stock deals where the acquirer trades at a lower P/E than the target "
              "are a classic source of dilution."},
        {"category": "M&A", "q": "What's the difference between a strategic buyer and a financial buyer?",
         "a": "A strategic buyer is an operating company acquiring for synergies — cost savings, cross-sell, "
              "market access — and can justify paying more because it captures value beyond the target's "
              "standalone cash flows. A financial buyer (e.g. a PE firm) underwrites standalone returns, "
              "typically uses leverage, and exits in roughly 3–7 years, so it's more price-disciplined absent "
              "an add-on angle."},
        {"category": "M&A", "q": "What is a synergy, and what's the difference between cost and revenue synergies?",
         "a": "Synergies are the extra value created by combining two companies beyond what they'd achieve "
              "separately. Cost synergies come from eliminating duplicate functions or overhead and are seen "
              "as more reliable and quicker to realize. Revenue synergies come from cross-selling or expanded "
              "distribution, but are harder to predict, so they're discounted heavily in deal models."},
        {"category": "M&A", "q": "What is a control premium, and why does it exist?",
         "a": "It's the amount an acquirer pays above the target's unaffected (pre-announcement) share price to "
              "gain control. It exists because control lets the buyer make decisions, extract synergies, and "
              "direct cash flows in ways a passive minority shareholder can't — which is why precedent "
              "transaction multiples typically run higher than trading comps."},
        {"category": "LBO", "q": "What makes a good LBO candidate?",
         "a": "Stable, predictable cash flows to service debt; low ongoing capex needs; a strong, defensible "
              "market position; an undervalued or non-cyclical asset; and room for operational improvement or "
              "a clear exit path within a typical 3–7 year hold."},
        {"category": "LBO", "q": "Walk me through a basic LBO model.",
         "a": "Step 1: set the purchase price (often an EV/EBITDA multiple) and the sources & uses of funds — "
              "mostly debt plus a sponsor equity check. Step 2: project the operating model and free cash "
              "flow, using FCF to pay down debt over the hold. Step 3: assume an exit multiple (often similar "
              "to entry) applied to exit-year EBITDA, subtract remaining debt to get exit equity value, then "
              "compute IRR and MOIC versus the equity invested."},
        {"category": "Fit", "q": "Why investment banking?",
         "a": "A strong answer ties genuine interest in deal-making and corporate finance to specific steps "
              "you've already taken — modeling practice, networking with bankers, following live deals — and "
              "to what you want to learn next: how to value businesses, structure transactions, and work "
              "closely with senior leadership on high-stakes decisions. Avoid generic answers about prestige "
              "or pay."},
        {"category": "Fit", "q": "Walk me through a recent M&A deal you've been following and why it's interesting.",
         "a": "Pick one specific, recent deal. Cover who's buying whom, the strategic rationale, how it's "
              "funded (cash/stock/debt mix), the multiple paid versus comps, and the market's reaction "
              "(accretive/dilutive, stock move). Use the Live M&A News tab to pick a fresh headline and "
              "rehearse this exact structure on it."},
    ]

    categories = ["All"] + sorted(set(q["category"] for q in QUESTION_BANK))
    chosen_cat = st.selectbox("Topic", categories)
    filtered = QUESTION_BANK if chosen_cat == "All" else [q for q in QUESTION_BANK if q["category"] == chosen_cat]

    mode = st.radio("Mode", ["📖 Browse all", "🎲 Random Quiz Mode"], horizontal=True)

    if mode == "📖 Browse all":
        for item in filtered:
            with st.expander(f"[{item['category']}] {item['q']}"):
                st.info(item['a'])
    else:
        if "quiz_q" not in st.session_state or st.session_state.get("quiz_cat") != chosen_cat:
            st.session_state.quiz_q = random.choice(filtered)
            st.session_state.quiz_cat = chosen_cat
            st.session_state.revealed = False

        if st.button("🎲 Next question"):
            st.session_state.quiz_q = random.choice(filtered)
            st.session_state.revealed = False

        q = st.session_state.quiz_q
        st.subheader(f"[{q['category']}] {q['q']}")

        if st.button("👁️ Reveal answer"):
            st.session_state.revealed = True

        if st.session_state.get("revealed"):
            st.success(q['a'])
        else:
            st.caption("Say your answer out loud before revealing — that's what actually builds interview fluency.")

# ==========================================
# TAB: MENTAL MATH SHORTCUTS
# ==========================================
with tab_math:
    st.header("⚡ Investment Banking Mental Math Toolkit")

    st.subheader("1. The P/E Rule for 100% Stock Deals")
    st.write(
        "A senior banker will often ask you to call accretion/dilution within 5 seconds, no calculator. "
        "**Rule:** in a 100% stock deal, if the Acquirer's P/E is **higher** than the Target's implied "
        "purchase P/E, the deal is **Accretive**. If the Acquirer's P/E is lower, it's **Dilutive**."
    )
    acq_pe = st.number_input("Acquirer P/E Multiple", value=20.0, key="pe_acq")
    tgt_pe = st.number_input("Target P/E Multiple", value=15.0, key="pe_tgt")
    if acq_pe > tgt_pe:
        st.success(f"Acquirer P/E ({acq_pe}x) > Target P/E ({tgt_pe}x) → instantly **ACCRETIVE**.")
    else:
        st.error(f"Acquirer P/E ({acq_pe}x) < Target P/E ({tgt_pe}x) → instantly **DILUTIVE**.")

    st.divider()
    st.subheader("2. Quick Cash-Deal Accretion Check")
    st.write(
        "**Rule of thumb:** in an all-cash deal, compare the Target's earnings yield (Net Income ÷ Purchase "
        "Equity Value, i.e. the inverse of the purchase P/E) to the acquirer's after-tax cost of cash/debt. "
        "If the target's earnings yield is **higher** than the funding cost, the deal is accretive."
    )
    target_ni = st.number_input("Target Net Income ($M)", value=120.0, key="cash_ni")
    purchase_val = st.number_input("Purchase Equity Value ($M)", value=6100.0, key="cash_val")
    after_tax_cost = st.number_input("After-Tax Cost of Funds (%)", value=4.5, key="cash_cost") / 100
    earnings_yield = target_ni / purchase_val if purchase_val else 0
    st.write(f"Target earnings yield: **{earnings_yield*100:.2f}%** vs. after-tax cost of funds: **{after_tax_cost*100:.2f}%**")
    if earnings_yield > after_tax_cost:
        st.success("Earnings yield > cost of funds → **ACCRETIVE**.")
    else:
        st.error("Earnings yield < cost of funds → **DILUTIVE**.")

    st.divider()
    st.subheader("3. Rule of 72")
    st.write("Quick way to estimate doubling time for a growth rate: **72 ÷ growth rate % ≈ years to double**.")
    growth = st.number_input("Annual Growth / Return Rate (%)", value=12.0, key="r72")
    if growth > 0:
        st.write(f"At {growth}% per year, a value roughly doubles in **{72/growth:.1f} years**.")

# ==========================================
# TAB: TALKING & VIDEO PRACTICE
# ==========================================
with tab_practice:
    st.header("🎤 Talking & Video Interview Practice")
    st.write(
        "Turn a real deal into a spoken answer, then rehearse it on camera. The app times you, "
        "transcribes your speech live in the browser, and scores your pace, filler words, and "
        "talking-point coverage — like a self-run mock interview."
    )

    # ---------- STEP 1: Pick or paste a deal ----------
    st.subheader("Step 1 — Pick a deal")
    source_mode = st.radio(
        "Source", ["Pull a headline from the News tab", "Paste my own deal summary"],
        horizontal=True, key="practice_source"
    )

    headline = ""
    if source_mode == "Pull a headline from the News tab":
        col1, col2 = st.columns([1, 2])
        with col1:
            practice_cat = st.selectbox("Sector", list(NEWS_FEEDS.keys()), key="practice_cat")
        try:
            practice_entries = fetch_news(NEWS_FEEDS[practice_cat])[:15]
            titles = [e.title for e in practice_entries] if practice_entries else []
        except Exception:
            titles = []
        with col2:
            if titles:
                headline = st.selectbox("Headline", titles, key="practice_headline_select")
            else:
                st.warning("No headlines loaded yet — visit the News tab first, or paste your own summary instead.")
    else:
        headline = st.text_input("Deal headline", placeholder="e.g. Acme Health to acquire MedDevice Co for $2.1B")

    # ---------- STEP 2: Structured deal facts ----------
    st.subheader("Step 2 — Fill in the deal facts")
    st.caption("Pull these from the article. Leave blank if a detail wasn't reported — the script will adapt.")

    c1, c2 = st.columns(2)
    with c1:
        acquirer = st.text_input("Acquirer", key="p_acq")
        rationale = st.text_area("Strategic rationale (1 short sentence)", key="p_rationale",
                                  placeholder="e.g. expands the acquirer's diagnostics portfolio into Europe")
        your_view = st.selectbox("Your read on the deal", ["Accretive", "Dilutive", "Too early to tell"], key="p_view")
    with c2:
        target = st.text_input("Target", key="p_tgt")
        terms = st.text_input("Premium / multiple paid", key="p_terms",
                               placeholder="e.g. 22% premium, ~13x EBITDA")
        funding = st.text_input("Funding mix", key="p_funding", placeholder="e.g. 70% cash, 30% stock")

    why_view = st.text_input("One-line reason for your read", key="p_why",
                              placeholder="e.g. cash-funded at a reasonable multiple with clear cost synergies")

    if st.button("✍️ Generate practice scripts", type="primary"):
        if not acquirer or not target:
            st.warning("Add at least the Acquirer and Target names so the script has something to anchor on.")
        else:
            rationale_txt = rationale.strip() or "strengthen its position in a related market"
            terms_txt = terms.strip() or "terms that weren't fully disclosed"
            funding_txt = funding.strip() or "a mix of cash and stock"
            why_txt = why_view.strip() or "of how the funding mix and multiple compare to peers"

            elevator_script = (
                f"{acquirer} is acquiring {target}{(' — ' + headline) if headline and headline not in (acquirer, target) else ''}. "
                f"The deal is meant to {rationale_txt}, funded through {funding_txt}, at {terms_txt}. "
                f"My read is that it's {your_view.lower()}, mainly because {why_txt}."
            )

            full_script = (
                f"So the deal I've been following is {acquirer}'s acquisition of {target}. "
                f"{('Headline context: ' + headline + '. ') if headline else ''}"
                f"Strategically, the idea is to {rationale_txt} — which makes sense given how competitive that space has gotten. "
                f"On terms, {acquirer} is paying {terms_txt}, funded through {funding_txt}. "
                f"That funding mix matters because it directly drives the earnings impact — debt is cheaper and tax-deductible "
                f"but adds leverage, while stock avoids debt but dilutes existing shareholders. "
                f"Putting that together, I'd call this deal {your_view.lower()}, largely because {why_txt}. "
                f"If I were on the deal team, the thing I'd want to stress-test next is whether the projected synergies "
                f"are realistic, and how the market has reacted to the announcement so far."
            )

            bullets = [
                f"Who: {acquirer} buying {target}",
                f"Why: {rationale_txt}",
                f"Terms: {terms_txt}",
                f"Funding: {funding_txt}",
                f"View: {your_view} — {why_txt}",
                "Follow-up: synergy realism + market reaction",
            ]

            st.session_state.gen_elevator = elevator_script
            st.session_state.gen_full = full_script
            st.session_state.gen_bullets = bullets
            st.session_state.gen_keyterms = [acquirer, target] + [w for w in [
                "synerg", "premium", "multiple", "cash", "stock", "debt", "accretive", "dilutive"
            ] if w.lower() in (rationale_txt + terms_txt + funding_txt + why_txt).lower()]

    if "gen_full" in st.session_state:
        st.divider()
        st.subheader("Your generated scripts")
        v1, v2, v3 = st.tabs(["🚀 30s Elevator Version", "🎯 60–90s Full Answer", "📋 Bullet Cheat Sheet"])
        with v1:
            st.markdown(f"> {st.session_state.gen_elevator}")
        with v2:
            st.markdown(f"> {st.session_state.gen_full}")
        with v3:
            for b in st.session_state.gen_bullets:
                st.write(f"- {b}")

        st.caption(
            "Edit any of the fields above and regenerate as many times as you like — the goal is a script "
            "that sounds like *you*, not a script to memorize word-for-word."
        )

        # ---------- STEP 3: Talking & video practice ----------
        st.divider()
        st.subheader("Step 3 — Practice on camera")
        practice_script_choice = st.radio(
            "Which version do you want to rehearse?",
            ["60–90s Full Answer", "30s Elevator Version"], horizontal=True, key="practice_choice"
        )
        script_to_show = (
            st.session_state.gen_full if practice_script_choice == "60–90s Full Answer"
            else st.session_state.gen_elevator
        )

        st.markdown(
            f"<div style='font-size:1.15rem; line-height:1.6; background:#f5f5f5; "
            f"padding:16px; border-radius:8px;'>{script_to_show}</div>",
            unsafe_allow_html=True
        )

        st.write("")

        practice_privacy_mode = st.radio(
            "Practice mode",
            ["🎙️ Camera + live transcript (uses Chrome/Edge speech recognition)",
             "🔒 Fully offline — timer + self-rating only, no camera/mic at all"],
            key="privacy_mode"
        )

        if practice_privacy_mode.startswith("🎙️"):
            st.warning(
                "**Be aware before you turn this on:** the live transcript uses your browser's *built-in* "
                "Speech Recognition. This app never receives, stores, or uploads your audio or video — the "
                "video preview and transcript run entirely inside your browser tab and disappear when you "
                "close it. **However**, Chrome/Edge's speech recognition engine itself sends your audio to "
                "Google's or Microsoft's servers to generate the transcript — that's a browser feature, "
                "outside this app's control. If you'd rather not send audio anywhere, use the fully offline "
                "mode below instead."
            )
            key_terms_json = json.dumps(st.session_state.gen_keyterms)

            practice_html = """
<div style="font-family: -apple-system, sans-serif;">
  <video id="preview" autoplay muted playsinline
         style="width:280px; height:210px; border-radius:10px; background:#111; object-fit:cover;"></video>
  <div style="margin-top:10px;">
    <button id="startBtn" style="padding:8px 16px; border-radius:6px; border:none; background:#2563eb; color:white; cursor:pointer;">▶️ Start Practice</button>
    <button id="stopBtn" disabled style="padding:8px 16px; border-radius:6px; border:none; background:#dc2626; color:white; cursor:pointer;">⏹ Stop</button>
    <span id="timer" style="margin-left:10px; font-size:1.1rem; font-weight:600;">00:00</span>
  </div>
  <h4 style="margin-bottom:4px;">Live Transcript</h4>
  <div id="transcript" style="border:1px solid #ddd; padding:10px; min-height:70px; white-space:pre-wrap; border-radius:6px; background:#fafafa;"></div>
  <div id="results" style="margin-top:12px;"></div>
</div>
<script>
const keyTerms = __KEYTERMS_JSON__;
let recognition;
let startTime;
let timerInterval;
let finalTranscript = "";

const video = document.getElementById('preview');
navigator.mediaDevices.getUserMedia({video:true, audio:false}).then(function(stream){
  video.srcObject = stream;
}).catch(function(err){
  document.getElementById('results').innerHTML = "<p style='color:#b91c1c'>Camera unavailable or permission denied: " + err + "</p>";
});

function fmtTime(s){
  const m = Math.floor(s/60).toString().padStart(2,'0');
  const sec = (s%60).toString().padStart(2,'0');
  return m + ":" + sec;
}

document.getElementById('startBtn').onclick = function(){
  finalTranscript = "";
  document.getElementById('transcript').innerText = "";
  document.getElementById('results').innerHTML = "";
  startTime = Date.now();
  document.getElementById('startBtn').disabled = true;
  document.getElementById('stopBtn').disabled = false;
  timerInterval = setInterval(function(){
    const elapsed = Math.floor((Date.now()-startTime)/1000);
    document.getElementById('timer').innerText = fmtTime(elapsed);
  }, 500);

  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SpeechRecognition){
    document.getElementById('results').innerHTML = "<p style='color:#b91c1c'>Live transcription needs Chrome or Edge. You can still rehearse on camera and self-time.</p>";
    return;
  }
  recognition = new SpeechRecognition();
  recognition.continuous = true;
  recognition.interimResults = true;
  recognition.lang = 'en-US';
  recognition.onresult = function(event){
    let interim = "";
    for (let i = event.resultIndex; i < event.results.length; i++){
      const t = event.results[i][0].transcript;
      if (event.results[i].isFinal){ finalTranscript += t + " "; }
      else { interim += t; }
    }
    document.getElementById('transcript').innerText = finalTranscript + interim;
  };
  recognition.onerror = function(e){ console.log(e); };
  try { recognition.start(); } catch(e) { console.log(e); }
};

document.getElementById('stopBtn').onclick = function(){
  clearInterval(timerInterval);
  document.getElementById('stopBtn').disabled = true;
  document.getElementById('startBtn').disabled = false;
  if (recognition){ try { recognition.stop(); } catch(e) {} }
  const elapsedSec = Math.max(1, Math.floor((Date.now()-startTime)/1000));
  analyze(finalTranscript, elapsedSec);
};

function analyze(text, elapsedSec){
  const words = text.trim().split(/\\s+/).filter(Boolean);
  const wordCount = words.length;
  const wpm = Math.round(wordCount / (elapsedSec/60));
  const fillers = ["um","uh","like","you know","sort of","kind of","basically","actually","i mean"];
  let fillerCount = 0;
  const lowerText = text.toLowerCase();
  fillers.forEach(function(f){
    const re = new RegExp("\\\\b" + f.replace(" ", "\\\\s") + "\\\\b", "g");
    const matches = lowerText.match(re);
    if (matches) fillerCount += matches.length;
  });
  let covered = 0;
  keyTerms.forEach(function(k){ if (k && lowerText.includes(k.toLowerCase())) covered++; });
  const coveragePct = keyTerms.length ? Math.round((covered/keyTerms.length)*100) : 0;

  let paceFeedback = "";
  if (wpm < 110) paceFeedback = "A bit slow — aim for 130-160 wpm to sound confident rather than hesitant.";
  else if (wpm > 175) paceFeedback = "A bit fast — ease off slightly so it reads as composed, not rushed.";
  else paceFeedback = "Good pace — right in the confident interview range.";

  let html = "<h4>Results</h4>";
  html += "<p><b>Duration:</b> " + fmtTime(elapsedSec) + " &nbsp; <b>Words:</b> " + wordCount + " &nbsp; <b>Pace:</b> " + (isFinite(wpm) ? wpm : 0) + " wpm</p>";
  html += "<p>" + paceFeedback + "</p>";
  html += "<p><b>Filler words:</b> " + fillerCount + (fillerCount > 3 ? " — try trimming these for a crisper delivery." : " — clean delivery.") + "</p>";
  html += "<p><b>Key talking points hit:</b> " + covered + "/" + keyTerms.length + " (" + coveragePct + "%)</p>";
  if (wordCount === 0){
    html = "<p style='color:#b91c1c'>No speech was captured — check your mic permissions and try again.</p>";
  }
  document.getElementById('results').innerHTML = html;
}
</script>
"""
            practice_html = practice_html.replace("__KEYTERMS_JSON__", key_terms_json)
            components.html(practice_html, height=560)

            st.caption(
                "💡 Run it 2-3 times back to back. Watch your filler-word count trend down and your coverage "
                "of key points trend toward 100% — that consistency is what reads as 'interview-ready' to a banker."
            )

        else:
            st.success(
                "✅ Zero permissions requested in this mode — no camera, no mic, nothing leaves your screen. "
                "Use a phone or watch timer and rate yourself honestly."
            )
            offline_html = """
<div style="font-family: -apple-system, sans-serif;">
  <div style="margin-top:6px;">
    <button id="oStart" style="padding:8px 16px; border-radius:6px; border:none; background:#2563eb; color:white; cursor:pointer;">▶️ Start timing</button>
    <button id="oStop" disabled style="padding:8px 16px; border-radius:6px; border:none; background:#dc2626; color:white; cursor:pointer;">⏹ Stop</button>
    <span id="oTimer" style="margin-left:10px; font-size:1.1rem; font-weight:600;">00:00</span>
  </div>
  <p style="margin-top:8px; color:#555;">Deliver your answer out loud, facing a mirror or blank wall if you want a posture check, then stop the timer and fill in the checklist below in Streamlit.</p>
</div>
<script>
let oStart, oInterval;
document.getElementById('oStart').onclick = function(){
  oStart = Date.now();
  document.getElementById('oStart').disabled = true;
  document.getElementById('oStop').disabled = false;
  oInterval = setInterval(function(){
    const e = Math.floor((Date.now()-oStart)/1000);
    const m = Math.floor(e/60).toString().padStart(2,'0');
    const s = (e%60).toString().padStart(2,'0');
    document.getElementById('oTimer').innerText = m+":"+s;
  }, 500);
};
document.getElementById('oStop').onclick = function(){
  clearInterval(oInterval);
  document.getElementById('oStop').disabled = true;
  document.getElementById('oStart').disabled = false;
};
</script>
"""
            components.html(offline_html, height=110)

            st.markdown("**Self-rating checklist** — fill in right after you stop the timer:")
            cc1, cc2 = st.columns(2)
            with cc1:
                st.select_slider("Pace", ["Too slow", "A bit slow", "Just right", "A bit fast", "Too fast"],
                                  value="Just right", key="off_pace")
                st.select_slider("Filler words (um/like/you know)", ["None noticed", "A few", "Several", "A lot"],
                                  value="A few", key="off_fillers")
            with cc2:
                covered = st.multiselect(
                    "Key points you actually said out loud",
                    st.session_state.gen_keyterms, key="off_covered"
                )
                st.select_slider("Overall confidence", ["Shaky", "Okay", "Solid", "Very confident"],
                                  value="Okay", key="off_conf")
            if st.session_state.gen_keyterms:
                st.caption(
                    f"Coverage: {len(st.session_state.get('off_covered', []))}/"
                    f"{len(st.session_state.gen_keyterms)} key points hit this run."
                )
    else:
        st.info("Fill in Step 1 and 2 above, then click **Generate practice scripts** to unlock the camera practice tool.")

st.sidebar.divider()
st.sidebar.caption(
    "📚 For deeper technical drilling beyond this app, cross-reference Rosenbaum & Pearl's "
    "*Investment Banking* and your 400 Questions IB Interview Guide."
)