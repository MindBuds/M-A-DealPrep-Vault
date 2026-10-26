import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import feedparser
import random

# ==========================================
# PAGE CONFIG
# ==========================================
st.set_page_config(page_title="M&A DealPrep Vault", layout="wide", page_icon="<svg role="img" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><title>OpenAPI Initiative</title><path d="M21.039 0a2.959 2.959 0 00-2.65 4.274l-6.447 6.447a2.96 2.96 0 101.335 1.336l6.447-6.447A2.959 2.959 0 1021.04 0zM10.628 2.745c-.072 0-.143.003-.214.004-.072.002-.143.002-.215.005-.447.018-.893.064-1.335.138l-.03.005-.185.033-.105.02a7.718 7.718 0 00-.289.062l-.032.008a10.69 10.69 0 00-2.55.95l-.155.089c-.063.034-.125.07-.187.105-.046.027-.093.051-.14.079H5.19l-.01.005-.036.02v.002l.111.184 3.15 5.23a4.168 4.168 0 01.38-.202 4.294 4.294 0 011.628-.413c.071-.004.143-.008.214-.008zm.428.01v6.333c.325.034.647.103.96.209l4.66-4.66c-.173-.12-.348-.237-.528-.347l-.026-.015c-.056-.035-.112-.067-.168-.1l-.098-.056-.099-.055a12.735 12.735 0 00-.171-.092l-.027-.014a10.628 10.628 0 00-1.425-.617c-.69-.241-1.403-.41-2.128-.505l-.089-.012-.09-.01a6.56 6.56 0 00-.17-.019l-.049-.004-.204-.017a6.44 6.44 0 00-.255-.015c-.031-.003-.062-.003-.093-.004zM4.782 4.498a9.92 9.92 0 00-1.36 1.062l4.461 4.461.018.018c.049-.04.098-.078.149-.116l-.011-.018zm-1.67 1.36c-.05.05-.098.103-.147.154l-.149.155c-.33.357-.63.73-.902 1.118l-.039.056a10.588 10.588 0 00-.216.326 10.6 10.6 0 00-1.65 5.276l-.006.215-.003.214h6.317c0-.072.007-.143.01-.214.005-.072.006-.144.013-.215.081-.822.399-1.625.952-2.3.045-.055.096-.106.144-.16.048-.052.093-.107.144-.158zm16.255 1.464l-4.663 4.663c.106.312.175.634.21.959h6.332l-.004-.094a11.579 11.579 0 00-.032-.456l-.005-.052a13.044 13.044 0 00-.026-.241v-.009l-.033-.24v-.009a10.618 10.618 0 00-.327-1.493l-.003-.01a15.839 15.839 0 00-.07-.228l-.01-.03a14.111 14.111 0 00-.069-.204l-.02-.055a5.65 5.65 0 00-.153-.405 7.84 7.84 0 00-.093-.227 16.67 16.67 0 00-.063-.144l-.037-.081a13.776 13.776 0 00-.08-.171l-.024-.052-.096-.194-.014-.027a11.2 11.2 0 00-.112-.212l-.004-.008a10.615 10.615 0 00-.604-.98zm-4.43 6.05c0 .071-.006.142-.01.214-.003.072-.005.143-.012.214a4.29 4.29 0 01-.952 2.301c-.045.055-.096.107-.144.16-.048.053-.093.108-.144.159l4.467 4.467c.051-.051.099-.104.148-.155.05-.052.1-.103.148-.155.331-.358.633-.733.905-1.122l.032-.046.098-.144.085-.13.04-.063a10.597 10.597 0 001.647-5.272c.003-.071.004-.143.006-.214.001-.071.004-.143.004-.214zM.01 13.8l.004.093.01.179.005.076.017.206.005.046c.007.076.015.153.024.228l.003.022a9.605 9.605 0 00.033.248c.072.505.182 1.005.327 1.497l.002.006c.022.077.047.154.071.23l.004.014.005.014a15.737 15.737 0 00.153.439l.03.08.059.148a7.702 7.702 0 00.093.228l.062.14.038.084.078.169.027.054a10.677 10.677 0 00.225.441l.025.043 5.408-3.258.02-.012a4.314 4.314 0 01-.395-1.414h-.025zm.505 2.846l-.206.058.002.005zm6.425-1.052l-5.415 3.262c.083.139.17.273.259.406l.008.014.004.005.008.014h.001c.007.012.014.022.022.032l.001.002v.001a10.634 10.634 0 00.298.417l.006.008a9.963 9.963 0 00.29.368l.033.04c.043.052.086.103.13.153l.057.065.112.127.064.069.029.031.083.09.035.035c.049.051.098.103.149.153L7.58 16.42a3.86 3.86 0 01-.285-.321 4.422 4.422 0 01-.356-.505zm6.416 1.111c-.05.04-.1.079-.15.116l.011.018 3.257 5.407c.151-.099.3-.2.446-.307.315-.232.62-.484.914-.756l-4.46-4.46zm-5.457.003l-.015.015-4.46 4.46a8.966 8.966 0 00.195.176c.022.02.043.04.065.058l.152.13a10.622 10.622 0 00.215.174l.023.017.191.148.008.005c.268.2.547.389.834.564l.03.018.164.097.101.057a5.458 5.458 0 00.27.148c.008.004.016.01.025.013.162.085.327.164.493.24l.158-.385 2.243-5.448.009-.02a4.328 4.328 0 01-.701-.467zm4.951.353c-.061.037-.124.07-.187.104a4.318 4.318 0 01-3.271.336c-.069-.02-.135-.047-.203-.071-.067-.024-.136-.044-.202-.072l-2.242 5.444-.088.213-.075.183v.001l.017.007a.137.137 0 00.019.007l.005.003c.052.021.106.04.159.06.067.027.133.053.2.077l.102.04c.702.247 1.43.42 2.168.518l.087.012.09.01.172.019a7.173 7.173 0 00.252.022c.023.001.048.001.071.003l.184.011.112.005a7.06 7.06 0 00.358.007h.05a10.667 10.667 0 001.793-.15l.185-.034.105-.02.109-.023.18-.04.032-.008a10.684 10.684 0 002.55-.95c.052-.028.104-.06.156-.089.063-.034.125-.07.187-.105.043-.024.087-.047.13-.073h.001l.002-.002.002-.001.002-.001.007-.004.042-.025-.11-.183-.11-.184zm3.262 5.414l-.042.025.042-.024zm-.05.029zm-.005.004h-.002z"/></svg>")

st.title("M&A DealPrep Vault")
st.caption("Live Deal News, Interactive Case Studies & Technical Interview Simulator for Aspiring Investment Bankers")

tab_news, tab_case, tab_qa, tab_math = st.tabs(
    ["Live M&A News", "Interactive Case Studies", "Technical Q&A Bank", "⚡ Mental Math Shortcuts"]
)

# ==========================================
# TAB: LIVE M&A NEWS
# ==========================================
with tab_news:
    st.header(" Live Global M&A News Feed")
    st.write("Pulled live from Google News RSS — no API key needed. Pick a category and refresh anytime.")

    NEWS_FEEDS = {
        "All M&A / Global Deals": "https://news.google.com/rss/search?q=mergers+and+acquisitions+when:3d&hl=en-US&gl=US&ceid=US:en",
        "Healthcare & MedTech M&A": "https://news.google.com/rss/search?q=(healthcare+OR+medtech+OR+%22medical+device%22)+(merger+OR+acquisition)+when:5d&hl=en-US&gl=US&ceid=US:en",
        "Tech M&A": "https://news.google.com/rss/search?q=technology+(merger+OR+acquisition)+when:3d&hl=en-US&gl=US&ceid=US:en",
        "Private Equity / Buyouts": "https://news.google.com/rss/search?q=private+equity+buyout+when:3d&hl=en-US&gl=US&ceid=US:en",
        "Cross-Border Deals": "https://news.google.com/rss/search?q=cross-border+acquisition+when:5d&hl=en-US&gl=US&ceid=US:en",
    }

    col_a, col_b = st.columns([2, 1])
    with col_a:
        category = st.selectbox("Filter by sector", list(NEWS_FEEDS.keys()), index=0)
    with col_b:
        num_articles = st.slider("Number of headlines", 5, 25, 12)

    if st.button("🔄 Refresh feed now"):
        st.cache_data.clear()

    @st.cache_data(ttl=1800, show_spinner="Fetching latest deal headlines...")
    def fetch_news(feed_url: str):
        feed = feedparser.parse(feed_url)
        return feed.entries

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

    st.sidebar.header(" Live Deal Adjustments")
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
    st.header(" Technical Interview Question Bank")
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

st.sidebar.divider()
st.sidebar.caption(
    "📚 For deeper technical drilling beyond this app, cross-reference Rosenbaum & Pearl's "
    "*Investment Banking* and your 400 Questions IB Interview Guide."
)
