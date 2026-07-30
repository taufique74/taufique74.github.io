---
title: "The transformer forward pass, one matmul at a time"
author: Taufiquzzaman Peyash
pubDatetime: 2026-07-30T00:00:00Z
description: An interactive walkthrough that computes a tiny transformer live in the browser — 21 steps from token IDs to next-word probabilities, every tensor small enough to check by hand.
draft: true
tags:
  - mech-interp
  - transformers
  - interactive
---

Every explanation of the transformer eventually collapses into a table of shapes: `[B, T, 768] @ [768, 64] → [B, T, 64]`. The table is a good reference and a bad teacher, because nothing in it moves.

So I built a version that moves: an [interactive walkthrough of the forward pass](/interactive/transformer-forward-pass.html) — 21 steps from token IDs to next-word probabilities, played on a zoomable architecture diagram. Each step shows the calculation, the tensors going in and out, and the shape transformation, with a caption explaining what the step is actually for.

The usual way to show tensor internals is GPT-2's real dimensions with the values elided: 768-wide matrices and a lot of ellipses. This goes the other way. The model is a toy small enough to show every number: three tokens ("The cat sat"), `d_model = 4`, two heads with `d_head = 2`, an 8-word vocabulary. The forward pass runs live in the browser from hand-picked weights, so every cell on screen is a computed value, not an illustration. Each tensor carries both shape labels (toy `[3, 4]`, GPT-2 `[T, 768]`), so the arithmetic stays checkable while the dimensions stay honest.

Two things are worth verifying with a pencil. The attention score for cat → The, which the walkthrough expands term by term: (0.17 × −0.40 + 1.09 × −0.43) / √2 = −0.38. And any row of the post-softmax attention pattern, which sums to exactly 1.00; there is a badge next to the grid doing that check in public.

The weights are hand-picked, not trained, so the final prediction is noise; the toy model "predicts" whatever its arbitrary weights happen to say. The point is watching the plumbing: where the 64 dimensions go when Q·Kᵀ collapses them into a T×T grid, why the residual stream never changes shape from embedding to unembedding, which hidden cells GELU kills and which it lets through.

<iframe src="/interactive/transformer-forward-pass.html" title="Transformer forward pass — interactive walkthrough" loading="lazy" style="width:100%;height:640px;border:1px solid var(--border,#ccc);border-radius:8px"></iframe>

Arrow keys step, space plays, the divider between the diagram and the stage drags. The embedded version is cramped — [open it full-screen](/interactive/transformer-forward-pass.html).
