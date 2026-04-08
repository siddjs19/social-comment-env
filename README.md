# Social Comment Environment

A reinforcement learning environment simulating social media comment moderation.

## Features
- Multi-step environment (reset, step, state)
- Deterministic scenarios (easy, medium, hard)
- Reward shaping based on moderation quality
- OpenEnv compliant API

## API Endpoints
- POST /reset
- POST /step
- GET /state

## Inference
Run:
python inference.py

Outputs structured logs:
[START]
[STEP]
[END]

## Deployment
Live API:
https://warriorsid-social-comment-env.hf.space

## Tasks
- Easy: low toxicity
- Medium: mixed behavior
- Hard: high toxicity threads

---
title: Social Comment Environment
emoji: 🤖
colorFrom: blue
colorTo: green
sdk: docker
app_file: app.py
pinned: false
---