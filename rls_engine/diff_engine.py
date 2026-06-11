import re
from typing import Dict

def extract_conditions(sql: str):
    sql = sql.lower()

    using_match = re.search(r"using\s*\((.*?)\)", sql)
    check_match = re.search(r"with check\s*\((.*?)\)", sql)

    return {
        "using": using_match.group(1) if using_match else None,
        "check": check_match.group(1) if check_match else None
    }


def diff_policies(old_sql: str, new_sql: str) -> Dict:
    old = extract_conditions(old_sql)
    new = extract_conditions(new_sql)

    diff = {
        "using_changed": old["using"] != new["using"],
        "check_changed": old["check"] != new["check"],
        "old": old,
        "new": new
    }

    return diff