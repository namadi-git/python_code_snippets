"""
PATHLIB CHEATSHEET
Quick reference for common Path operations in Python.

Usage:
    from pathlib import Path
"""

from pathlib import Path

# -------------------------------------------------------------------
# 1. CREATE PATH OBJECTS
# -------------------------------------------------------------------

# From string (relative or absolute)
p = Path("data/file.txt")          # relative path
p_abs = Path("/tmp/data/file.txt") # absolute (Unix) or r"C:\\tmp\\file.txt" on Windows

# Using / to join paths (preferred over os.path.join)
root = Path("data")
file_path = root / "subdir" / "file.txt"  # "data/subdir/file.txt"


# -------------------------------------------------------------------
# 2. CURRENT DIRECTORY, HOME, SCRIPT LOCATION
# -------------------------------------------------------------------

# Current working directory
cwd = Path.cwd()        # e.g. "/Users/you/project"
# Home directory
home = Path.home()      # e.g. "/Users/you"

# Path of this script (only works in a script, not plain REPL)
# script_path = Path(__file__)
# Absolute, normalized path to this file
# script_path_resolved = script_path.resolve()


# -------------------------------------------------------------------
# 3. BASIC PATH PROPERTIES
# -------------------------------------------------------------------

p = Path("data/reports/report_2025.pdf")

parent = p.parent       # "data/reports" → directory containing the file
name = p.name           # "report_2025.pdf" → full filename
stem = p.stem           # "report_2025" → filename without extension
suffix = p.suffix       # ".pdf" → extension (with dot)
suffixes = p.suffixes   # [".tar", ".gz"] for "archive.tar.gz"


# -------------------------------------------------------------------
# 4. CHECKING EXISTENCE & FILE TYPE
# -------------------------------------------------------------------

# Check if path exists on disk
exists = p.exists()

# Check if file or directory
is_file = p.is_file()
is_dir = p.is_dir()


# -------------------------------------------------------------------
# 5. CREATING DIRECTORIES & FILES
# -------------------------------------------------------------------

logs_dir = Path("logs/subdir")

# mkdir() – create a directory
# parents=True → create missing parent folders too
# exist_ok=True → no error if folder already exists
logs_dir.mkdir(parents=True, exist_ok=True)

# touch() – create an empty file (or update its modified timestamp)
log_file = logs_dir / "app.log"
log_file.touch()  # creates "logs/subdir/app.log" if it doesn't exist


# -------------------------------------------------------------------
# 6. LISTING CONTENTS
# -------------------------------------------------------------------

# iterdir() – non-recursive listing of a directory
for entry in logs_dir.iterdir():
    # Each entry is a Path object (file or directory)
    # Use .is_file() / .is_dir() to inspect
    pass

# rglob() – recursive search (all subfolders)
# NOTE: case_sensitive is available in Python 3.12+
# Find all .log files under logs_dir (case-insensitive)
for log in logs_dir.rglob("*.log", case_sensitive=False):
    # Do something with log
    pass


# -------------------------------------------------------------------
# 7. PATH RESOLUTION
# -------------------------------------------------------------------

# resolve() – get absolute path, resolve symlinks
resolved = p.resolve()  # e.g. "/Users/you/project/data/reports/report_2025.pdf"


# -------------------------------------------------------------------
# 8. PARENT DIRECTORIES
# -------------------------------------------------------------------

# Single parent
parent = p.parent       # one level up

# Multiple parents
grandparent = p.parent.parent

# All parents
parents = list(p.parents)  # [PosixPath('data/reports'), PosixPath('data'), PosixPath('.')]


# -------------------------------------------------------------------
# 9. RENAME / MOVE / REPLACE / DELETE
# -------------------------------------------------------------------

src = logs_dir / "app.log"
dst = logs_dir / "renamed_app.log"

# rename() – rename or move; errors if dst exists
if src.exists():
    src.rename(dst)

# replace() – rename or move; overwrites dst if it exists
backup = logs_dir / "backup.log"
backup.touch()
if dst.exists():
    dst.replace(backup)  # dst → backup (overwrite)

# unlink() – delete a file
if backup.exists():
    backup.unlink()

# rmdir() – remove an EMPTY directory (raises error if not empty)
empty_dir = Path("empty_folder")
empty_dir.mkdir(exist_ok=True)
empty_dir.rmdir()  # OK only if directory has no files/subdirs


# -------------------------------------------------------------------
# 10. SMALL PRACTICAL EXAMPLE
# -------------------------------------------------------------------

def list_txt_files_under(root: Path) -> None:
    """
    Recursively print all .txt files under `root`,
    showing full path, parent folder, and filename.
    """
    for path in root.rglob("*.txt", case_sensitive=False):
        print(f"Full:   {path.resolve()}")
        print(f"Parent: {path.parent}")
        print(f"Name:   {path.stem}{path.suffix}")
        print("-" * 40)


if __name__ == "__main__":
    # Example: list all .txt files under current working directory
    list_txt_files_under(Path.cwd())
