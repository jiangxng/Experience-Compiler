from __future__ import annotations
from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class ScenarioBenchmarkResult:
    scenario_id:str; passed:bool; checks:tuple[str,...]; failures:tuple[str,...]
class ManufacturingBenchmark:
    REQUIRED={"critical-material-shortage":{"decision-panel","evidence-stack","impact-preview"},
              "capacity-overload":{"decision-panel","evidence-stack","impact-preview"},
              "quality-hold":{"decision-panel","evidence-stack","impact-preview"},
              "machine-downtime-risk":{"decision-panel","evidence-stack","impact-preview"},
              "fulfillment-allocation":{"decision-panel","evidence-stack","impact-preview"}}
    def evaluate_experience(self,scenario_id,proposal):
        caps={r.capability for r in proposal.regions};req=self.REQUIRED[scenario_id]
        failures=tuple(f"missing capability {x}" for x in sorted(req-caps))
        return ScenarioBenchmarkResult(scenario_id,not failures,tuple(sorted(caps)),failures)
