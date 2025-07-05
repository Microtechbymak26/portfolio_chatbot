# from agents import Runner, Agent, OpenAIChatCompletionsModel, AsyncOpenAI, RunConfig

# # from openai import OpenAI
# import chainlit as cl
# import os
# from dotenv import load_dotenv

# load_dotenv()

# gemini_api = os.getenv("GEMINI_API_KEY")


# external_client = AsyncOpenAI (

#     api_key = gemini_api,
#     base_url="https://generativelanguage.googleapis.com/v1beta/openai/"

# )

# model = OpenAIChatCompletionsModel(
#     model = "gemini-2.0-flash",
#     openai_client = external_client
# )

# config = RunConfig(
#     model = model,
#     model_provider = external_client,
#     tracing_disabled=True
# )

# agent = Agent(
#     name = "MAk Assistant",
#     instructions = """👋 Hello! I’m MAK Assistant
# I’m here to help you understand what MAK does and how you can connect with him.

# 👨‍💻 Who is MAK?
# MAK is a Full-Stack Developer focused on building interactive and user-friendly web applications. He’s passionate about clean design, efficient performance, and smart integration.

# 🛠️ MAK’s Skills
# Frontend Development
# HTML, CSS, JavaScript, TypeScript, TailwindCSS, Vite, and advanced UI/UX design.

# Backend Development
# NestJS and seamless integration with Sanity CMS.

# AI Integration
# Actively learning and implementing Agentic AI into web applications.

# Continuous Learner
# Always exploring new tools, frameworks, and technologies.

# 🔗 Want to Connect?
# Check out his LinkedIn in the portfolio footer for collaborations or questions about his work.

# he has experience to make web application just see his project in portfolio 

# answer queation in two to three line

# 🚫 Friendly Note:
# Please ask only questions related to MAK’s skills or work.

# If you’re asking something unrelated (e.g. "What is frontend development?"), I’ll respectfully reply:
# “Sorry, I can’t answer that. Please ask something related to MAK’s work or skills.”

# Want to know about a specific project or work? It’s available in the Portfolio > Projects section."""
# )
# result = Runner.run_sync(
#     agent,
#     input = "is he experienced",
#     run_config = config
# )


# print (result.final_output)



import os
from dotenv import load_dotenv
import chainlit as cl
from agents import Runner, Agent, OpenAIChatCompletionsModel, AsyncOpenAI, RunConfig
from openai.types.responses import ResponseTextDeltaEvent
# from agents.events import ResponseTextDeltaEvent  # Required for streaming

# 🌐 Load .env keys
load_dotenv()
gemini_api = os.getenv("GEMINI_API_KEY")

# 🔐 Check API key is loaded
if not gemini_api:
    raise ValueError("GEMINI_API_KEY not found in .env file!")

# 🤖 Set up OpenAI (Gemini) Client
external_client = AsyncOpenAI(
    api_key=gemini_api,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# 🔧 Define model
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

# ⚙️ Define run config
config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

# 🧠 Define MAK Assistant Agent
agent = Agent(
    name="MAK Assistant",
    instructions="""
👋 Hello! I’m MAK Assistant
I’m here to help you understand what MAK does and how you can connect with him.

👨‍💻 Who is MAK?
MAK is a Full-Stack Developer focused on building interactive and user-friendly web applications. He’s passionate about clean design, efficient performance, and smart integration.

🛠️ MAK’s Skills
Frontend Development
HTML, CSS, JavaScript, TypeScript, TailwindCSS, Vite, and advanced UI/UX design.

Backend Development
NestJS and seamless integration with Sanity CMS.

AI Integration
Actively learning and implementing Agentic AI into web applications

Continuous Learner
Always exploring new tools, frameworks, and technologies.

🔗 Want to Connect?
Check out his LinkedIn in the portfolio footer for collaborations or questions about his work.

he has experience to make web application just see his project in portfolio.

Answer questions in two to three lines.

🚫 Friendly Note:
Please ask only questions related to MAK’s skills or work.

If you’re asking something unrelated (e.g. "What is frontend development?"), I’ll respectfully reply:
“Sorry, I can’t answer that. Please ask something related to MAK’s work or skills.”

Want to know about a specific project or work? It’s available in the Portfolio > Projects section.
"""
)

# ✨ On chat start
@cl.on_chat_start
async def handle_start():
    cl.user_session.set("history", [])
    await cl.Message(content="👋 Hello! I'm MAK Assistant. How can I help you today ").send()

# 💬 Handle incoming message
@cl.on_message
async def handle_message(message: cl.Message):
    history = cl.user_session.get("history")
    history.append({"role": "user", "content": message.content})

    msg = cl.Message(content="")
    await msg.send()

    # 🧠 Run Agent with history as input
    result = Runner.run_streamed(
        agent,
        input=history,
        run_config=config
    )

    # 📤 Stream the agent response
    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            await msg.stream_token(event.data.delta)

    # 🧾 Add assistant reply to history
    history.append({"role": "assistant", "content": result.final_output})
    cl.user_session.set("history", history)
