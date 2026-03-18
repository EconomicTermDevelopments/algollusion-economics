# Algollusion Economics Dataset

## Dataset Description
### Summary
Synthetic 200-row dataset for `Algollusion` measurement and computational experiments.

### Supported Tasks
- Economic analysis
- Computational Economics / Industrial Organization research
- Computational economics

### Languages
- English (metadata and documentation)
- Python (code examples)

## Dataset Structure
### Data Fields
- `id`: Unique observation id
- `period`: Synthetic monthly period
- `market_concentration`: HHI-style concentration proxy
- `algorithm_adoption`: Share of pricing decisions using algorithms
- `price_sync_index`: Cross-firm price synchronization
- `demand_volatility`: Demand variance channel
- `communication_signal`: Tacit coordination signal strength
- `margin_spread`: Markup spread above competitive benchmark
- `collusion_risk_proxy`: Auxiliary risk proxy
- `algollusion_index`: Composite term index

### Data Splits
- Full dataset: 200 examples

## Dataset Creation
### Source Data
Synthetic data generated for demonstrating Algollusion applications.

### Data Generation
Channels are sampled from controlled distributions with correlated structure. The term index is computed from normalized channels and directional weights.

## Considerations
### Social Impact
Research-only synthetic data for method development and reproducibility testing.

## Additional Information
### Licensing
MIT License - free for academic and commercial use.

### Citation
@dataset{algollusion2026,
title={{Algollusion Economics Dataset}},
author={{Economic Research Collective}},
year={{2026}}
}
