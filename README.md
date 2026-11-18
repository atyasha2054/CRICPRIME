# CLUTCH IQ 2.0 — Fresh self-contained implementation

This is a clean rebuild from the six competition CSVs. It has **no imports from
the old CLUTCH IQ baseline**. All Python modules required by this version live
inside `src/`.

## Folder structure

- `data/raw/`: original competition CSVs.
- `data/processed/`: derived delivery states, pressure features and OOS predictions.
- `src/engine.py`: complete phase implementation.
- `src/phase*.py`: independently runnable phase entry points.
- `outputs/`: audits, metrics, Top 10s and sensitivity reports.
- `models/`: reserved for persisted model artifacts.

## Install (Windows PowerShell)

```powershell
cd path\to\CLUTCH-IQ-2.0-FRESH
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Run in order

```powershell
python src/phase1_data_foundation.py
python src/phase2_3_models.py
python src/phase4_hybrid_pressure.py
python src/phase5_player_rankings.py
python src/phase6_validation_report.py
```

Or run all phases:

```powershell
python src/run_pipeline.py --phase all
```

Run a single phase via the engine:
```powershell
python src/engine.py --phase 1
python src/engine.py --phase 2-3
python src/engine.py --phase 4
python src/engine.py --phase 5
python src/engine.py --phase 6
```

## Methodology implemented

### Phase 1 — Data foundation
- Joins deliveries to match and competition metadata.
- Excludes innings 3+ (extra innings/Super Overs).
- Uses match innings limits; missing limits default to 120 legal balls.
- Legal delivery excludes wides and `Overstep` (treated as no-ball).
- Batter balls faced excludes wides; no-balls count as faced.
- Bowler conceded runs are batter runs plus wide/no-ball extras.
- Bowler credited wickets: Caught, Bowled, LBW, Stump, Hit Wicket.
- Constructs pre-delivery score, wickets, balls remaining, chase target and run rates.
- Keeps match-level winner label only for decisive matches.

### Phase 2/3 — Expected performance and win probability
- Expanding chronological folds: first season uses an initial warm-up block;
  later seasons train only on earlier seasons.
- No match overlap between train and scored fold.
- Estimates expected batter runs, bowler runs conceded and wicket probability.
- Estimates batting-side win probability from pre-delivery state.
- Writes metrics and out-of-sample predictions.

### Phase 4 — Hybrid pressure
- MSD: chase RRR-vs-CRR stress and wicket stress; first innings par-deficit proxy.
- RSI: remaining balls × remaining wickets resource availability.
- SSI: lagged collapse, recovery demand, partnership dependency and critical-over flag.
- PEP: phase progression gated by state severity.
- BPI and BoPI are distinct role-specific situational-demand indices.
- Current WPL is explicitly a proxy (`4*WP*(1-WP)` times state severity), **not**
  the full expected absolute WP change over all possible next-ball outcomes.
  Do not claim the complete WPL formulation is implemented yet.

### Phase 5 — Player rankings
- Batter residual = actual runs - expected runs.
- Bowler residual = expected conceded runs - actual conceded runs.
- Uses batter balls-faced exposure and bowler legal-ball exposure separately.
- Pressure/normal comparison, intensity weighting, empirical-Bayes shrinkage proxy,
  and player-match cluster bootstrap.
- Thresholds:
  - relaxed: 5 pressure / 5 normal matches; 40 / 75 balls
  - current: 8 / 8 matches; 60 / 100 balls
  - strict: 12 / 12 matches; 100 / 150 balls

## Critical research limitations to address before competition submission

This code is an end-to-end runnable research prototype, not yet a scientifically
validated final system.

1. WPL must be upgraded from the disclosed proxy to
   `E[abs(WP_after - WP_before) | pre-delivery state]`, using a next-ball outcome
   distribution estimated only from earlier matches and simulated post-outcome
   states. Never use the realised current delivery to score pressure.
2. First-innings par deficit is currently a phase/season mean proxy. Replace it
   with a chronological historical par curve conditioned on format, legal-ball
   position and wickets.
3. The situational responsibility features are observable proxies, not direct
   measurements of a player's psychological pressure.
4. Empirical-Bayes and bootstrap calculations are initial approximations. Audit
   the bootstrap design and uncertainty estimator before interpreting intervals.
5. Weight values are starting hypotheses. Run chronological ablation and weight
   sensitivity before asserting the hybrid is better than baseline.
6. Check the official source data dictionary for `extras1_runs`, `extras_2_runs`,
   `Overstep`, revised overs and dismissal semantics.
7. T20 and T20I coverage is imbalanced. Report format-specific robustness and
   do not over-generalize from the combined ranking.

## Outputs

- `outputs/phase1_audit.json`
- `outputs/model_metrics.json`
- `outputs/top10_batters_relaxed.csv`, `top10_batters_current.csv`,
  `top10_batters_strict.csv`
- `outputs/top10_bowlers_relaxed.csv`, `top10_bowlers_current.csv`,
  `top10_bowlers_strict.csv`
- `outputs/threshold_sensitivity.csv`
- `outputs/methodology_and_validation_report.json`

The model scores are out-of-sample for the scored folds. Early warm-up matches
in the first season do not receive predictions and therefore are not ranked.
