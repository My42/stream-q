"""Test script to see all confidence scores."""

import sys
sys.path.insert(0, '/Users/vmqt/projects/stream-q/ai/src')

from stream_q.faq import FAQManager

# Hardcoded FAQ entries
faq_entries = [
    {"question": "What is the stream schedule?", "answer": "I stream Monday, Wednesday, Friday at 7 PM EST"},
    {"question": "What game are you playing?", "answer": "Currently playing Elden Ring"},
    {"question": "Can I join your Discord?", "answer": "Yes! Link is discord.gg/example"},
    {"question": "Do you take game suggestions?", "answer": "Yes, feel free to suggest games in chat!"},
    {"question": "What are your PC specs?", "answer": "RTX 4090, i9-13900K, 32GB RAM"},
]

# Initialize with very low threshold to see all scores
faq_manager = FAQManager(faq_entries, confidence_threshold=0.0)

test_questions = [
    "What is the stream schedule?",
    "When do you go live?",
    "What game are we playing today?",
    "Discord link?",
    "What's your computer setup?",
    "What's for dinner?",
]

print("\nAll confidence scores:\n")
for question in test_questions:
    result = faq_manager.find_answer(question)
    if result:
        print(f'Q: "{question}"')
        print(f'   Best match: "{result["question"]}"')
        print(f'   Confidence: {result["confidence"]:.3f}\n')
