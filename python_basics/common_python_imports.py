import logging
import re
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path


# Custom LoggerAdapter to format extra context in logs
class PipeTextAdapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        # Pop the 'extra' dictionary out of kwargs (returns None if not present)
        extra = kwargs.pop("extra", None)

        if extra:
            # Format extras as "key=value | key2=value2"
            extra_text = " | ".join(
                f"{key}={value}" for key, value in extra.items()
            )

            # Prepend the extra text and a pipe before the actual message
            msg = f"{extra_text} | {msg}"

        return msg, kwargs


def datetime_essentials():
    # 1. Getting current dates and times
    now = datetime.now()  # Local time (naive, no timezone)
    now_utc = datetime.now(timezone.utc)  # UTC time (timezone aware)
    today = date.today()  # Just the date (YYYY-MM-DD)

    print(f"Local Now: {now}")
    print(f"UTC Now: {now_utc}")
    print(f"Today: {today}")

    # 2. Constructing specific dates
    moon_landing = datetime(1969, 7, 20, 20, 17, tzinfo=timezone.utc)

    # 3. Formatting (datetime to string) using strftime
    # %Y = Year, %m = Month, %d = Day, %H = Hour (24h), %M = Minute
    # %A = Weekday name, %B = Month name
    formatted = moon_landing.strftime("%A, %B %d, %Y at %H:%M")
    print(f"Formatted: {formatted}")  # Sunday, July 20, 1969 at 20:17

    # 4. Parsing (string to datetime) using strptime
    date_string = "2026-10-31 14:30:00"
    parsed_date = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")

    # 5. Time Math using timedelta
    # You can add/subtract days, hours, minutes, seconds, weeks
    # (but not months or years)
    tomorrow = now + timedelta(days=1)
    previous_week = now - timedelta(weeks=1)

    two_hours_ago = now - timedelta(hours=2)
    print(
        f"Tomorrow: {tomorrow}, Previous Week: {previous_week}, "
        f"Two Hours Ago: {two_hours_ago}"
    )

    # Calculating differences between two dates returns a timedelta
    time_until_halloween = parsed_date - now
    print(f"Days until Halloween: {time_until_halloween.days}")


def pathlib_essentials():
    # 1. Creating path objects
    current_dir = Path.cwd()  # Current working directory
    print(f"Current Directory: {current_dir}")
    home_dir = Path.home()  # User's home directory
    print(f"User's Home Directory: {home_dir}")

    # 2. Joining paths (Use the '/' operator instead of os.path.join)
    # This automatically uses the correct separator for your OS (\ on Windows,
    # / on Mac/Linux)
    my_folder = current_dir / "my_project" / "data"
    print(f"My Folder Path: {my_folder}")
    my_file = my_folder / "config.json"
    print(f"My File Path: {my_file}")

    # 3. Directory operations
    # Create directory (parents=True acts like mkdir -p, exist_ok ignores if it
    # already exists)
    my_folder.mkdir(parents=True, exist_ok=True)

    # 4. Checking path existence and types
    if my_folder.exists() and my_folder.is_dir():
        print(f"Directory ready: {my_folder}")

    # 5. Reading and Writing directly (no 'with open()' needed for simple text)
    # When you call .write_text() or .read_text(), Python actually handles the
    # with open() context manager for you under the hood. It opens the file,
    # reads or writes the data, and safely closes the file automatically.
    my_file.write_text('{"status": "active"}', encoding="utf-8")
    content = my_file.read_text(encoding="utf-8")
    print(f"File content: {content}")

    # 6. Extracting parts of a path
    print(f"Name: {my_file.name}")  # "config.json"
    print(f"Stem: {my_file.stem}")  # "config"
    print(f"Extension: {my_file.suffix}")  # ".json"
    print(f"Parent dir: {my_file.parent}")  # ".../my_project/data"

    # 7. Searching (Globbing)
    # .glob() for current dir, .rglob() for recursive search
    python_files = list(current_dir.rglob("*.py"))
    print(f"Found {len(python_files)} Python files in this project.")


def logging_essentials():
    # 1. Basic Configuration
    # We configure a structured format including time, logger name, level,
    # and message
    logging.basicConfig(
        # Minimum level to capture (DEBUG captures everything)
        level=logging.DEBUG,
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.StreamHandler(sys.stdout),  # Output to console
            logging.FileHandler("app.log"),  # Simultaneously save to a file
        ],
    )

    # 2. Create a specific logger for this module/component
    # Using __name__ is best practice as it names the logger after your file
    logger = logging.getLogger(__name__)

    # 3. Log Levels (in increasing order of severity)
    logger.debug("1. Debug: Detailed info for diagnosing problems.")
    logger.info("2. Info: General application events (e.g., 'Server started').")
    logger.warning(
        "3. Warning: Something unexpected happened, but app still runs."
    )
    logger.error("4. Error: A serious issue occurred, a function failed.")
    logger.critical("5. Critical: A fatal error, the program may crash.")

    # 4. Logging Exceptions
    # Using exc_info=True (or logger.exception) automatically attaches the
    # stack trace to the log
    try:
        1 / 0  # type: ignore
    except ZeroDivisionError:
        # exc_info=True includes the traceback in the log,
        # which is very useful for debugging.
        logger.error("Attempted to divide by zero", exc_info=True)

    # 5. Structured logging with extra context
    user_id = 42
    session_id = "abc123"
    # logger.info(f"User logged in with ID: {user_id}")
    pipe_logger = PipeTextAdapter(logger, {})
    pipe_logger.info("User logged in", extra={"user_id": user_id})
    pipe_logger.warning(
        "Private session ended", extra={"session_id": session_id}
    )
    # Note: To natively output JSON structured logs, you usually pair this
    # with a third-party library like `python-json-logger`.


def re_essentials():
    # 1. SLUG CLEANUP (Using re.sub for substitution)
    title = "  Hello World! -- This is a Test: 100% Awesome.  "

    # Step A: Convert to lowercase and strip leading/trailing whitespace
    slug = title.lower().strip()

    # Step B: Replace any non-alphanumeric character (\W) or underscore with a
    # hyphen \W matches anything that is NOT [a-zA-Z0-9_]
    slug = re.sub(r"[\W_]+", "-", slug)

    # Step C: Strip hyphens from the start and end
    # (in case punctuation was there)
    slug = slug.strip("-")

    print(f"Original: {title}")
    print(f"Slug:     {slug}")  # Output: hello-world-this-is-a-test-100-awesome

    # 2. MATCHING vs SEARCHING
    text = "User email is contact@example.com right now."

    # re.search scans the WHOLE string and finds the first match
    email_pattern = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
    search_result = re.search(email_pattern, text)
    # If a match is found, search_result will be a Match object; otherwise,
    # it will be None. Use search_result.group() to get the matched string.
    if search_result:
        print(f"Found email: {search_result.group()}")

    # re.match only looks at the VERY BEGINNING of the string.
    # This will fail because the string starts with "User", not an email.
    match_result = re.match(email_pattern, text)
    print(f"Match result (at start of string): {match_result}")

    # 3. FINDALL (Extracting multiple matches)
    prices_text = "Apples are $1.50, bananas are $0.75, and grapes are $3.00."
    # Find a literal dollar sign (\$), followed by digits, a period,
    # and two digits
    prices = re.findall(r"\$\d+\.\d{2}", prices_text)
    print(f"All prices found: {prices}")  # ['$1.50', '$0.75', '$3.00']

    # 4. COMPILING (For performance)
    # If you use a regex repeatedly in a loop, compile it once first.
    compiled_regex = re.compile(r"\d{4}")  # Matches any 4 digits (e.g., a year)
    print(compiled_regex.findall("Years 1999, 2010, and 2026"))


if __name__ == "__main__":
    datetime_essentials()
    pathlib_essentials()
    logging_essentials()
    re_essentials()
