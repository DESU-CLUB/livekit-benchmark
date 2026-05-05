## Background
LiveKit SIP enables phone call integration with LiveKit rooms. An inbound SIP trunk defines which phone numbers LiveKit should accept calls from. A SIP dispatch rule determines how incoming calls on a trunk are routed to rooms and agents. The Python server SDK provides the `livekit.api` module with a `LiveKitAPI` async context manager to call the SIP management API.

## Requirements
Write a Python script that creates a SIP inbound trunk and a dispatch rule, then saves the resulting IDs to a JSON config file.

## Implementation Guide
1. Navigate to the project directory at `/home/user/livekit-sip`.
2. Create a file named `setup_sip.py` that:
   - Loads environment variables from `.env.local` using `python-dotenv` (`load_dotenv('.env.local')`).
   - Uses `asyncio.run` and `async with api.LiveKitAPI() as lkapi:`.
   - Creates a SIP inbound trunk:
     ```python
     trunk = await lkapi.sip.create_sip_inbound_trunk(
         api.CreateSIPInboundTrunkRequest(
             trunk=api.SIPInboundTrunkInfo(
                 name="AI Call Center",
                 numbers=["+15551234567"],
             )
         )
     )
     ```
   - Creates a SIP dispatch rule:
     ```python
     rule = await lkapi.sip.create_sip_dispatch_rule(
         api.CreateSIPDispatchRuleRequest(
             rule=api.SIPDispatchRuleInfo(
                 rule=api.SIPDispatchRule(
                     dispatch_rule_individual=api.SIPDispatchRuleIndividual(
                         room_prefix="call-"
                     )
                 ),
                 trunk_ids=[trunk.sip_trunk_id],
                 attributes={"agent_name": "phone-agent"},
             )
         )
     )
     ```
   - Prints `f"SIP inbound trunk created: {trunk.sip_trunk_id}"` to stdout.
   - Saves the config to `sip_config.json` in the project directory:
     ```json
     {
       "trunk_id": "<trunk.sip_trunk_id>",
       "dispatch_rule_id": "<rule.sip_dispatch_rule_id>",
       "trunk_name": "AI Call Center",
       "numbers": ["+15551234567"]
     }
     ```
3. Run the script: `python3 setup_sip.py`

## Constraints
- Project path: `/home/user/livekit-sip`
- Log file: `/home/user/livekit-sip/sip_config.json`
- `livekit-server-sdk` (Python) and `python-dotenv` are already installed via pip
- `.env.local` already exists with `LIVEKIT_URL`, `LIVEKIT_API_KEY`, `LIVEKIT_API_SECRET`
- Trunk name must be `"AI Call Center"`, phone number `"+15551234567"`
- Dispatch rule must use `dispatch_rule_individual` with `room_prefix="call-"`
- Dispatch rule attribute must include `"agent_name": "phone-agent"`

## Integrations
- **LiveKit Python Server SDK**: `livekit.api` — `LiveKitAPI`, `CreateSIPInboundTrunkRequest`, `SIPInboundTrunkInfo`, `CreateSIPDispatchRuleRequest`, `SIPDispatchRuleInfo`, `SIPDispatchRule`, `SIPDispatchRuleIndividual`
- **python-dotenv**: environment variable loading
