import asyncio
import json
from dotenv import load_dotenv
from livekit import api

load_dotenv('.env.local')

TRUNK_NAME = "AI Call Center"
PHONE_NUMBER = "+15551234567"
ROOM_PREFIX = "call-"
AGENT_NAME = "phone-agent"


async def main():
    async with api.LiveKitAPI() as lkapi:
        # --- Create (or reuse) SIP inbound trunk ---
        trunk = None
        try:
            result = await lkapi.sip.create_sip_inbound_trunk(
                api.CreateSIPInboundTrunkRequest(
                    trunk=api.SIPInboundTrunkInfo(
                        name=TRUNK_NAME,
                        numbers=[PHONE_NUMBER],
                    )
                )
            )
            trunk = result
        except Exception as e:
            # If the trunk already exists for this number, find and reuse it
            if "Conflicting inbound SIP Trunks" in str(e):
                list_result = await lkapi.sip.list_sip_inbound_trunk(
                    api.ListSIPInboundTrunkRequest()
                )
                for t in list_result.items:
                    if PHONE_NUMBER in t.numbers and t.name == TRUNK_NAME:
                        trunk = t
                        print(f"Reusing existing trunk: {trunk.sip_trunk_id}")
                        break
            if trunk is None:
                raise

        # --- Create (or reuse) SIP dispatch rule ---
        rule = None
        try:
            result = await lkapi.sip.create_sip_dispatch_rule(
                api.CreateSIPDispatchRuleRequest(
                    rule=api.SIPDispatchRuleInfo(
                        rule=api.SIPDispatchRule(
                            dispatch_rule_individual=api.SIPDispatchRuleIndividual(
                                room_prefix=ROOM_PREFIX
                            )
                        ),
                        trunk_ids=[trunk.sip_trunk_id],
                        attributes={"agent_name": AGENT_NAME},
                    )
                )
            )
            rule = result
        except Exception as e:
            # If a rule already exists for this trunk, find and reuse it
            list_result = await lkapi.sip.list_sip_dispatch_rule(
                api.ListSIPDispatchRuleRequest()
            )
            for r in list_result.items:
                if trunk.sip_trunk_id in r.trunk_ids:
                    rule = r
                    print(f"Reusing existing dispatch rule: {rule.sip_dispatch_rule_id}")
                    break
            if rule is None:
                raise

    print(f"SIP inbound trunk created: {trunk.sip_trunk_id}")

    config = {
        "trunk_id": trunk.sip_trunk_id,
        "dispatch_rule_id": rule.sip_dispatch_rule_id,
        "trunk_name": TRUNK_NAME,
        "numbers": [PHONE_NUMBER],
    }

    with open("sip_config.json", "w") as f:
        json.dump(config, f, indent=2)

    print(f"Config saved to sip_config.json")


asyncio.run(main())
