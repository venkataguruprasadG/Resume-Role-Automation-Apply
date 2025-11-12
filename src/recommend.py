# src/recommend.py
import json


def score_role(candidate_skills, taxonomy):
    results = []
    for role, cfg in taxonomy.items():
        must = set(cfg["must_have"])
        nice = set(cfg.get("nice_to_have", []))
        score = 0.0

        # must-have coverage (weighted higher)
        score += 2.0 * (len(must & set(candidate_skills)) / max(1, len(must)))

        # nice-to-have coverage
        score += 1.0 * (len(nice & set(candidate_skills)) / max(1, len(nice)))

        results.append({"role": role, "score": round(score, 3)})

    return sorted(results, key=lambda x: x["score"], reverse=True)


def recommend(skills, taxonomy):
    return score_role(skills, taxonomy)
