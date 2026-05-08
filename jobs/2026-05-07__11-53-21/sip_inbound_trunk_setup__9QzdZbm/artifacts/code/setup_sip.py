import asyncio
import json
import os
from dotenv import load_dotenv
from livekit import api

async def main():
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
                rule=api.SIPDispatchRule(
                    dispatch_rule_individual=api.SIPDispatchRuleIndividual(
                        room_prefix="call-"
                    )
                ),
                trunk_ids=[trunk.sip_trunk_id],
                attributes={"agent_name": "phone-agent"},
            )
        )
        
        print(f"SIP inbound trunk created: {trunk.sip_trunk_id}")
        
        config = {
            "trunk_id": trunk.sip_trunk_id,
            "dispatch_rule_id": rule.sip_dispatch_rule_id,
            "trunk_name": "AI Call Center",
            "numbers": ["+15551234567"]
        }
        
        with open('sip_config.json', 'w') as f:
            json.dump(config, f, indent=2)

if __name__ == "__main__":
    asyncio.run(main())
