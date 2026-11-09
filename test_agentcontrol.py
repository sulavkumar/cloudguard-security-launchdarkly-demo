
import asyncio
import os

from dotenv import load_dotenv
from launchdarkly_ai_server import config, init_client, shutdown
from launchdarkly_ai_openai_agents import create_openai_agents_handler

import ldclient
from ldclient.config import Config
from ldclient import Context

load_dotenv()

async def main():
    sdk_key = os.getenv("LAUNCHDARKLY_SDK_KEY")

    if not sdk_key:
        raise RuntimeError("LaunchDarkly SDK key is missing.")

    # Reuse the existing LaunchDarkly SDK configuration
    ldclient.set_config(Config(sdk_key))
    ld_client = ldclient.get()

    await init_client(client=ld_client)

    context = {
        "kind": "user",
        "key": "security_admin_001",
        "name": "Security Administrator",
        "user_tier": "Standard",
        "geography": "India",
        "environment": "Production"
    }

    try:
        agent = config(
            key="cloud-guard-ai-security-analyst",
            handler=create_openai_agents_handler()
        )

        print("Agent config key:", "cloud-guard-ai-security-analyst")
        print("Invoking Agent with Test context...")
        result = await agent.invoke(
            "A cloud server has SSH port 22 exposed to the public internet. "
            "Explain the security risks and recommend remediation steps.",
            context
        )

        print("\nCloudGuard AI Security Analyst:")
        print(result.response)

    finally:
        await shutdown()
        ld_client.close()

if __name__ == "__main__":
    asyncio.run(main())