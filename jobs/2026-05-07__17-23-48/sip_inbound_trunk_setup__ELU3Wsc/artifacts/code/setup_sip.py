import asyncio
import json
from dotenv import load_dotenv
import livekit.api as api

# Load environment variables from .env.local
load_dotenv('.env.local')

async def main():
    # Create LiveKit API client
    async with api.LiveKitAPI() as lkapi:
        # Define our desired trunk configuration
        trunk_name = "AI Call Center"
        phone_number = "+15551234567"
        
        # Check if trunk already exists
        trunks = await lkapi.sip.list_inbound_trunk(api.ListSIPInboundTrunkRequest())
        
        existing_trunk = None
        for trunk in trunks.items:
            if trunk.name == trunk_name and phone_number in trunk.numbers:
                existing_trunk = trunk
                break
        
        if existing_trunk:
            print(f"Using existing SIP inbound trunk: {existing_trunk.sip_trunk_id}")
            trunk_id = existing_trunk.sip_trunk_id
        else:
            # Create new SIP inbound trunk
            trunk = await lkapi.sip.create_inbound_trunk(
                api.CreateSIPInboundTrunkRequest(
                    trunk=api.SIPInboundTrunkInfo(
                        name=trunk_name,
                        numbers=[phone_number],
                    )
                )
            )
            
            print(f"SIP inbound trunk created: {trunk.sip_trunk_id}")
            trunk_id = trunk.sip_trunk_id
        
        # Check if dispatch rule already exists for this trunk
        rules = await lkapi.sip.list_dispatch_rule(api.ListSIPDispatchRuleRequest())
        
        existing_rule = None
        for rule in rules.items:
            if trunk_id in rule.trunk_ids:
                existing_rule = rule
                break
        
        if existing_rule:
            print(f"Using existing SIP dispatch rule: {existing_rule.sip_dispatch_rule_id}")
            rule_id = existing_rule.sip_dispatch_rule_id
        else:
            # Create new SIP dispatch rule
            rule = await lkapi.sip.create_dispatch_rule(
                api.CreateSIPDispatchRuleRequest(
                    rule=api.SIPDispatchRuleInfo(
                        rule=api.SIPDispatchRule(
                            dispatch_rule_individual=api.SIPDispatchRuleIndividual(
                                room_prefix="call-"
                            )
                        ),
                        trunk_ids=[trunk_id],
                        attributes={"agent_name": "phone-agent"},
                    )
                )
            )
            
            print(f"SIP dispatch rule created: {rule.sip_dispatch_rule_id}")
            rule_id = rule.sip_dispatch_rule_id
        
        # Save config to JSON file
        config = {
            "trunk_id": trunk_id,
            "dispatch_rule_id": rule_id,
            "trunk_name": trunk_name,
            "numbers": [phone_number]
        }
        
        with open('sip_config.json', 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"Configuration saved to sip_config.json")

if __name__ == "__main__":
    asyncio.run(main())