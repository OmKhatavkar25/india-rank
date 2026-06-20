"""Tests for the skill taxonomy and extraction."""

from candidate_ranker.skills import extract_skills, normalize_skill, skill_coverage


def test_normalize_known_skill() -> None:
    assert normalize_skill("Python") == "python"
    assert normalize_skill("python3") == "python"
    assert normalize_skill("Kubernetes") == "kubernetes"
    assert normalize_skill("k8s") == "kubernetes"


def test_normalize_unknown_skill() -> None:
    assert normalize_skill("non_existent_skill_xyz") is None


def test_extract_skills_basic() -> None:
    text = "I know Python, Kubernetes, and TensorFlow"
    skills = extract_skills(text)
    assert "python" in skills
    assert "kubernetes" in skills
    assert "tensorflow" in skills


def test_extract_skills_with_aliases() -> None:
    text = "Experienced with k8s, py, and tf"
    skills = extract_skills(text)
    assert "kubernetes" in skills
    assert "python" in skills
    assert "tensorflow" in skills


def test_extract_skills_empty() -> None:
    assert extract_skills("") == []
    assert extract_skills("nothing relevant here") == []


def test_skill_coverage() -> None:
    jd = {"python", "kubernetes", "docker", "aws"}
    assert skill_coverage(jd, {"python", "kubernetes"}) == 0.5
    assert skill_coverage(jd, {"python", "kubernetes", "docker", "aws"}) == 1.0
    assert skill_coverage(set(), {"python"}) == 0.5
    assert skill_coverage(jd, set()) == 0.0
