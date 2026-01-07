"""Demo script to test FAQ matching with embeddings."""

from stream_q.faq import FAQManager
from stream_q.utils import get_config


def main():
    """Run FAQ matching demo."""
    # Get configuration
    config = get_config()
    confidence_threshold = config["confidence_threshold"]

    # Hardcoded FAQ entries with multiple question variations
    faq_entries = [
        {
            "questions": [
                "What is the stream schedule?",
                "When do you stream?",
                "When do you go live?",
                "What time do you start streaming?",
                "What days do you stream?",
            ],
            "answer": "I stream Monday, Wednesday, Friday at 7 PM EST",
        },
        {
            "questions": [
                "What game are you playing?",
                "What game are we playing today?",
                "What's the current game?",
            ],
            "answer": "Currently playing Elden Ring",
        },
        {
            "questions": [
                "Can I join your Discord?",
                "Discord link?",
                "Where is the Discord?",
                "How do I join Discord?",
            ],
            "answer": "Yes! Link is discord.gg/example",
        },
        {
            "questions": [
                "Do you take game suggestions?",
                "Can I suggest a game?",
                "What about game requests?",
            ],
            "answer": "Yes, feel free to suggest games in chat!",
        },
        {
            "questions": [
                "What are your PC specs?",
                "What's your computer setup?",
                "What PC do you have?",
                "What are your specs?",
            ],
            "answer": "RTX 4090, i9-13900K, 32GB RAM",
        },
    ]

    # Initialize FAQ manager
    print(f"\n{'='*60}")
    print("StreamQ - FAQ Matching Demo")
    print(f"{'='*60}\n")

    faq_manager = FAQManager(faq_entries, confidence_threshold)

    print(f"\nConfidence threshold: {confidence_threshold}")
    print(f"\n{'='*60}\n")

    # Test questions
    test_questions = [
        "What is the stream schedule?",  # Exact match (in variations)
        "When do you go live?",  # Exact match (in variations)
        "What game are we playing today?",  # Exact match (in variations)
        "Discord link?",  # Exact match (in variations)
        "What's your computer setup?",  # Exact match (in variations)
        "streaming times?",  # Paraphrase (not in variations)
        "What's for dinner?",  # Unrelated
        "How's the weather?",  # Unrelated
    ]

    # Test each question
    for question in test_questions:
        print(f"Q: \"{question}\"")
        result = faq_manager.find_answer(question)

        if result:
            print(f"   Matched: \"{result['matched_question']}\"")
            print(f"   A: \"{result['answer']}\"")
            print(f"   Confidence: {result['confidence']:.2f}")
        else:
            print(f"   A: No match found (confidence too low)")

        print()

    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
