import json
import logging
import textwrap
from pathlib import Path

from dotenv import load_dotenv
from livekit.agents import (
    Agent,
    AgentServer,
    AgentSession,
    JobContext,
    JobProcess,
    RunContext,
    cli,
    function_tool,
    inference,
    room_io,
)
from livekit.plugins import ai_coustics, silero
from livekit.plugins.turn_detector.multilingual import MultilingualModel

from knowledge_base import KnowledgeBase
from lead_storage import LeadStorage

logger = logging.getLogger("agent")

load_dotenv(".env.local")

# Initialize knowledge base and lead storage
knowledge_base = KnowledgeBase()
lead_storage = LeadStorage()


class FounderAssistant(Agent):
    """Voice AI agent representing Maneuver's founder."""
    
    def __init__(self) -> None:
        super().__init__(
            llm=inference.LLM(model="openai/gpt-4o"),
            instructions=textwrap.dedent(
                """\
                You are Husain Topiwala, founder of Maneuver. You bring enterprise AI thinking to the businesses that actually run the economy — SMBs that typically get priced out of Fortune 500-level AI consulting.
                
                You're having a natural voice conversation with a potential client. Your personality is:
                - Warm, confident, and genuinely curious
                - Technical but not academic — you explain AI in business terms
                - Direct but not pushy — you've built real systems at JP Morgan, Vanguard, Deloitte
                - You ask thoughtful follow-up questions about their business metrics
                - You share relevant examples from enterprise AI work when appropriate
                - You sound like a real founder who's built real systems, not a chatbot or form
                
                # Your Two Jobs
                
                ## 1. Discovery Mode (Default)
                When someone first connects, introduce yourself briefly and start a discovery conversation. You want to understand:
                - Who they are (name, company, role)
                - What business problem they're trying to solve
                - What business metrics they care about (revenue, cost, time, quality, customer satisfaction)
                - Whether they're thinking about AI or already trying to implement it
                - What they've tried so far (if anything)
                - Their timeline and budget expectations
                
                Ask these questions naturally over the course of the conversation. Don't make it feel like a form or checklist. Branch based on their answers. Show genuine interest.
                
                If they say something surprising or interesting, explore it before moving to the next question. Dig deeper. Ask follow-ups.
                
                When you learn something important, use the update_lead_field tool to capture it.
                
                After answering a question about Maneuver, naturally return to discovery with a transition like "but tell me more about your situation..." or "anyway, back to you..." or "so what's the business metric you're trying to move?"
                
                ## 2. Q&A Mode
                If they ask YOU questions about Maneuver (services, process, pricing, case studies, team, mission, vision), answer confidently using the get_maneuver_info tool. Be specific and conversational.
                
                Key points to emphasize when relevant:
                - AI is an operating shift, not a feature
                - Every recommendation is tied to a business metric
                - Systems are designed to be owned by their team, not create dependency
                - You lead every engagement personally
                - No junior consultants, no offshore handoffs
                - Enterprise AI thinking without enterprise budgets
                
                Switch fluidly between discovery and Q&A within the same conversation. If they ask about your services mid-discovery, answer them, then naturally return to discovery.
                
                # Output Rules (Voice Conversation)
                
                - Respond in plain text only. No markdown, lists, JSON, or formatting.
                - Keep responses brief: 1-3 sentences at a time. Ask one question at a time.
                - Spell out numbers, phone numbers, email addresses.
                - Avoid acronyms with unclear pronunciation.
                - Don't mention tool names or internal processes.
                - Sound natural and conversational.
                
                # When to End Discovery
                
                When you've gathered the core information (name, company, problem, business metrics, timeline, budget) and they seem ready to move forward or want next steps, use the end_discovery tool. This will save their information and show them a summary.
                
                # Visual Layer (Bonus)
                
                When appropriate, you can trigger visual elements:
                - If they ask "what services do you offer?", call show_services_slide() as you start answering
                - If they ask about a specific service, call show_service_detail(service_name)
                - If they ask "what's your process?" or "how does it work?", call show_process_diagram()
                
                These are optional enhancements. The conversation should work perfectly even without them.
                
                # Opening
                
                Start with something like: "Hey! I'm Husain, founder of Maneuver. Thanks for taking the time to chat. I'd love to learn a bit about what you're working on and see if we might be a good fit. First off, what's your name?"
                
                Keep it natural and conversational throughout.
                """
            ),
        )
    
    @function_tool
    async def update_lead_field(self, context: RunContext, field: str, value: str):
        """
        Capture and store information about the lead during discovery.
        
        Use this tool whenever you learn something important about the prospect:
        - Their name, company, or role
        - The problem or challenge they're facing
        - Their timeline or budget
        - What solutions they've tried
        
        Args:
            field: The type of information (e.g., 'name', 'company', 'problem', 'timeline', 'budget', 'current_solutions')
            value: The actual information to store
        """
        logger.info(f"Capturing lead field: {field} = {value}")
        
        success = lead_storage.update_field(field, value)
        
        if success:
            # TODO: Forward to frontend via RPC for visual update (bonus feature)
            # await context.room.local_participant.perform_rpc(
            #     destination_identity="frontend",
            #     method="updateLeadField",
            #     payload=json.dumps({"field": field, "value": value})
            # )
            return f"Captured: {field}"
        else:
            return "Failed to capture information"
    
    @function_tool
    async def get_maneuver_info(self, context: RunContext, topic: str):
        """
        Retrieve information about Maneuver to answer the prospect's questions.
        
        Use this when they ask about:
        - Services offered
        - Pricing or costs
        - Process or how it works
        - Case studies or results
        - Team or founder background
        - What Maneuver does
        
        Args:
            topic: What they're asking about (e.g., 'services', 'pricing', 'process', 'case studies', 'team')
        """
        logger.info(f"Retrieving knowledge about: {topic}")
        
        info = knowledge_base.get_info(topic)
        
        if info:
            return info
        else:
            return "I don't have specific information about that, but I'm happy to discuss it further or connect you with our team."
    
    @function_tool
    async def end_discovery(self, context: RunContext):
        """
        Signal that discovery is complete and save the captured lead information.
        
        Use this when:
        - You've gathered the core discovery information
        - The prospect is ready for next steps
        - They want to schedule a follow-up or move forward
        
        This will save their information and show them a summary of what was captured.
        """
        logger.info("Ending discovery and saving lead data")
        
        # Save lead data
        session_id = context.room.name if hasattr(context, 'room') else None
        filepath = lead_storage.save_lead(session_id)
        
        # Get summary
        summary = lead_storage.get_summary()
        
        logger.info(f"Lead data saved to: {filepath}")
        logger.info(f"Summary:\n{summary}")
        
        # TODO: Forward to frontend via RPC to show summary view (bonus feature)
        # await context.room.local_participant.perform_rpc(
        #     destination_identity="frontend",
        #     method="showDiscoverySummary",
        #     payload=json.dumps(lead_storage.get_lead_data())
        # )
        
        return f"Discovery complete. Information saved. Summary: {summary}"
    
    @function_tool
    async def show_services_slide(self, context: RunContext):
        """
        Trigger the frontend to display a visual slide of Maneuver's services.
        
        Use this when they ask "what services do you offer?" or similar questions about your offerings.
        
        This is a bonus visual feature. The conversation works without it.
        """
        logger.info("Triggering services slide visual")
        
        # TODO: Forward to frontend via RPC (bonus feature)
        # await context.room.local_participant.perform_rpc(
        #     destination_identity="frontend",
        #     method="showServicesSlide",
        #     payload=json.dumps({})
        # )
        
        return "Services slide triggered"
    
    @function_tool
    async def show_service_detail(self, context: RunContext, service_name: str):
        """
        Trigger the frontend to display detailed information about a specific service.
        
        Use this when they ask about a specific service like "tell me more about GTM strategy" or "what's included in Revenue Operations?"
        
        Args:
            service_name: The service they're asking about (e.g., 'GTM Strategy', 'Sales Playbook', 'Revenue Operations', 'Fractional CRO')
        
        This is a bonus visual feature. The conversation works without it.
        """
        logger.info(f"Triggering service detail visual for: {service_name}")
        
        # TODO: Forward to frontend via RPC (bonus feature)
        # await context.room.local_participant.perform_rpc(
        #     destination_identity="frontend",
        #     method="showServiceDetail",
        #     payload=json.dumps({"service": service_name})
        # )
        
        return f"Service detail for {service_name} triggered"
    
    @function_tool
    async def show_process_diagram(self, context: RunContext):
        """
        Trigger the frontend to display Maneuver's process diagram.
        
        Use this when they ask "what's your process?", "how does it work?", or "what are the steps?"
        
        This is a bonus visual feature. The conversation works without it.
        """
        logger.info("Triggering process diagram visual")
        
        # TODO: Forward to frontend via RPC (bonus feature)
        # await context.room.local_participant.perform_rpc(
        #     destination_identity="frontend",
        #     method="showProcessDiagram",
        #     payload=json.dumps({})
        # )
        
        return "Process diagram triggered"


server = AgentServer()


def prewarm(proc: JobProcess):
    """Prewarm models before agent starts."""
    proc.userdata["vad"] = silero.VAD.load()


server.setup_fnc = prewarm


@server.rtc_session(agent_name="maneuver-founder")
async def maneuver_founder_agent(ctx: JobContext):
    """Main agent session handler."""
    # Logging setup
    ctx.log_context_fields = {
        "room": ctx.room.name,
    }
    
    logger.info(f"Starting Maneuver founder agent in room: {ctx.room.name}")
    
    # Set up voice AI pipeline
    session = AgentSession(
        # Speech-to-text
        stt=inference.STT(model="deepgram/nova-3", language="multi"),
        # Text-to-speech
        tts=inference.TTS(
            model="cartesia/sonic-3", 
            voice="9626c31c-bec5-4cca-baa8-f8ba9e84c8bc"  # Professional male voice
        ),
        # Turn detection
        turn_detection=MultilingualModel(),
        vad=ctx.proc.userdata["vad"],
        # Preemptive generation for lower latency
        preemptive_generation=True,
    )
    
    # Start the session
    await session.start(
        agent=FounderAssistant(),
        room=ctx.room,
        room_options=room_io.RoomOptions(
            audio_input=room_io.AudioInputOptions(
                noise_cancellation=ai_coustics.audio_enhancement(
                    model=ai_coustics.EnhancerModel.QUAIL_VF_S
                ),
            ),
        ),
    )
    
    # Join the room
    await ctx.connect()
    
    logger.info("Maneuver founder agent connected and ready")


if __name__ == "__main__":
    cli.run_app(server)
