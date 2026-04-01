# ============================================
#   Simple Log File Analyzer
#   Concepts used: lists, loops, functions,
#   string methods, dictionaries, file I/O
# ============================================

# ---------- SAMPLE LOG DATA ----------
# (In Colab we don't have a real file, so we create one first)

sample_logs = """INFO 2024-01-01 10:00:01 User logged in
ERROR 2024-01-01 10:05:22 Database connection failed
WARNING 2024-01-01 10:10:45 Memory usage high
INFO 2024-01-01 10:15:00 File uploaded successfully
ERROR 2024-01-01 10:20:33 Null pointer exception
INFO 2024-01-01 10:25:10 User logged out
WARNING 2024-01-01 10:30:55 Disk space low
ERROR 2024-01-01 10:35:44 Timeout error
INFO 2024-01-01 10:40:00 Backup completed
ERROR 2024-01-01 10:45:12 Authentication failed
WARNING 2024-01-01 10:50:30 CPU usage high
INFO 2024-01-01 10:55:05 System started
"""

# ---------- STEP 1: CREATE THE LOG FILE ----------

def create_log_file(filename):
    with open(filename, "w") as f:
        f.write(sample_logs)
    print(f"✅ Log file '{filename}' created!\n")


# ---------- STEP 2: READ THE LOG FILE ----------

def read_log_file(filename):
    lines = []
    with open(filename, "r") as f:
        for line in f:
            line = line.strip()       # remove extra spaces/newlines
            if line != "":            # skip empty lines
                lines.append(line)
    return lines


# ---------- STEP 3: COUNT LOG LEVELS ----------

def count_log_levels(lines):
    counts = {"INFO": 0, "ERROR": 0, "WARNING": 0}

    for line in lines:
        if line.startswith("INFO"):
            counts["INFO"] += 1
        elif line.startswith("ERROR"):
            counts["ERROR"] += 1
        elif line.startswith("WARNING"):
            counts["WARNING"] += 1

    return counts


# ---------- STEP 4: FILTER BY LOG LEVEL ----------

def filter_by_level(lines, level):
    result = []
    for line in lines:
        if line.startswith(level):
            result.append(line)
    return result


# ---------- STEP 5: SEARCH IN LOGS ----------

def search_keyword(lines, keyword):
    result = []
    for line in lines:
        if keyword.lower() in line.lower():   # case-insensitive search
            result.append(line)
    return result


# ---------- STEP 6: PRINT REPORT ----------

def print_report(counts, total):
    print("=" * 45)
    print("         📋 LOG FILE ANALYSIS REPORT")
    print("=" * 45)
    print(f"  Total log entries   : {total}")
    print(f"  INFO    entries     : {counts['INFO']}")
    print(f"  WARNING entries     : {counts['WARNING']}")
    print(f"  ERROR   entries     : {counts['ERROR']}")
    print("=" * 45)


# ---------- MAIN PROGRAM ----------

def main():
    filename = "sample.log"

    # Step 1: Create log file
    create_log_file(filename)

    # Step 2: Read log file
    lines = read_log_file(filename)
    print(f"📂 Total lines read: {len(lines)}\n")

    # Step 3: Count levels and print report
    counts = count_log_levels(lines)
    print_report(counts, len(lines))

    # Step 4: Show all ERROR logs
    print("\n🔴 ERROR Logs:")
    errors = filter_by_level(lines, "ERROR")
    for e in errors:
        print("  ", e)

    # Step 5: Show all WARNING logs
    print("\n🟡 WARNING Logs:")
    warnings = filter_by_level(lines, "WARNING")
    for w in warnings:
        print("  ", w)

    # Step 6: Search for a keyword
    keyword = "failed"
    print(f"\n🔍 Search results for '{keyword}':")
    results = search_keyword(lines, keyword)
    if results:
        for r in results:
            print("  ", r)
    else:
        print("  No results found.")


# Run the program
main()