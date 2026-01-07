"""FAQ Manager with semantic search using sentence transformers."""

from typing import Optional
import numpy as np
from sentence_transformers import SentenceTransformer


class FAQManager:
    """Manages FAQ entries and performs semantic search using embeddings."""

    def __init__(self, faq_entries: list[dict], confidence_threshold: float = 0.7):
        """Initialize FAQ manager with entries and load the embedding model.

        Args:
            faq_entries: List of dicts with 'questions' (list[str]) and 'answer' (str)
            confidence_threshold: Minimum similarity score to return a match (0-1)
        """
        self.confidence_threshold = confidence_threshold

        # Load the sentence transformer model
        print("Loading sentence-transformers model...")
        self.model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        print("Model loaded successfully!")

        # Process FAQ entries and flatten question variations
        self.faq_questions = []  # All question variations (flattened)
        self.faq_to_entry = []  # Maps each question back to its FAQ entry

        for entry in faq_entries:
            # Only support "questions" format (list of question variations)
            if "questions" not in entry:
                raise ValueError("FAQ entry must have 'questions' key with a list of question variations")

            questions = entry["questions"]

            # Add all variations for this FAQ
            for question in questions:
                self.faq_questions.append(question)
                self.faq_to_entry.append(entry)

        # Generate embeddings for all question variations
        total_questions = len(self.faq_questions)
        total_entries = len(faq_entries)
        print(f"Generating embeddings for {total_entries} FAQ entries ({total_questions} question variations)...")
        self.faq_embeddings = self.model.encode(self.faq_questions, convert_to_numpy=True)
        print("Embeddings generated!")

    def find_answer(self, question: str) -> Optional[dict]:
        """Find the best matching FAQ answer for a given question.

        Args:
            question: The user's question to match

        Returns:
            Dict with 'matched_question', 'answer', and 'confidence' if match found, else None
        """
        # Generate embedding for the input question
        question_embedding = self.model.encode([question], convert_to_numpy=True)[0]

        # Calculate cosine similarity with all FAQ embeddings
        similarities = self._cosine_similarity(question_embedding, self.faq_embeddings)

        # Find the best match
        best_idx = np.argmax(similarities)
        best_similarity = similarities[best_idx]

        # Return match if confidence is above threshold
        if best_similarity >= self.confidence_threshold:
            matched_entry = self.faq_to_entry[best_idx]
            matched_question = self.faq_questions[best_idx]

            return {
                "matched_question": matched_question,
                "answer": matched_entry["answer"],
                "confidence": float(best_similarity),
            }

        return None

    @staticmethod
    def _cosine_similarity(vec1: np.ndarray, vec2: np.ndarray) -> np.ndarray:
        """Calculate cosine similarity between a vector and a matrix of vectors.

        Args:
            vec1: Single embedding vector (1D array)
            vec2: Matrix of embedding vectors (2D array)

        Returns:
            Array of similarity scores
        """
        # Normalize vectors
        vec1_norm = vec1 / np.linalg.norm(vec1)
        vec2_norm = vec2 / np.linalg.norm(vec2, axis=1, keepdims=True)

        # Calculate dot product
        return np.dot(vec2_norm, vec1_norm)
