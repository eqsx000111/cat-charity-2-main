from datetime import datetime

from app.models.charity_project import CharityProject


def calculate_duration_days(
    start: datetime,
    end: datetime
) -> int:
    return (end.date() - start.date()).days


def prepare_projects_report(
    projects: list[CharityProject]
) -> list[list[str]]:
    rows = []

    for project in projects:
        duration = calculate_duration_days(
            project.create_date,
            project.close_date
        )

        rows.append([
            project.name,
            str(duration),
            project.description
        ])

    return rows