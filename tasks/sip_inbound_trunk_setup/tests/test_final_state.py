import json
import os
import subprocess
import pytest
from pathlib import Path

PROJECT_DIR = Path("/home/user/livekit-sip")
SETUP_SCRIPT = PROJECT_DIR / "setup_sip.py"
SIP_CONFIG = PROJECT_DIR / "sip_config.json"


def test_setup_sip_py_exists():
    assert SETUP_SCRIPT.is_file(), f"setup_sip.py not found at {SETUP_SCRIPT}"


def test_script_uses_create_sip_inbound_trunk():
    source = SETUP_SCRIPT.read_text()
    assert "create_sip_inbound_trunk" in source, (
        "setup_sip.py must call create_sip_inbound_trunk"
    )


def test_script_uses_create_sip_dispatch_rule():
    source = SETUP_SCRIPT.read_text()
    assert "create_sip_dispatch_rule" in source, (
        "setup_sip.py must call create_sip_dispatch_rule"
    )


def test_script_uses_call_prefix():
    source = SETUP_SCRIPT.read_text()
    assert "call-" in source, (
        "setup_sip.py must use room_prefix='call-' in the dispatch rule"
    )


def test_script_uses_livekit_api():
    source = SETUP_SCRIPT.read_text()
    assert "LiveKitAPI" in source, (
        "setup_sip.py must use api.LiveKitAPI() as the API client"
    )


def test_sip_config_json_exists():
    assert SIP_CONFIG.is_file(), (
        f"sip_config.json not found at {SIP_CONFIG} — run setup_sip.py to generate it"
    )


def test_sip_config_has_trunk_id():
    data = json.loads(SIP_CONFIG.read_text())
    assert "trunk_id" in data, "sip_config.json must contain 'trunk_id'"
    assert isinstance(data["trunk_id"], str) and data["trunk_id"], (
        "sip_config.json 'trunk_id' must be a non-empty string"
    )


def test_sip_config_has_dispatch_rule_id():
    data = json.loads(SIP_CONFIG.read_text())
    assert "dispatch_rule_id" in data, (
        "sip_config.json must contain 'dispatch_rule_id'"
    )
    assert isinstance(data["dispatch_rule_id"], str) and data["dispatch_rule_id"], (
        "sip_config.json 'dispatch_rule_id' must be a non-empty string"
    )


def test_sip_config_trunk_name():
    data = json.loads(SIP_CONFIG.read_text())
    assert data.get("trunk_name") == "AI Call Center", (
        f"sip_config.json 'trunk_name' must be 'AI Call Center', got: {data.get('trunk_name')}"
    )


def test_sip_config_numbers():
    data = json.loads(SIP_CONFIG.read_text())
    assert "numbers" in data, "sip_config.json must contain 'numbers'"
    assert isinstance(data["numbers"], list), (
        "sip_config.json 'numbers' must be a list"
    )
    assert "+15551234567" in data["numbers"], (
        f"sip_config.json 'numbers' must contain '+15551234567', got: {data['numbers']}"
    )
