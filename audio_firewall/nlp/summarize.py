def summarize_flags(flagged_segments, user_keywords=None):
    if not flagged_segments:
        return "No flagged segments to summarize."

    summary_lines = []

    for segment in flagged_segments:
        text_lower = segment["text"].lower()
        matched_keywords = []

        # Detect which keywords appeared in the segment text
        for keyword in user_keywords or []:
            if keyword.lower() in text_lower:
                matched_keywords.append(keyword)

        # Format output
        if matched_keywords:
            summary_lines.append(
                f" {segment['timestamp']}: flagged keywords → {', '.join(set(matched_keywords))}"
            )
        else:
            summary_lines.append(
                f" {segment['timestamp']}: sensitive topic detected (semantic match)"
            )

    return "\n".join(summary_lines)
