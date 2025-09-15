# Reference to reference

1. fetch range from reference (pySAM)
2. generate (based on distribution) or load (from VCF) variants
3. apply variants to range
4. convert to appropriate format for sequencing platform modeling?

```python
# valiant -> seq_converter.py
def apply_variants(ref_seq: Seq, alt_length: int, variants: Sequence[Variant]) -> Seq
```
