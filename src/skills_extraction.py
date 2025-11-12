# src/skills_extraction.py
import json
from rapidfuzz import process, fuzz


def load_taxonomy(path="data/job_role_taxonomy.json"):
    return json.load(open(path))


def build_skill_dict(taxonomy):
    skills = set()
    for role, cfg in taxonomy.items():
        skills |= set(cfg["must_have"]) | set(cfg.get("nice_to_have", []))
    return sorted(skills)


def extract_skills(text, skill_list, score_cutoff=75):
    words = text.split()
    hits = process.extract(
        " ".join(words),
        skill_list,
        scorer=fuzz.token_set_ratio,
        score_cutoff=score_cutoff,
    )
    return sorted({skill for skill, score, _ in hits})
