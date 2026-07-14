def identify_section_type(section_name):
    name = section_name.lower()

    if "symptom" in name:
        return "symptom"

    elif "diagnosis" in name or "condition" in name:
        return "diagnosis"

    elif "medication" in name or "medicine" in name or "treatment" in name:
        return "medicine"

    elif "test" in name or "report" in name or "result" in name:
        return "test"

    elif "cause" in name or "risk" in name:
        return "risk_factor"

    else:
        return "general"



def analyze_text(text):
    lines = text.split("\n")

    result = {
        "title": "",
        "sections": []
    }

    current_section = None

    for line in lines:
        line = line.strip()

        if not line:
            continue

        # First meaningful line as title
        if result["title"] == "":
            result["title"] = line
            continue

        # Section detection (basic)
        if line.endswith(":"):
            current_section = {
                "name": line.replace(":", ""),
                "content": []
            }
            result["sections"].append(current_section)

        else:
            if current_section:
                current_section["content"].append(line)

    return result
