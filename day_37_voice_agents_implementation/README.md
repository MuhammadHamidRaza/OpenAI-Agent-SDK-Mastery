# Day 37: `Voice` Agents Implementation

[![Proprietary License](https://img.shields.io/badge/license-proprietary-red.svg)](../LICENSE)

---

### **Course Overview**

Welcome to Day 37 of the **OpenAI Agent SDK Mastery** course! Yesterday, you built a responsive, real-time agent. Today, we take the next logical step by **implementing a fully functional voice-enabled agent**. Building upon the concepts introduced on Day 27 (`Voice` Agents Intro), you'll learn how to integrate Speech-to-Text (STT) and Text-to-Speech (TTS) services with your AI agent to create a truly natural, spoken conversational experience. This session will focus on the practical aspects of connecting these components, managing the voice pipeline, and ensuring a fluid, interactive dialogue, making your agents capable of listening and speaking with users.

---

## Recap: The Voice Agent Pipeline

Recall the core components of a voice agent:

1.  **Speech-to-Text (STT):** Converts user's spoken audio into text.
2.  **AI Agent (LLM + Tools + Logic):** Processes the text, reasons, and generates a text response.
3.  **Text-to-Speech (TTS):** Converts the agent's text response into spoken audio.

Our goal today is to connect these pieces, focusing on how the OpenAI Agents SDK fits into this pipeline.

---

## Integrating STT and TTS Services

While the OpenAI Agents SDK itself doesn't provide STT/TTS capabilities directly, it seamlessly integrates with external services and libraries that do. Popular choices include:

*   **OpenAI's Whisper (STT) and Text-to-Speech API (TTS):** High-quality, easy to integrate.
*   **Google Cloud Speech-to-Text / Text-to-Speech:** Robust, scalable, and widely used.
*   **Amazon Polly (TTS) / Transcribe (STT):** AWS offerings.
*   **Deepgram, AssemblyAI (STT):** Specialized for speech recognition.
*   **Local Libraries:** `SpeechRecognition` (for STT, often uses Google Web Speech API), `gTTS` (for TTS, uses Google Translate).

For this implementation, we will use conceptual functions to represent calls to these external services, allowing us to focus on the agent integration logic.

---

## Practical Implementation: A Voice-Enabled Assistant

Let's build a voice assistant that can answer questions and use a simple tool, all through spoken commands.

```python
import asyncio
import os
# import speech_recognition as sr # For actual STT
# from gtts import gTTS # For actual TTS
# import pygame # For playing audio (requires pygame.mixer.init())

from agents import Agent, Runner
from agents.tools import function_tool

# Ensure API key is set
if "OPENAI_API_KEY" not in os.environ:
    print("Please set the OPENAI_API_KEY environment variable.")
    exit()

# ---
# Conceptual STT and TTS Functions ---
# In a real application, these would call actual APIs or libraries
async def conceptual_stt_service(audio_data) -> str:
    """Simulates an asynchronous Speech-to-Text service."""
    print("[STT Service]: Processing audio...")
    await asyncio.sleep(1) # Simulate network/processing delay
    # For demonstration, we'll just return a hardcoded text or the input as text
    if "hello" in audio_data.lower():
        return "Hello there"
    elif "time" in audio_data.lower():
        return "What time is it"
    elif "weather" in audio_data.lower():
        return "What is the weather like"
    return audio_data # Treat input as already transcribed for simplicity

async def conceptual_tts_service(text_to_speak: str) -> bytes:
    """Simulates an asynchronous Text-to-Speech service."""
    print(f"[TTS Service]: Synthesizing audio for: '{text_to_speak[:30]}...'")
    await asyncio.sleep(1) # Simulate network/processing delay
    return b"simulated_audio_bytes" # In real app, this would be actual audio bytes

async def play_audio(audio_bytes: bytes):
    """Simulates playing audio bytes."""
    # In a real app, you'd use a library like pygame, simpleaudio, or pydub
    print("[Audio Player]: Playing synthesized speech...")
    # Example with pygame (requires pygame.mixer.init() and loading sound)
    # from io import BytesIO
    # sound = pygame.mixer.Sound(BytesIO(audio_bytes))
    # sound.play()
    # while pygame.mixer.get_busy():
    #     await asyncio.sleep(0.1)
    await asyncio.sleep(1) # Simulate audio playback time

# ---
# Custom Tool for Voice Agent ---
@function_tool
def get_current_time_voice(timezone: str = "UTC") -> str:
    """Returns the current time in a specified timezone for a voice agent."""
    from datetime import datetime
    import pytz
    try:
        tz = pytz.timezone(timezone)
        now = datetime.now(tz)
        return f"The current time in {timezone.replace('_', ' ')} is {now.strftime('%I:%M %p on %A, %B %d, %Y')}."
    except pytz.UnknownTimeZoneError:
        return f"I'm sorry, I don't recognize the timezone {timezone}."

# Define the Voice Agent
voice_agent = Agent(
    name="VoiceAssistant",
    instructions=(
        "You are a friendly and helpful voice assistant. "
        "You can answer general questions and tell the current time. "
        "Speak clearly and concisely. "
        "Use the 'get_current_time_voice' tool when asked about the time. "
    ),
    tools=[get_current_time_voice]
)

async def voice_interaction_loop():
    print("\n--- Voice Assistant Ready ---\n")
    print("Say 'exit' to quit.")

    while True:
        # Simulate capturing audio input (e.g., from microphone)
        # In a real app: recognizer = sr.Recognizer(); with sr.Microphone() as source: audio = recognizer.listen(source)
        user_audio_input = input("You (type your spoken command): ") # User types what they would say
        if user_audio_input.lower() == 'exit':
            break

        # Step 1: STT - Convert audio to text
        transcribed_text = await conceptual_stt_service(user_audio_input)
        print(f"[Transcribed]: {transcribed_text}")

        # Step 2: Agent processes text and generates response (streaming for real-time feel)
        agent_response_text = ""
        print("Agent: ", end="", flush=True)
        with Runner.run_streamed(voice_agent, transcribed_text) as stream:
            async for event in stream:
                if hasattr(event, 'text'):
                    print(event.text, end="", flush=True)
                    agent_response_text += event.text
                elif hasattr(event, 'tool_name'):
                    print(f"\n[Agent using tool: {event.tool_name}]")
                elif hasattr(event, 'output'):
                    print(f"\n[Tool output: {event.output}]")
            final_result = stream.get_final_result()
            agent_response_text = final_result.final_output # Ensure we get the complete final output
        print("\n")

        # Step 3: TTS - Convert agent's text response to audio and play
        if agent_response_text:
            synthesized_audio_bytes = await conceptual_tts_service(agent_response_text)
            await play_audio(synthesized_audio_bytes)

    print("Goodbye!")

if __name__ == "__main__":
    # For actual audio playback, you might need to initialize pygame mixer
    # pygame.mixer.init()
    asyncio.run(voice_interaction_loop())

```

**Explanation:**

*   **Conceptual STT/TTS/Audio Playback:** We use `async` functions (`conceptual_stt_service`, `conceptual_tts_service`, `play_audio`) to simulate the asynchronous nature of real STT/TTS API calls and audio playback. In a real application, you would replace these with calls to actual libraries or services.
*   **`get_current_time_voice` Tool:** A custom tool designed to provide time information, which the voice agent can use.
*   **`voice_agent` Definition:** The agent is instructed to be a friendly voice assistant and to use the time tool.
*   **`voice_interaction_loop`:** This `async` function orchestrates the entire voice interaction:
    1.  It simulates capturing user audio (via `input()`).
    2.  Calls the conceptual STT service to get transcribed text.
    3.  Runs the `voice_agent` with the transcribed text, using `Runner.run_streamed()` for real-time output.
    4.  Collects the agent's full text response.
    5.  Calls the conceptual TTS service to synthesize audio from the agent's response.
    6.  Simulates playing the audio.

---

## Key Considerations for Voice Agent Implementation

*   **Latency:** Minimize latency at every stage (STT, LLM, TTS) for a fluid experience. Asynchronous operations are critical.
*   **Error Handling:** Robustly handle STT misinterpretations, LLM errors, and TTS failures.
*   **Barge-in/Interruption:** Implement logic to allow users to interrupt the agent mid-response.
*   **Voice Quality:** Choose high-quality TTS voices that sound natural and engaging.
*   **Microphone/Speaker Management:** Proper handling of audio input/output devices.
*   **Context Management:** Ensure the agent maintains context across turns, especially in multi-turn voice conversations.

---

## Key Takeaways

*   **Voice Agents** integrate STT, an AI agent (LLM), and TTS to enable natural spoken interactions.
*   The OpenAI Agents SDK provides the core agent logic, which seamlessly connects with external STT/TTS services.
*   Asynchronous programming and streaming are vital for achieving a responsive voice experience.
*   Implementing custom tools allows voice agents to perform actions based on spoken commands.

Today, you've built a voice-enabled agent, bringing your AI applications to life through natural conversation. Tomorrow, we'll embark on **Project 4: Real-time Stock Analyst**, combining real-time data processing with agent intelligence to provide live insights.