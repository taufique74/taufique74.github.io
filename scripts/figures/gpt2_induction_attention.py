"""Export real GPT-2 small attention patterns on a repeated-token sequence.

The classic induction test: feed `[BOS] r1 r2 ... rN r1 r2 ... rN` where r is a
random token sequence. An induction head attends from position i in the second
copy back to the token that *followed* the matching token in the first copy.
That shows up as a bright off-diagonal stripe at offset (N-1).

Output shape is deliberately small enough to ship to a browser: we keep only the
top-k heads by induction score, quantised to 3 decimals.
"""

import json
import pathlib

import torch
from transformer_lens import HookedTransformer

SEQ = 15  # tokens per copy
TOP_K = 6
OUT = (
    pathlib.Path(__file__).resolve().parents[2]
    / "src/data/figures/gpt2-induction-attention.json"
)

torch.set_grad_enabled(False)
torch.manual_seed(0)

model = HookedTransformer.from_pretrained("gpt2-small", device="cpu")
model.eval()

# Random tokens, avoiding special ids. Repeat them once.
rand = torch.randint(1000, 10000, (1, SEQ))
tokens = torch.cat([torch.tensor([[model.tokenizer.bos_token_id]]), rand, rand], dim=1)
n = tokens.shape[1]

logits, cache = model.run_with_cache(tokens, remove_batch_dim=True)

# Induction score: mean of the diagonal at offset -(SEQ-1), over the second copy.
# That diagonal is exactly "attend to the token after my previous occurrence".
scores = {}
for layer in range(model.cfg.n_layers):
    pattern = cache["pattern", layer]  # [head, query, key]
    for head in range(model.cfg.n_heads):
        diag = pattern[head].diagonal(offset=-(SEQ - 1))
        scores[(layer, head)] = diag.mean().item()

ranked = sorted(scores.items(), key=lambda kv: kv[1], reverse=True)
selected = ranked[:TOP_K]

str_tokens = model.to_str_tokens(tokens)

heads = []
for (layer, head), score in selected:
    pattern = cache["pattern", layer][head]
    heads.append(
        {
            "layer": layer,
            "head": head,
            "label": f"L{layer}H{head}",
            "inductionScore": round(score, 4),
            # round hard — 3 decimals is well below what a heatmap can show
            "values": [[round(v, 3) for v in row] for row in pattern.tolist()],
        }
    )

payload = {
    "model": "gpt2-small",
    "prompt": {
        "kind": "repeated-random",
        "seqLen": SEQ,
        "description": (
            f"{SEQ} random tokens repeated twice, prefixed with BOS. "
            f"Induction heads produce a stripe at offset {SEQ - 1}."
        ),
    },
    "tokens": str_tokens,
    "nTokens": n,
    "inductionOffset": SEQ - 1,
    "heads": heads,
    "baseline": {
        "meanInductionScore": round(
            sum(scores.values()) / len(scores), 4
        ),
        "nHeadsTotal": len(scores),
    },
}

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(payload))

print(f"wrote {OUT} ({OUT.stat().st_size / 1024:.1f} KB)")
print(f"tokens: {n}, top heads:")
for h in heads:
    print(f"  {h['label']:8s} induction={h['inductionScore']:.4f}")
print(f"mean across all {len(scores)} heads: {payload['baseline']['meanInductionScore']:.4f}")
