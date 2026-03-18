"""
Algollusion: computational implementation for computational economics / industrial organization analysis.

Algollusion refers to autonomous emergence of collusive pricing behavior among algorithmic agents through reinforcement learning without explicit communication. This module provides a reproducible calculator that validates the canonical channels, normalizes each series, computes a weighted index, and supports simple counterfactual policy simulation. The design is intentionally transparent so researchers can inspect how the concept moves from definition to code. Typical uses include comparative diagnostics, notebook-based scenario testing, and integration into empirical pipelines where consistent measurement matters as much as prediction.
"""
from __future__ import annotations

from typing import Optional

import numpy as np
import pandas as pd

# Algollusion channels track the observable anatomy of the canonical definition.
TERM_CHANNELS = [
    "market_concentration",  # Market concentration captures a distinct economic channel.
    "algorithm_adoption",  # Algorithm adoption captures a distinct economic channel.
    "price_sync_index",  # Price sync index captures a distinct economic channel.
    "demand_volatility",  # Demand volatility mitigates exposure when it is high.
    "communication_signal",  # Communication signal captures a distinct economic channel.
    "margin_spread",  # Margin spread captures a distinct economic channel.
    "collusion_risk_proxy",  # Collusion risk proxy captures a distinct economic channel.
]

# Weighted channels preserve the repository's existing score logic.
WEIGHTED_CHANNELS = [
    "market_concentration",
    "algorithm_adoption",
    "price_sync_index",
    "demand_volatility",
    "communication_signal",
    "margin_spread",
]

# Default weights encode the relative economic importance of each weighted channel.
DEFAULT_WEIGHTS: dict[str, float] = {
    "market_concentration": 0.2,  # Market concentration captures a distinct economic channel.
    "algorithm_adoption": 0.2,  # Algorithm adoption captures a distinct economic channel.
    "price_sync_index": 0.2,  # Price sync index captures a distinct economic channel.
    "demand_volatility": 0.12,  # Demand volatility mitigates exposure when it is high.
    "communication_signal": 0.14,  # Communication signal captures a distinct economic channel.
    "margin_spread": 0.14,  # Margin spread captures a distinct economic channel.
}


class AlgollusionCalculator:
    """
    Compute Algollusion index scores from tabular data.

    Parameters
    ----------
    weights : dict[str, float] | None
        Optional weights overriding DEFAULT_WEIGHTS. Keys must match
        WEIGHTED_CHANNELS and values must sum to 1.0.
    """

    def __init__(self, weights: Optional[dict[str, float]] = None) -> None:
        # Alternative weights are useful for robustness checks across specifications.
        self.weights = weights or DEFAULT_WEIGHTS.copy()

        # Exact key matching prevents silent omission of economically relevant channels.
        if set(self.weights) != set(WEIGHTED_CHANNELS):
            raise ValueError(f"Weights must include exactly these channels: {WEIGHTED_CHANNELS}")

        # Unit-sum weights keep the index interpretable across datasets.
        if abs(sum(self.weights.values()) - 1.0) >= 1e-6:
            raise ValueError("Weights must sum to 1.0")

    @staticmethod
    def _normalise(series: pd.Series) -> pd.Series:
        """
        Return min-max normalized values on the unit interval.
        """
        lo = float(series.min())
        hi = float(series.max())
        if hi == lo:
            # Degenerate channels should not create spurious variation.
            return pd.Series(np.zeros(len(series)), index=series.index)
        return (series - lo) / (hi - lo)

    def calculate_algollusion(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Compute normalized channels, composite scores, and qualitative bands.
        """
        # Full channel validation keeps the score tied to the canonical definition.
        missing = [channel for channel in TERM_CHANNELS if channel not in df.columns]
        if missing:
            raise ValueError(f"Missing Algollusion channels: {missing}")

        out = df.copy()
        for channel in TERM_CHANNELS:
            out[f"{channel}_norm"] = self._normalise(out[channel])

        # Positive channels intensify the mechanism while negative channels offset it.
        out["algollusion_index"] = (
            + self.weights["market_concentration"] * out["market_concentration_norm"]
            + self.weights["algorithm_adoption"] * out["algorithm_adoption_norm"]
            + self.weights["price_sync_index"] * out["price_sync_index_norm"]
            + self.weights["communication_signal"] * out["communication_signal_norm"]
            + self.weights["margin_spread"] * out["margin_spread_norm"]
            + self.weights["demand_volatility"] * (1.0 - out["demand_volatility_norm"])
        )

        # Three bands keep the metric usable in audits, papers, and dashboards.
        out["algollusion_band"] = pd.cut(
            out["algollusion_index"],
            bins=[-np.inf, 0.33, 0.66, np.inf],
            labels=["low", "moderate", "high"],
        )
        return out

    def simulate_policy(self, df: pd.DataFrame, channel: str, reduction: float = 0.2) -> pd.DataFrame:
        """
        Simulate a policy shock that reduces one observed channel.
        """
        if channel not in TERM_CHANNELS:
            raise ValueError(f"Unknown Algollusion channel: {channel}")
        if reduction < 0.0 or reduction > 1.0:
            raise ValueError("reduction must be between 0.0 and 1.0")

        # Counterfactual shocks translate reforms into score movements.
        df_policy = df.copy()
        df_policy[channel] = df_policy[channel] * (1 - reduction)
        return self.calculate_algollusion(df_policy)


if __name__ == "__main__":
    sample = pd.read_csv("algollusion_dataset.csv")
    calc = AlgollusionCalculator()
    print(calc.calculate_algollusion(sample)[["algollusion_index", "algollusion_band"]].head(10).to_string(index=False))

    scenario = calc.simulate_policy(sample, channel="market_concentration", reduction=0.15)
    print("\nPolicy Scenario Mean Index:")
    print(float(scenario["algollusion_index"].mean()))
