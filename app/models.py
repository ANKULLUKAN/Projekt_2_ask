from dataclasses import dataclass, field
from typing import List, Optional
import statistics


@dataclass

#wyniki kazdej pojedynczej proby
class TrialResult:
    stimulus_type: str
    reaction_time_ms: Optional[float] = None
    correct: bool = False
    too_early: bool = False
    missed: bool = False
    expected_response: str = ""
    actual_response: str = ""


@dataclass
class TestSummary:

    name: str

    training_results: List[TrialResult] = field(default_factory=list)
    real_results: List[TrialResult] = field(default_factory=list)

    def valid_times(self):
        
        return [
            result.reaction_time_ms
            for result in self.real_results
            if result.correct and result.reaction_time_ms is not None
        ]

    def total_errors(self):
        return sum(
            1
            for result in self.real_results
            if (not result.correct) or result.too_early or result.missed
        )

    def stats(self):
        times = self.valid_times()

        if not times:
            return {
                "avg": 0.0,
                "min": 0.0,
                "max": 0.0,
                "median": 0.0,
                "std": 0.0,
                "count": 0,
            }

        std_val = statistics.stdev(times) if len(times) > 1 else 0.0

        return {
            "avg": statistics.mean(times),
            "min": min(times),
            "max": max(times),
            "median": statistics.median(times),
            "std": std_val,
            "count": len(times),
        }
