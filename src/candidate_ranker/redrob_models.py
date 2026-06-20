from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any


@dataclass
class Profile:
    anonymized_name: str
    headline: str
    summary: str
    location: str
    country: str
    years_of_experience: float
    current_title: str
    current_company: str
    current_company_size: str
    current_industry: str


@dataclass
class CareerEntry:
    company: str
    title: str
    start_date: str
    end_date: str | None
    duration_months: int
    is_current: bool
    industry: str
    company_size: str
    description: str


@dataclass
class EducationEntry:
    institution: str
    degree: str
    field_of_study: str
    start_year: int
    end_year: int
    grade: str | None = None
    tier: str = "unknown"


@dataclass
class Skill:
    name: str
    proficiency: str
    endorsements: int
    duration_months: int = 0


@dataclass
class Certification:
    name: str
    issuer: str
    year: int


@dataclass
class Language:
    language: str
    proficiency: str


@dataclass
class RedrobSignals:
    profile_completeness_score: float = 0.0
    signup_date: str = ""
    last_active_date: str = ""
    open_to_work_flag: bool = False
    profile_views_received_30d: int = 0
    applications_submitted_30d: int = 0
    recruiter_response_rate: float = 0.0
    avg_response_time_hours: float = 0.0
    skill_assessment_scores: dict[str, float] = field(default_factory=dict)
    connection_count: int = 0
    endorsements_received: int = 0
    notice_period_days: int = 0
    expected_salary_range_inr_lpa: dict[str, float] = field(default_factory=dict)
    preferred_work_mode: str = ""
    willing_to_relocate: bool = False
    github_activity_score: float = -1.0
    search_appearance_30d: int = 0
    saved_by_recruiters_30d: int = 0
    interview_completion_rate: float = 0.0
    offer_acceptance_rate: float = -1.0
    verified_email: bool = False
    verified_phone: bool = False
    linkedin_connected: bool = False


@dataclass
class Candidate:
    candidate_id: str
    profile: Profile
    career_history: list[CareerEntry] = field(default_factory=list)
    education: list[EducationEntry] = field(default_factory=list)
    skills: list[Skill] = field(default_factory=list)
    certifications: list[Certification] = field(default_factory=list)
    languages: list[Language] = field(default_factory=list)
    redrob_signals: RedrobSignals = field(default_factory=RedrobSignals)


def _parse_profile(raw: dict) -> Profile:
    p = raw.get("profile", {})
    return Profile(
        anonymized_name=p.get("anonymized_name", ""),
        headline=p.get("headline", ""),
        summary=p.get("summary", ""),
        location=p.get("location", ""),
        country=p.get("country", ""),
        years_of_experience=p.get("years_of_experience", 0.0),
        current_title=p.get("current_title", ""),
        current_company=p.get("current_company", ""),
        current_company_size=p.get("current_company_size", ""),
        current_industry=p.get("current_industry", ""),
    )


def _parse_career(raw_list: list[dict]) -> list[CareerEntry]:
    return [
        CareerEntry(
            company=e.get("company", ""),
            title=e.get("title", ""),
            start_date=e.get("start_date", ""),
            end_date=e.get("end_date"),
            duration_months=e.get("duration_months", 0),
            is_current=e.get("is_current", False),
            industry=e.get("industry", ""),
            company_size=e.get("company_size", ""),
            description=e.get("description", ""),
        )
        for e in raw_list
    ]


def _parse_education(raw_list: list[dict]) -> list[EducationEntry]:
    return [
        EducationEntry(
            institution=e.get("institution", ""),
            degree=e.get("degree", ""),
            field_of_study=e.get("field_of_study", ""),
            start_year=e.get("start_year", 0),
            end_year=e.get("end_year", 0),
            grade=e.get("grade"),
            tier=e.get("tier", "unknown"),
        )
        for e in raw_list
    ]


def _parse_skills(raw_list: list[dict]) -> list[Skill]:
    return [
        Skill(
            name=s.get("name", ""),
            proficiency=s.get("proficiency", "beginner"),
            endorsements=s.get("endorsements", 0),
            duration_months=s.get("duration_months", 0),
        )
        for s in raw_list
    ]


def _parse_certifications(raw_list: list[dict]) -> list[Certification]:
    return [
        Certification(
            name=c.get("name", ""),
            issuer=c.get("issuer", ""),
            year=c.get("year", 0),
        )
        for c in raw_list
    ]


def _parse_languages(raw_list: list[dict]) -> list[Language]:
    return [
        Language(language=l.get("language", ""), proficiency=l.get("proficiency", ""))
        for l in raw_list
    ]


def _parse_signals(raw: dict) -> RedrobSignals:
    rs = raw.get("redrob_signals", {})
    return RedrobSignals(
        profile_completeness_score=rs.get("profile_completeness_score", 0.0),
        signup_date=rs.get("signup_date", ""),
        last_active_date=rs.get("last_active_date", ""),
        open_to_work_flag=rs.get("open_to_work_flag", False),
        profile_views_received_30d=rs.get("profile_views_received_30d", 0),
        applications_submitted_30d=rs.get("applications_submitted_30d", 0),
        recruiter_response_rate=rs.get("recruiter_response_rate", 0.0),
        avg_response_time_hours=rs.get("avg_response_time_hours", 0.0),
        skill_assessment_scores=rs.get("skill_assessment_scores", {}),
        connection_count=rs.get("connection_count", 0),
        endorsements_received=rs.get("endorsements_received", 0),
        notice_period_days=rs.get("notice_period_days", 0),
        expected_salary_range_inr_lpa=rs.get("expected_salary_range_inr_lpa", {}),
        preferred_work_mode=rs.get("preferred_work_mode", ""),
        willing_to_relocate=rs.get("willing_to_relocate", False),
        github_activity_score=rs.get("github_activity_score", -1.0),
        search_appearance_30d=rs.get("search_appearance_30d", 0),
        saved_by_recruiters_30d=rs.get("saved_by_recruiters_30d", 0),
        interview_completion_rate=rs.get("interview_completion_rate", 0.0),
        offer_acceptance_rate=rs.get("offer_acceptance_rate", -1.0),
        verified_email=rs.get("verified_email", False),
        verified_phone=rs.get("verified_phone", False),
        linkedin_connected=rs.get("linkedin_connected", False),
    )


def parse_candidate(raw: dict) -> Candidate:
    return Candidate(
        candidate_id=raw.get("candidate_id", ""),
        profile=_parse_profile(raw),
        career_history=_parse_career(raw.get("career_history", [])),
        education=_parse_education(raw.get("education", [])),
        skills=_parse_skills(raw.get("skills", [])),
        certifications=_parse_certifications(raw.get("certifications", [])),
        languages=_parse_languages(raw.get("languages", [])),
        redrob_signals=_parse_signals(raw),
    )
