
def format_bib_name(name):
    """Safely format a runner's name for the bib."""
    if name is None:
        return ""

    try:
        return str(name).strip().upper()[:12]
    except Exception:
        return ""


def parse_finish_time(text):
    """Convert H:MM:SS into seconds safely."""
    if not isinstance(text, str):
        return 0

    try:
        parts = text.strip().split(":")
        if len(parts) != 3:
            return 0

        if not all(part.isdigit() for part in parts):
            return 0

        hours, minutes, seconds = map(int, parts)

        if minutes > 59 or seconds > 59:
            return 0

        return hours * 3600 + minutes * 60 + seconds
    except (ValueError, TypeError):
        return 0


def average_split(text):
    """Safely calculate the average of split times."""
    if not isinstance(text, str) or not text.strip():
        return 0.0

    try:
        splits = text.split()

        if not splits:
            return 0.0

        if not all(s.isdigit() for s in splits):
            return 0.0

        numbers = [int(s) for s in splits]
        return sum(numbers) / len(numbers)
    except (ValueError, TypeError):
        return 0.0


def main():
    print("==== Running format_bib_name ====")
    value = input("Enter the name to print on the bib: ")
    print("Bib name:", format_bib_name(value))

    print("\n==== Running parse_finish_time ====")
    value = input("Enter a finish time as H:MM:SS (e.g. 3:45:10): ")
    print("Finish time in seconds:", parse_finish_time(value))

    print("\n==== Running average_split ====")
    value = input("Enter your 5 km split times in minutes separated by spaces: ")
    print("Average split (minutes):", average_split(value))


if __name__ == "__main__":
    main()
