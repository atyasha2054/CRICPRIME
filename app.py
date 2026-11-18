from pathlib import Path
import html
import pandas as pd
import streamlit as st

# --------------------------- CONFIG ---------------------------
ROOT = Path(__file__).resolve().parent
OUT = ROOT / "outputs"

st.set_page_config(
    page_title="CricPrime | Pressure Performance",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --------------------------- DESIGN ---------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500;600;700&display=swap');

:root {
  --forest:#173c35; --forest2:#24574d; --paper:#f4efe5; --paper2:#ebe4d7;
  --ink:#202c29; --muted:#718079; --line:#d8d1c4; --orange:#d66b43;
  --gold:#d6b56d; --white:#fffdf8; --mint:#c9ded1;
}
.stApp {
  background:
    radial-gradient(ellipse at 8% 0%,rgba(214,107,67,.08),transparent 28%),
    linear-gradient(180deg,#f7f3eb 0%,#eee8dc 100%);
  color:var(--ink); font-family:'IBM Plex Sans',sans-serif;
}
.block-container {max-width:1320px;padding-top:1.3rem;padding-bottom:3.5rem}
h1,h2,h3,h4 {font-family:'DM Serif Display',serif!important;color:var(--forest)!important}
p,li,label,div {font-family:'IBM Plex Sans',sans-serif}
[data-testid="stHeader"] {background:rgba(247,243,235,.9)}
[data-testid="stCaptionContainer"] {color:var(--muted)}
.mast {
  background:var(--forest); color:var(--white); border-radius:5px;
  padding:32px 38px 28px; margin-bottom:25px; position:relative; overflow:hidden;
  border-bottom:6px solid var(--orange); box-shadow:0 12px 28px rgba(23,60,53,.12);
}
.mast:after {content:"T20 / T20I";position:absolute;right:30px;bottom:17px;color:#ffffff20;
  font:500 15px 'IBM Plex Mono',monospace;letter-spacing:2px}
.kicker {font:500 10px 'IBM Plex Mono',monospace;color:#e6b978;letter-spacing:2px;text-transform:uppercase}
.brand {font:400 clamp(42px,5vw,62px) 'DM Serif Display',serif;color:#fffdf8;line-height:1.02;margin-top:9px;letter-spacing:.2px}
.mastcopy {color:#d6e1d9;font-size:14px;line-height:1.75;max-width:700px;margin-top:12px}
.pill {display:inline-block;margin-top:17px;padding:6px 10px;border:1px solid #d6b56d80;
  color:#edc98e;font:500 9px 'IBM Plex Mono',monospace;letter-spacing:1.2px;text-transform:uppercase}
.eyebrow {font:500 10px 'IBM Plex Mono',monospace;color:var(--orange);letter-spacing:1.7px;text-transform:uppercase;margin-bottom:6px}
.section-title {font:400 30px 'DM Serif Display',serif;color:var(--forest);letter-spacing:.1px}
.section-copy {font-size:13px;color:var(--muted);line-height:1.7;margin-bottom:19px;max-width:850px}
div[data-testid="stMetric"] {background:var(--white);border:0;border-top:3px solid var(--forest);
  border-radius:3px;padding:15px 17px;box-shadow:0 5px 16px rgba(35,48,42,.045)}
[data-testid="stMetricLabel"] {color:#7b877f!important;font:500 10px 'IBM Plex Mono',monospace;text-transform:uppercase;letter-spacing:.4px}
[data-testid="stMetricValue"] {color:var(--forest)!important;font:600 25px 'IBM Plex Sans',sans-serif}
[data-testid="stMetricDelta"] {font-size:10px}
[data-testid="stTabs"] [role="tablist"] {gap:3px;border-bottom:1px solid var(--line)}
[data-testid="stTabs"] button {color:#718079;font:600 12px 'IBM Plex Sans',sans-serif;padding:11px 17px;border-radius:3px 3px 0 0}
[data-testid="stTabs"] button[aria-selected="true"] {color:var(--forest)!important;background:#e3e9df;border-bottom:3px solid var(--orange)!important}
div[data-baseweb="select"]>div {background:var(--white)!important;border:1px solid var(--line)!important;border-radius:3px!important}
/* Radio button labels: Batters and Bowlers */
[data-testid="stRadio"] label,
[data-testid="stRadio"] label p,
[data-testid="stRadio"] label span {
    color: #202c29 !important;
    font-weight: 600 !important;
}

/* Evidence standard label */
[data-testid="stSelectbox"] label,
[data-testid="stSelectbox"] label p,
[data-testid="stSelectbox"] label span {
    color: #202c29 !important;
    font-weight: 600 !important;
}

/* Selected dropdown value: Current, Relaxed, Strict */
[data-testid="stSelectbox"] div[data-baseweb="select"] *,
div[data-baseweb="select"] [role="combobox"] {
    color: #202c29 !important;
}

/* Dropdown menu options */
[role="listbox"] [role="option"] {
    color: #202c29 !important;
    background-color: #fffdf8 !important;
}
.rankhead,.rankrow {display:grid;grid-template-columns:48px minmax(130px,1.8fr) repeat(3,minmax(85px,.8fr));gap:12px;align-items:center}
.rankhead {padding:0 14px 8px;color:#8b948d;font:500 9px 'IBM Plex Mono',monospace;letter-spacing:.7px;text-transform:uppercase}
.rankrow {background:rgba(255,253,248,.88);border:1px solid var(--line);border-left:3px solid transparent;
  border-radius:3px;padding:12px 14px;margin-bottom:6px;box-shadow:0 2px 7px rgba(25,45,38,.025)}
.rankrow.first {background:#e5ede3;border-left-color:var(--orange);border-color:#cbd8cc}
.rankno {font:500 17px 'IBM Plex Mono',monospace;color:#9aa39b}
.rankno.one {color:var(--orange)}
.playername {font:600 14px 'IBM Plex Sans',sans-serif;color:var(--forest)}
.playerid {font:9px 'IBM Plex Mono',monospace;color:#9aa39b;margin-top:4px}
.statlabel {font:500 9px 'IBM Plex Mono',monospace;color:#8b948d;text-transform:uppercase;letter-spacing:.5px}
.statvalue {font:500 12px 'IBM Plex Mono',monospace;color:#314b42;margin-top:4px}
.lift {color:#b65b39}
.panel {background:var(--forest);color:white;border-radius:3px;padding:19px 22px;margin:12px 0;border-left:5px solid var(--gold)}
.panel .pk {color:#e8bd7a;font:500 9px 'IBM Plex Mono',monospace;letter-spacing:1.4px}
.panel .pt {font:400 21px 'DM Serif Display',serif;color:white;margin:7px 0}
.panel .pc {font-size:12px;color:#d4e0d8;line-height:1.75}
.method {background:var(--white);border:1px solid var(--line);border-radius:3px;padding:18px 20px;margin-bottom:10px}
.mi {font:500 9px 'IBM Plex Mono',monospace;letter-spacing:1px;color:var(--orange);margin-bottom:7px}
.mt {font:400 19px 'DM Serif Display',serif;color:var(--forest);margin-bottom:6px}
.mc {font-size:12px;color:#68776f;line-height:1.75}
.formula {background:#203e37;color:#f2f0e8;border-left:4px solid var(--gold);border-radius:2px;padding:13px 16px;margin:10px 0;font:11px/1.9 'IBM Plex Mono',monospace;overflow-x:auto}
.note {background:#f8eadb;border:1px solid #e8cbb0;color:#78523b;border-radius:3px;padding:13px 15px;font-size:12px;line-height:1.7;margin:10px 0}

/* Methodology experience */
.method-intro {
  background: linear-gradient(125deg,#173c35 0%,#28584d 100%);
  color:#fffdf8; padding:25px 28px; border-radius:5px;
  border-left:6px solid var(--gold); margin:10px 0 20px;
}
.method-intro .intro-kicker {font:500 9px 'IBM Plex Mono',monospace;color:#e8bd7a;letter-spacing:1.6px;text-transform:uppercase}
.method-intro .intro-title {font:400 27px 'DM Serif Display',serif;color:#fffdf8;margin:7px 0}
.method-intro .intro-copy {font-size:12px;line-height:1.8;color:#d7e3dc;max-width:900px}
.method-stat {
  background:#fffdf8;border:1px solid var(--line);border-top:3px solid var(--forest);
  padding:14px 16px;border-radius:3px;min-height:94px;
}
.method-stat .ms-label {font:500 9px 'IBM Plex Mono',monospace;color:#89948c;text-transform:uppercase;letter-spacing:.7px}
.method-stat .ms-value {font:400 21px 'DM Serif Display',serif;color:var(--forest);margin-top:5px}
.method-stat .ms-note {font-size:10px;color:#718079;margin-top:3px}
.method-section-label {font:500 9px 'IBM Plex Mono',monospace;color:var(--orange);letter-spacing:1.5px;text-transform:uppercase;margin:22px 0 8px}
.method-step {
  background:#fffdf8;border:1px solid var(--line);border-radius:3px;
  padding:16px 18px;height:100%;min-height:125px;
}
.method-step .step-no {font:500 9px 'IBM Plex Mono',monospace;color:var(--orange);letter-spacing:1px}
.method-step .step-title {font:400 17px 'DM Serif Display',serif;color:var(--forest);margin:6px 0}
.method-step .step-copy {font-size:11px;line-height:1.65;color:#718079}
.method-block {
  background:#fffdf8;border:1px solid var(--line);border-radius:3px;
  padding:17px 19px;margin:9px 0 12px;
}
.method-block h4 {font:400 19px 'DM Serif Display',serif;color:var(--forest);margin:0 0 7px}
.method-block p,.method-block li {font-size:12px;line-height:1.75;color:#65746c}
.method-block ul {padding-left:19px;margin:7px 0}
.method-block .formula {margin:12px 0}
.method-callout {
  background:#f8eadb;border:1px solid #e8cbb0;border-left:4px solid var(--orange);
  color:#78523b;border-radius:3px;padding:13px 16px;font-size:11px;line-height:1.75;margin:12px 0;
}
div[data-testid="stExpander"] {
  background:rgba(255,253,248,.72);border:1px solid var(--line);
  border-radius:4px;margin:7px 0;
}
div[data-testid="stExpander"] details summary {
  padding:10px 13px;color:var(--forest);font-weight:600;
}
div[data-testid="stExpander"] details summary:hover {color:var(--orange)}
.method-endnote {
  background:#e5ede3;border:1px solid #cbd8cc;border-radius:3px;
  padding:16px 19px;color:#365449;font-size:12px;line-height:1.8;margin-top:18px;
}

.footer {border-top:1px solid var(--line);margin-top:38px;padding-top:17px;text-align:center;color:#8a948c;font:10px 'IBM Plex Mono',monospace;letter-spacing:.4px}
.stButton button,.stDownloadButton button {border-radius:3px;font-weight:600}
@media(max-width:760px) {
 .rankhead,.rankrow {grid-template-columns:32px minmax(100px,1fr) minmax(72px,.8fr);gap:6px;padding-left:8px;padding-right:8px}
 .hide-mobile {display:none}.mast{padding:25px 21px}.mast:after{font-size:10px;right:12px}
}
</style>
""", unsafe_allow_html=True)

# --------------------------- HELPERS ---------------------------
def load_csv(name):
    path = OUT / name
    if not path.exists():
        return pd.DataFrame()
    try:
        return pd.read_csv(path)
    except Exception as exc:
        st.error(f"Unable to read {name}: {exc}")
        return pd.DataFrame()

def number(v, digits=2):
    try:
        return "—" if pd.isna(v) else f"{float(v):,.{digits}f}"
    except (TypeError, ValueError):
        return "—"

def integer(v):
    try:
        return "—" if pd.isna(v) else f"{int(float(v)):,}"
    except (TypeError, ValueError):
        return "—"

def lift_value(row):
    if "eb_lift" in row.index and pd.notna(row["eb_lift"]):
        return row["eb_lift"]
    return row.get("raw_lift", float("nan"))

def heading(kicker, title, copy):
    st.markdown(f'<div class="eyebrow">{kicker}</div><div class="section-title">{title}</div><div class="section-copy">{copy}</div>', unsafe_allow_html=True)

def player_row(row, fallback_rank):
    rank = int(row.get("rank", fallback_rank))
    name = html.escape(str(row.get("player_name", "Unknown player")))
    pid = html.escape(str(row.get("player_id", "—")))
    prob = row.get("bootstrap_prob_positive", float("nan"))
    try:
        prob = number(float(prob) * 100, 0) + "%"
    except (TypeError, ValueError):
        prob = "—"
    st.markdown(f"""
    <div class="rankrow {'first' if rank == 1 else ''}">
      <div class="rankno {'one' if rank == 1 else ''}">{rank:02d}</div>
      <div><div class="playername">{name}</div><div class="playerid">PLAYER REF · {pid}</div></div>
      <div><div class="statlabel">EB pressure lift</div><div class="statvalue lift">{number(lift_value(row))}</div></div>
      <div class="hide-mobile"><div class="statlabel">Pressure matches</div><div class="statvalue">{integer(row.get('pressure_matches'))}</div></div>
      <div class="hide-mobile"><div class="statlabel">P(positive lift)</div><div class="statvalue">{prob}</div></div>
    </div>""", unsafe_allow_html=True)

# --------------------------- HERO ---------------------------
st.markdown("""
<div class="mast">
  <div class="kicker">THE CRICKET PERFORMANCE REVIEW  /  VOL. 2022—26</div>
  <div class="brand">CricPrime<span style="color:#d7f36a">.</span></div>
  <div class="mastcopy">A data-led look at the players who hold their value when the game tightens. Explore pressure-adjusted batting and bowling performance through match context, expected output and statistical evidence.</div>
  <div class="pill">THE PRESSURE INDEX  ·  PLAYER EDITION</div>
</div>
""", unsafe_allow_html=True)

rank_tab, threshold_tab, method_tab = st.tabs(["🏆  Player rankings", "📈  Threshold study", "📚  Methodology"])

# ============================================================
# PLAYER RANKINGS
# ============================================================
with rank_tab:
    heading("THE PERFORMANCE BOARD", "The pressure ledger",
            "Explore the Top 10 batters and bowlers. Rankings compare performance against expected output in pressure and normal situations.")
    a, b = st.columns(2)
    with a:
        role_label = st.radio("Player role", ["Batters", "Bowlers"], horizontal=True)
    with b:
        threshold_label = st.selectbox("Evidence standard", ["Current", "Relaxed", "Strict"], index=0)
    role, threshold = role_label.lower(), threshold_label.lower()
    ranking = load_csv(f"top10_{role}_{threshold}.csv")
    if ranking.empty:
        st.warning(f"No ranking data found. Expected: outputs/top10_{role}_{threshold}.csv")
    else:
        if "rank" in ranking.columns:
            ranking = ranking.sort_values("rank")
        top = ranking.iloc[0]
        avg_matches = ranking["pressure_matches"].mean() if "pressure_matches" in ranking else float("nan")
        k1,k2,k3,k4 = st.columns(4)
        k1.metric("Players displayed", len(ranking))
        k2.metric("Leading player", str(top.get("player_name", "—")))
        k3.metric("Leading EB lift", number(lift_value(top)))
        k4.metric("Avg. pressure matches", number(avg_matches, 1))
        st.markdown("""
        <div class="panel"><div class="pk">HOW TO READ THE BOARD</div>
        <div class="pt">Pressure lift is the key signal</div>
        <div class="pc">A positive lift means the player's expected-performance residual rate was higher in pressure situations than in normal situations. EB lift is adjusted towards the population average to reduce unstable estimates from smaller samples.</div></div>
        """, unsafe_allow_html=True)
        st.markdown("""<div class="rankhead"><div>Rank</div><div>Player</div><div>EB lift</div><div class="hide-mobile">Pressure matches</div><div class="hide-mobile">P(positive lift)</div></div>""", unsafe_allow_html=True)
        for i, (_, row) in enumerate(ranking.iterrows(), 1):
            player_row(row, i)
        with st.expander("Inspect detailed player statistics"):
            cols = ["rank","player_id","player_name","pressure_matches","normal_matches","pressure_balls","normal_balls","pressure_rate","normal_rate","raw_lift","eb_lift","bootstrap_prob_positive","bootstrap_ci_low","bootstrap_ci_high"]
            cols = [c for c in cols if c in ranking.columns]
            st.dataframe(ranking[cols], use_container_width=True, hide_index=True)
        st.caption("Bootstrap probability is the fraction of bootstrap estimates above zero. It is an uncertainty indicator, not a guarantee of future performance.")

# ============================================================
# THRESHOLD ROBUSTNESS
# ============================================================
with threshold_tab:
    heading("EVIDENCE & ROBUSTNESS", "A test of ranking consistency",
            "The leaderboard is recalculated under three minimum-evidence standards to show how player selection changes as sample requirements become more demanding.")
    sensitivity = load_csv("threshold_sensitivity.csv")
    if sensitivity.empty:
        st.info("No threshold_sensitivity.csv found. Run the ranking phase first.")
    else:
        for role_name in ["batters", "bowlers"]:
            subset = sensitivity[sensitivity["role"].astype(str).str.lower() == role_name]
            if subset.empty:
                continue
            st.markdown(f"### {role_name.title()}")
            cols = st.columns(3)
            for col, level in zip(cols, ["relaxed", "current", "strict"]):
                rec = subset[subset["threshold"].astype(str).str.lower() == level]
                if not rec.empty:
                    r = rec.iloc[0]
                    with col:
                        st.metric(level.title(), f"{int(r.get('top10_count',0))}/10",
                                  f"{int(r.get('overlap_with_current',0))} overlap with Current")
        st.markdown("#### Full sensitivity table")
        st.dataframe(sensitivity, use_container_width=True, hide_index=True)

    st.markdown("### Three evidence standards")
    c1,c2,c3 = st.columns(3)
    cards = [
        ("STANDARD 01","Relaxed · Wider discovery","At least 5 pressure matches, 5 normal matches, 40 pressure balls and 75 normal balls. It explores a broader pool, but includes more uncertain estimates."),
        ("STANDARD 02","Current · Main comparison","At least 8 pressure matches, 8 normal matches, 60 pressure balls and 100 normal balls. It is the primary balance between player coverage and evidence."),
        ("STANDARD 03","Strict · Higher exposure","At least 12 pressure matches, 12 normal matches, 100 pressure balls and 150 normal balls. It tests whether the shortlist persists with greater accumulated evidence."),
    ]
    for col, (idx,title,copy) in zip([c1,c2,c3], cards):
        with col:
            st.markdown(f'<div class="method"><div class="mi">{idx}</div><div class="mt">{title}</div><div class="mc">{copy}</div></div>', unsafe_allow_html=True)
    st.markdown("""<div class="note">These cut-offs are heuristic eligibility rules, not statistically optimized thresholds. Their purpose is to expose the trade-off between coverage and sample reliability. Use the sensitivity table to discuss ranking stability, not to claim that one threshold is universally optimal.</div>""", unsafe_allow_html=True)

# ============================================================
# METHODOLOGY — FRESH METHODOLOGY PDF
# ============================================================
with method_tab:
    heading(
        "THE CRICPRIME PLAYBOOK",
        "Understand the pressure model",
        "A guided tour of the data, match-state signals, player-specific pressure, "
        "and the statistical checks behind the leaderboard."
    )

    st.markdown("""
    <div class="method-intro">
      <div class="intro-kicker">THE IDEA IN ONE MINUTE</div>
      <div class="intro-title">Pressure is the situation. Performance is the response.</div>
      <div class="intro-copy">
        A run scored in a comfortable game state is not necessarily equivalent to
        a run scored when the required rate is climbing and wickets are falling.
        CricPrime estimates the expected output for each delivery context, compares
        actual output with that expectation, and studies whether a player performs
        relatively better in pressure situations than in normal situations.
        The model measures observable match demands—not a player's private
        psychological state.
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Quick orientation: compact summary cards make the section easier to scan.
    q1, q2, q3, q4 = st.columns(4)
    quick_stats = [
        ("COVERAGE", "2022–2026", "T20 and T20I"),
        ("UNIT OF ANALYSIS", "Delivery", "State measured before the ball"),
        ("PRESSURE ENGINE", "5 signals", "Combined into HDPI"),
        ("PLAYER OUTPUT", "BPI / BoPI", "Separate batter and bowler indices"),
    ]
    for col, (label, value, note) in zip([q1, q2, q3, q4], quick_stats):
        with col:
            st.markdown(
                f'<div class="method-stat"><div class="ms-label">{label}</div>'
                f'<div class="ms-value">{value}</div><div class="ms-note">{note}</div></div>',
                unsafe_allow_html=True
            )

    st.markdown('<div class="method-section-label">THE MODEL JOURNEY</div>', unsafe_allow_html=True)
    journey = [
        ("01", "Prepare the data", "Clean deliveries, match metadata, innings limits and team results."),
        ("02", "Rebuild the situation", "Create a pre-delivery snapshot of score, wickets, balls and target."),
        ("03", "Estimate expectations", "Predict expected runs and wicket probability from match context."),
        ("04", "Measure pressure", "Combine match difficulty, WPL proxy, resources, stress and phase."),
        ("05", "Compare performance", "Calculate residuals, pressure lift and uncertainty-adjusted rankings."),
    ]
    cols = st.columns(5)
    for col, (n, title, copy) in zip(cols, journey):
        with col:
            st.markdown(
                f'<div class="method-step"><div class="step-no">STEP {n}</div>'
                f'<div class="step-title">{title}</div><div class="step-copy">{copy}</div></div>',
                unsafe_allow_html=True
            )

    st.markdown('<div class="method-section-label">EXPLORE THE DETAILS</div>', unsafe_allow_html=True)
    st.caption("Open a chapter when you want the definitions, formulas and implementation notes.")

    with st.expander("01  ·  Data foundation and delivery accounting", expanded=False):
        st.markdown("""
        <div class="method-block">
          <h4>What goes into the analysis?</h4>
          <p>The framework uses ball-by-ball data with match and competition metadata
          for T20 and T20I matches from 2022–2026.</p>
          <ul>
            <li>Innings 1 and 2 are retained; innings 3 and later, including Super Overs, are excluded.</li>
            <li>A delivery is uniquely identified by <code>(match_id, innings, innings_ball_num)</code>; duplicate keys trigger an error.</li>
            <li>The innings limit comes from the revised-overs field, with 120 balls as fallback.</li>
            <li>Wides and <code>Overstep</code> are treated as non-legal deliveries. The methodology interprets <code>Overstep</code> as a no-ball; verify this against the source data dictionary.</li>
            <li>Batter balls faced exclude wides and include no-balls. Bowler exposure uses legal balls only.</li>
            <li>Bowler-credited wickets are Caught, Bowled, LBW, Stump and Hit Wicket. Run-outs are not credited to the bowler.</li>
          </ul>
          <div class="formula">Team runs = Batter runs + extras1_runs + extras_2_runs<br>
          Bowler runs conceded = Batter runs + wide/no-ball extras</div>
        </div>
        """, unsafe_allow_html=True)

    with st.expander("02  ·  Reconstructing the match before each delivery", expanded=False):
        st.markdown("""
        <div class="method-block">
          <h4>The pre-delivery snapshot</h4>
          <p>For each delivery, the state is reconstructed immediately before the ball:
          score, wickets lost and remaining, legal balls bowled, balls remaining,
          innings limit, phase, target, runs required, required run rate and current
          run rate. The current delivery outcome is excluded from its own state.</p>
          <div class="formula">RunsRequired = max(Target − ScoreBefore, 0)<br>
          RRR = 6 × RunsRequired / BallsRemaining<br>
          CRR = 6 × ScoreBefore / LegalBallsBefore</div>
          <p>RRR is undefined when no balls remain; CRR is undefined before the first
          legal ball. The pipeline uses safe downstream handling.</p>
        </div>
        """, unsafe_allow_html=True)

    with st.expander("03  ·  Chronological modelling and expected performance", expanded=False):
        st.markdown("""
        <div class="method-block">
          <h4>Keep the future out of the past</h4>
          <p>Expanding chronological folds are used. In the earliest season, the first
          25% of distinct match dates are a warm-up period and later dates are scored.
          For each subsequent season, training uses only earlier seasons. Training and
          scored match IDs must not overlap. This reduces future-information leakage,
          although feature definitions, joins and labels still require audit.</p>
          <h4>Expected-output models</h4>
          <ul>
            <li><b>Expected batter runs:</b> <code>HistGradientBoostingRegressor</code>, predictions clipped to 0–6.</li>
            <li><b>Expected bowler runs conceded:</b> <code>HistGradientBoostingRegressor</code>, predictions clipped to 0–10.</li>
            <li><b>Credited wicket probability:</b> <code>HistGradientBoostingClassifier</code>.</li>
          </ul>
          <h4>Win-probability model used by the Fresh approach</h4>
          <p>Standardized <code>LogisticRegression</code> (<code>C=0.5</code>,
          <code>max_iter=500</code>, <code>class_weight='balanced'</code>) estimates
          whether the batting team wins. Ties, no-results and abandoned matches are
          excluded from winner-label training.</p>
          <p>Features include innings, score, wickets before and remaining, legal balls
          before, balls remaining, innings limit, runs required, RRR, CRR and format code.
          Player identifiers and the current delivery outcome are not model features.</p>
        </div>
        """, unsafe_allow_html=True)

    with st.expander("04  ·  The five components of match pressure", expanded=True):
        st.markdown("""
        <div class="method-block">
          <h4>Match-State Difficulty (MSD)</h4>
          <p>MSD measures how demanding the current match state is. The chase and
          first-innings calculations differ.</p>
          <b>Chase MSD</b>
          <div class="formula">RRRStress = clip((RRR − CRR) / 8, 0, 1)<br>
          WicketStress = clip((10 − WicketsRemaining) / 10, 0, 1)<sup>1.5</sup><br>
          MSD_chase = 0.60 × RRRStress + 0.40 × WicketStress</div>
          <p>RRR stress rises when the required scoring rate exceeds the current rate.
          Wicket stress rises non-linearly as wickets are lost.</p>
          <b>First-innings MSD</b>
          <div class="formula">FirstParStress = clip(ParScoreDeficit / 18, 0, 1)<br>
          MSD_first = 0.65 × FirstParStress + 0.35 × WicketStress</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="method-block">
          <h4>Win-Probability Leverage (WPL proxy)</h4>
          <p>The Fresh approach uses a state-sensitivity proxy. It emphasizes uncertain
          match states and increases the proxy when match-state difficulty or resource
          scarcity is high.</p>
          <div class="formula">WPL_proxy = 4 × WP × (1 − WP) × max(MSD, 0.35 × RSI)</div>
          <ul>
            <li><code>WP</code> is predicted batting-team win probability before the delivery.</li>
            <li><code>4 × WP × (1 − WP)</code> is largest at WP = 0.5 and smaller near 0 or 1.</li>
            <li><code>MSD</code> is match-state difficulty; <code>RSI</code> is resource scarcity.</li>
          </ul>
          <div class="method-callout"><b>Interpretation note:</b> This is a proxy, not the expected absolute
          win-probability movement over all possible next-ball outcomes. It should not
          be presented as full outcome-based WPL.</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="method-block">
          <h4>Resource Scarcity Index (RSI)</h4>
          <p>RSI measures how much batting resource has been consumed. It rises as
          balls and wickets are used.</p>
          <div class="formula">RSI = 1 − [(BallsRemaining / InningsBallLimit) × (WicketsRemaining / 10)]</div>
          <p>This is a compact resource-scarcity proxy, not a full
          Duckworth–Lewis-style resource model.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="method-block">
          <h4>Situational Stress Index (SSI)</h4>
          <div class="formula">SSI = 0.35 × CollapseStress + 0.30 × RecoveryRequirement<br>
          + 0.20 × PartnershipDependency + 0.15 × CriticalOverFlag<br><br>
          CollapseStress = clip(WicketsLast12 / 3, 0, 1)<br>
          PartnershipDependency = clip(WicketsBefore / 9, 0, 1)</div>
          <p><code>WicketsLast12</code> counts wickets in the previous 12 legal balls,
          excluding the current delivery. Recovery requirement is RRR/18 for a chase
          and ParScoreDeficit/18 in the first innings, clipped to [0,1].
          CriticalOverFlag is 1 in the death phase and 0 otherwise.</p>
          <h4>Phase &amp; Execution Pressure (PEP)</h4>
          <div class="formula">PEP = PhaseFraction × max(MSD, 0.5 × RSI)<br>
          PhaseFraction = LegalBallsBefore / InningsBallLimit</div>
          <p>Phase progression amplifies existing match/resource stress; death overs
          are not automatically assigned maximum pressure.</p>
        </div>
        """, unsafe_allow_html=True)

    with st.expander("05  ·  First-innings par-score proxy", expanded=False):
        st.markdown("""
        <div class="method-block">
          <h4>How the first-innings reference is formed</h4>
          <p>The Fresh version calculates the mean completed first-innings total by
          format and season, multiplies it by the current phase fraction, and compares
          that proxy par with the actual score before the delivery.</p>
          <div class="formula">SeasonPar = mean(CompletedFirstInningsTotal | Format, Season)<br>
          ProxyParScore = SeasonPar × PhaseFraction<br>
          ParScoreDeficit = max(ProxyParScore − ScoreBefore, 0)</div>
          <p>This proxy does not condition expected score on wickets lost or exact ball
          position beyond phase fraction. It uses a season-level average and is not a
          full chronological, state-conditioned par model.</p>
        </div>
        """, unsafe_allow_html=True)

    with st.expander("06  ·  Combined pressure score and pressure bands", expanded=False):
        st.markdown("""
        <div class="method-block">
          <h4>Hybrid Dynamic Pressure Intelligence (HDPI)</h4>
          <p>The five dimensions are combined on a 0–1 scale and multiplied by 100.</p>
          <div class="formula">HDPI = 100 × (0.25×MSD + 0.30×WPLproxy + 0.20×RSI<br>
          + 0.15×SSI + 0.10×PEP)</div>
        </div>
        """, unsafe_allow_html=True)
        st.dataframe(
            pd.DataFrame(
                [["Routine", "0–40"], ["Elevated", "40–60"], ["High", "60–75"],
                 ["Severe", "75–90"], ["Critical", "90–100"]],
                columns=["Pressure band", "HDPI score"]
            ),
            use_container_width=True, hide_index=True
        )
        st.caption("The general HDPI pressure flag is score ≥ 60. Component weights are fixed design assumptions, not formally optimized weights.")

    with st.expander("07  ·  Role-specific pressure: BPI and BoPI", expanded=False):
        st.markdown("""
        <div class="method-block">
          <h4>Batter Pressure Intelligence (BPI)</h4>
          <div class="formula">BPI = 100 × (0.35×HDPI/100 + 0.25×BatterUrgency<br>
          + 0.20×DismissalRisk + 0.20×BatterResponsibility)</div>
          <p>Batter urgency is RRR/18 for a chase; in the first innings it combines
          phase fraction (55%) and par deficit/30 (45%). Dismissal risk combines a
          low-wickets indicator (60%) and partnership dependency (40%). Batter
          responsibility combines partnership dependency (60%) and recent collapse
          stress (40%). BPI pressure is BPI ≥ 60.</p>
          <h4>Bowler Pressure Intelligence (BoPI)</h4>
          <div class="formula">BoPI = 100 × (0.35×HDPI/100 + 0.25×BowlerDefenceUrgency<br>
          + 0.20×WicketThreat + 0.20×BowlerResponsibility)</div>
          <p>Bowler defence urgency is RRR/18 for a chase; in the first innings it
          combines phase fraction (60%) and par deficit/30 (40%). Wicket threat
          combines wickets already lost/8 (50%) and recent wickets in the previous
          12 legal balls (50%). Bowler responsibility combines defence urgency (60%)
          and death-phase flag (40%). BoPI pressure is BoPI ≥ 60.</p>
        </div>
        """, unsafe_allow_html=True)

    with st.expander("08  ·  From expected performance to pressure lift", expanded=False):
        st.markdown("""
        <div class="method-block">
          <h4>Residuals: actual output minus expectation</h4>
          <p>Expected-performance models estimate typical delivery output in a given
          pre-delivery context. Residuals compare actual output with expectation.</p>
          <div class="formula">BatterResidual = ActualBatterRuns − ExpectedBatterRuns<br>
          BowlerResidual = ExpectedBowlerRunsConceded − ActualBowlerRunsConceded<br><br>
          WeightedBatterResidual = BatterResidual × (BPI/100)<sup>1.5</sup><br>
          WeightedBowlerResidual = BowlerResidual × (BoPI/100)<sup>1.5</sup></div>
          <p>Positive residuals are favorable for both roles. Exposure is batter balls
          faced for batters and legal balls bowled for bowlers. Rates are calculated
          per 100 exposure balls.</p>
          <div class="formula">PressureRate = 100 × Σ(WeightedResidual_pressure) / PressureExposure<br>
          NormalRate = 100 × Σ(WeightedResidual_normal) / NormalExposure<br>
          RawLift = PressureRate − NormalRate</div>
          <p>Credited wicket probability residual is retained as a separate supporting
          signal; it is not converted into run value.</p>
        </div>
        """, unsafe_allow_html=True)

    with st.expander("09  ·  Reliability: shrinkage, bootstrap and eligibility", expanded=False):
        st.markdown("""
        <div class="method-block">
          <h4>Empirical-Bayes shrinkage</h4>
          <p>Shrinkage reduces extreme estimates from smaller or noisier samples by
          pulling them towards a zero prior mean.</p>
          <div class="formula">EBLift = RawLift × τ² / (τ² + SE²)</div>
          <p><code>τ²</code> is estimated between-player variance. <code>SE²</code> is
          an implementation sampling-variance proxy based on player-match residual
          variation and exposure; it is an empirical shrinkage approximation, not a
          fully specified hierarchical likelihood.</p>
          <h4>Match-cluster bootstrap</h4>
          <p>Player match-state clusters are resampled separately for pressure and
          normal states. The pressure-minus-normal difference is recalculated, then
          the fraction of estimates above zero and the percentile interval are reported.</p>
          <div class="method-callout">The methodology PDF records 120 bootstrap draws in the first package
          and 40 screening draws in the WPL-upgrade package, and recommends at least
          1,000 draws for final reporting. Confirm the draw count in the exact code run.</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("**Minimum evidence required for eligibility**")
        st.dataframe(
            pd.DataFrame([
                ["Relaxed", 5, 5, 40, 75],
                ["Current", 8, 8, 60, 100],
                ["Strict", 12, 12, 100, 150],
            ], columns=["Standard", "Pressure matches", "Normal matches",
                        "Pressure balls", "Normal balls"]),
            use_container_width=True, hide_index=True
        )
        st.markdown("""
        <div class="method-block">
          <p><b>How the standards differ:</b> Relaxed increases player coverage;
          Current is the primary balance between coverage and evidence; Strict tests
          the shortlist among players with greater accumulated exposure. These are
          heuristic starting choices, not statistically optimized cut-offs.</p>
          <p>Eligible players are ordered by EB lift, then bootstrap probability
          positive, lower confidence bound, raw lift and pressure-match count.</p>
        </div>
        """, unsafe_allow_html=True)

    with st.expander("10  ·  Limitations and responsible interpretation", expanded=False):
        st.markdown("""
        <div class="method-block">
          <h4>What the model can—and cannot—claim</h4>
          <ul>
            <li>Pressure is a modelled situational-demand construct, not a direct psychological measurement.</li>
            <li>Component weights and eligibility thresholds are design hypotheses requiring ablation, sensitivity analysis and review.</li>
            <li>Fresh WPL and first-innings par are proxies; do not describe them as full outcome-based leverage or state-conditioned par.</li>
            <li>Predictions depend on the correctness of extras, wicket, target, revised-overs and match-winner fields.</li>
            <li>T20 and T20I formats may differ; combined rankings should be accompanied by format-specific robustness checks.</li>
            <li>Bootstrap intervals at low draw counts are screening estimates, not definitive inferential intervals.</li>
          </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="method-endnote">
      <b>In one sentence:</b> CricPrime compares each player's actual output with
      context-aware expected output, identifies pressure using five match-state
      dimensions, separates batter and bowler demands, and uses shrinkage,
      bootstrap uncertainty and evidence thresholds to make the final shortlist
      more interpretable.
    </div>
    """, unsafe_allow_html=True)

# --------------------------- FOOTER ---------------------------
st.markdown("""
<div class="footer"><b style="color:#203852;letter-spacing:2px">CRICPRIME</b><br><br>
READ THE GAME. MEASURE THE MOMENT.<br>
CRICPRIME  /  T20 + T20I  /  2022—2026</div>
""", unsafe_allow_html=True)
