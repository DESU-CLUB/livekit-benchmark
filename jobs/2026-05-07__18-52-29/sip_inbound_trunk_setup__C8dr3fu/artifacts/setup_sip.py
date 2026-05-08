import asyncio
import json

from dotenv import load_dotenv
from livekit import api


async def main() -> None:
    load_dotenv('.env.local')

    async with api.LiveKitAPI() as lkapi:
        trunk = await lkapi.sip.create_sip_inbound_trunk(
            api.CreateSIPInboundTrunkRequest(
                trunk=api.SIPInboundTrunkInfo(
                    name="AI Call Center",
                    numbers=["+15551234567"],
                )
            )
        )

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

    print(f"SIP inbound trunk created: {trunk.sip_trunk_id}")

    config = {
        "trunk_id": trunk.sip_trunk_id,
        "dispatch_rule_id": rule.sip_dispatch_rule_id,
        "trunk_name": "AI Call Center",
        "numbers": ["+15551234567"],
    }

    with open("sip_config.json", "w", encoding="utf-8") as config_file:
        json.dump(config, config_file, indent=2)
        config_file.write("\n")


if __name__ == "__main__":
    asyncio.run(main())
