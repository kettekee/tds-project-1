def parse_and_execute_task(task_description: str):
    """
    Parses the plain‑English task description and dispatches to the appropriate function.
    Supports tasks A1–A10.
    """
    task_lower = task_description.lower()

    # Task A1: Run datagen.py
    if "datagen.py" in task_lower:
        from tasks.operations import task_a1_run_datagen
        # Extract email from the task (assuming it's enclosed in backticks)
        # For simplicity, assume the email is the first backtick-quoted string.
        import re
        m = re.search(r"`([^`]+@[^`]+)`", task_description)
        if not m:
            raise ValueError("No email found in task description for A1")
        email = m.group(1)
        return task_a1_run_datagen(email)

    # Task A2: Format markdown file
    elif "format" in task_lower and "format.md" in task_lower:
        from tasks.operations import task_a2_format_markdown
        return task_a2_format_markdown()

    # Task A3: Count Wednesdays in dates.txt
    elif "wednesday" in task_lower and "dates.txt" in task_lower:
        from tasks.operations import task_a3_count_wednesdays
        return task_a3_count_wednesdays()

    # Task A4: Sort contacts.json
    elif "sort" in task_lower and "contacts.json" in task_lower:
        from tasks.operations import task_a4_sort_contacts
        return task_a4_sort_contacts()

    # Task A5: Logs – write first line of 10 most recent .log files
    elif "most recent" in task_lower and ".log" in task_lower:
        from tasks.operations import task_a5_logs_recent
        return task_a5_logs_recent()

    # Task A6: Create docs index
    elif "docs" in task_lower and "index.json" in task_lower:
        from tasks.operations import task_a6_create_docs_index
        return task_a6_create_docs_index()

    # Task A7: Extract sender's email from email.txt
    elif "email.txt" in task_lower and "sender" in task_lower:
        from tasks.operations import task_a7_extract_email
        return task_a7_extract_email()

    # Task A8: Extract credit card number (delegated to LLM service)
    elif "credit card" in task_lower and "extract" in task_lower:
        from services.llm_service import extract_credit_card_number
        return extract_credit_card_number()

    # Task A9: Find similar comments using embeddings
    elif "comments.txt" in task_lower and "similar" in task_lower:
        from tasks.operations import task_a9_find_similar_comments
        return task_a9_find_similar_comments()

    # Task A10: Total sales for Gold tickets
    elif "gold" in task_lower and "ticket" in task_lower:
        from tasks.operations import task_a10_total_sales_gold
        return task_a10_total_sales_gold()

    raise ValueError("Unrecognized or unsupported task description.")
