# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------

"""Ruleset Requirements tests subdirectory."""

from typing import Any


def create_rule(
    name: str, rule_type: str, ruleset_name: str, parameters: dict[str, Any], ruleset_id: str = "0"
):
    """Helper function to create rule structure"""
    return {
        "name": name,
        "type": rule_type,
        "ruleset_id": ruleset_id,
        "ruleset": {"name": ruleset_name},
        "parameters": parameters,
    }
