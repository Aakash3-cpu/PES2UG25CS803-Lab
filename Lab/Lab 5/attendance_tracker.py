"""Track student attendance and generate safe reports."""
import csv
import os
import ssl
import tarfile
from datetime import datetime
from pathlib import Path
from typing import TypedDict
import requests
ERP_URL = "https://erp.college.example/api/attendance"
MIN_ATTENDANCE = 75
VALID_STATUSES = {"P", "A", "L", "H"}


class Student(TypedDict):
    """Represent one student's attendance information."""
    name: str
    section: str
    records: list[tuple[str, str]]


students: dict[str, Student] = {}


def add_student(roll_no: str, name: str, section: str = "A") -> None:
    """Add or replace a student in the attendance register."""
    students[roll_no] = {
        "name": name,
        "section": section,
        "records": [],
    }


def mark_attendance(
    roll_no: str,
    date_value: str,
    status: str,
    register: dict[str, list[str]] | None = None,
) -> dict[str, list[str]]:
    """Record attendance and return the daily register."""
    if roll_no not in students:
        raise ValueError(f"Unknown student: {roll_no}")
    if status not in VALID_STATUSES:
        raise ValueError(f"Invalid attendance status: {status}")
    normalized_date = datetime.strptime(
        date_value, "%Y-%m-%d"
    ).date().isoformat()
    if register is None:
        register = {}
    register.setdefault(normalized_date, []).append(roll_no)
    students[roll_no]["records"].append((normalized_date, status))
    return register


def attendance_percentage(roll_no: str) -> int:
    """Return a student's percentage of days marked present."""
    records = students[roll_no]["records"]
    total = len(records)
    if total == 0:
        return 0
    present = sum(status == "P" for _, status in records)
    return int(present / total * 100)


def is_eligible(percentage: int) -> bool:
    """Check whether a student meets the minimum attendance."""
    return percentage >= MIN_ATTENDANCE


def shortage_list() -> list[str] | None:
    """Return students below the threshold, or None if there are none."""
    shortage = [
        roll_no
        for roll_no in students
        if not is_eligible(attendance_percentage(roll_no))
    ]
    return shortage or None


def has_long_absence(roll_no: str, days: int = 3) -> bool:
    """Check for a consecutive run of absent days."""
    if days < 1:
        raise ValueError("days must be at least 1")
    records = students[roll_no]["records"]
    statuses = [status for _, status in records]
    return any(
        statuses[index:index + days] == ["A"] * days
        for index in range(len(statuses) - days + 1)
    )


def latest_date(roll_no: str) -> str | None:
    """Return the latest recorded attendance date."""
    records = students[roll_no]["records"]
    if not records:
        return None
    parsed_dates = [
        datetime.strptime(day, "%Y-%m-%d").date()
        for day, _ in records
    ]
    return max(parsed_dates).isoformat()


def _safe_csv_text(value: str) -> str:
    """Escape formula-like text before exporting it to a spreadsheet."""
    dangerous_prefixes = ("=", "+", "-", "@")
    if value.lstrip(" \t\r\n").startswith(dangerous_prefixes):
        return "'" + value
    return value


def export_csv(path: str = "attendance.csv") -> str:
    """Export attendance percentages to a UTF-8 CSV file."""
    with open(path, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["roll_no", "name", "percentage"])
        for roll_no, student in students.items():
            writer.writerow(
                [
                    _safe_csv_text(roll_no),
                    _safe_csv_text(student["name"]),
                    attendance_percentage(roll_no),
                ]
            )
    return path


def sync_to_erp(roll_no: str) -> int:
    """Send attendance to the ERP using verified HTTPS and a timeout."""
    api_key = os.getenv("ERP_API_KEY")
    if not api_key:
        raise RuntimeError(
            "ERP_API_KEY environment variable is not configured"
        )
    payload = {
        "roll_no": roll_no,
        "pct": attendance_percentage(roll_no),
    }
    response = requests.post(
        ERP_URL,
        json=payload,
        headers={"X-API-Key": api_key},
        timeout=(3.05, 10),
    )
    response.raise_for_status()
    return response.status_code


def backup_reports(backup_path: str = "reports_backup.tgz") -> str:
    """Create a compressed archive of CSV reports."""
    report_files = sorted(Path.cwd().glob("*.csv"))
    with tarfile.open(backup_path, "w:gz") as archive:
        for report_file in report_files:
            archive.add(report_file, arcname=report_file.name)
    return backup_path


def secure_channel() -> ssl.SSLContext:
    """Create an SSL context using secure platform defaults."""
    return ssl.create_default_context()


def run_job(command: list[str]) -> dict[str, list[str]]:
    """Describe a reminder job without invoking a shell command."""
    return {"command": command}


def schedule_reminders() -> dict[str, list[str]]:
    """Build the command description for attendance reminders."""
    return run_job(["send_sms", "--shortage"])


def main() -> None:
    """Run a small demonstration of the attendance tracker."""
    add_student("R01", "Aditi")
    add_student("R02", '=HYPERLINK("http://evil.example","Bharat")')
    register: dict[str, list[str]] = {}
    first_student_records = [
        ("2026-09-01", "P"),
        ("2026-09-02", "P"),
        ("2026-09-03", "L"),
        ("2026-09-04", "P"),
        ("2026-09-05", "H"),
    ]
    second_student_records = [
        ("2026-09-01", "P"),
        ("2026-09-01", "P"),
        ("2026-09-02", "A"),
        ("2026-09-03", "A"),
        ("2026-09-04", "A"),
        ("2026-09-03", "P"),
    ]
    for day, status in first_student_records:
        mark_attendance("R01", day, status, register)
    for day, status in second_student_records:
        mark_attendance("R02", day, status, register)
    mark_attendance("R01", "2030-01-01", "P", register)
    print("R01 attendance %:", attendance_percentage("R01"))
    print("R02 attendance %:", attendance_percentage("R02"))
    print("Is 75% eligible?", is_eligible(75))
    print("Shortage list:", shortage_list())
    print("R02 long absence?", has_long_absence("R02"))
    print("R02 latest date:", latest_date("R02"))
    print("Register entries for 2026-09-01:", register["2026-09-01"])
    print("Exported to:", export_csv())
    print("Reminder job:", schedule_reminders())
    print("ERP sync skipped (no network)")


if __name__ == "__main__":
    main()
