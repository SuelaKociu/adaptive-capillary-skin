#!/usr/bin/env python3
import argparse, json
from pathlib import Path
from acs.model import nominal_timeseries, monte_carlo


def main():
    parser=argparse.ArgumentParser(description="Run ACS virtual falsification model")
    parser.add_argument("--trials", type=int, default=1000)
    parser.add_argument("--output", default="reproduced_outputs")
    args=parser.parse_args()
    out=Path(args.output); data=out/"data"; data.mkdir(parents=True,exist_ok=True)

    nominal=nominal_timeseries(); nominal.to_csv(data/"nominal_timeseries.csv",index=False)
    broad=monte_carlo(args.trials,False); design=monte_carlo(args.trials,True)
    broad.to_csv(data/"monte_carlo_unoptimized.csv",index=False)
    design.to_csv(data/"monte_carlo_design_envelope.csv",index=False)
    summary={
      "status":"COMPUTATIONAL / VIRTUAL ONLY - NOT PHYSICAL EXPERIMENTS",
      "trials_per_ensemble":args.trials,
      "broad_prior_pass_rate":float(broad.pass_all.mean()),
      "design_envelope_pass_rate":float(design.pass_all.mean()),
      "falsification_gate":{
        "leak_reduction_pct_min":80,
        "isolation_time_s_max":600,
        "flow_retention_pct_min":70,
        "sensor_effect_sigma_min":5
      }
    }
    (out/"simulation_summary.json").write_text(json.dumps(summary,indent=2),encoding="utf-8")
    print(json.dumps(summary,indent=2))

if __name__ == "__main__":
    main()
