# StreamQ - TODO List

## ✅ Completed

### Project Setup
- [x] Initialize Python project with uv
- [x] Set up project structure (src/stream_q/)
- [x] Configure dependencies (sentence-transformers, numpy, twitchio)
- [x] Create CLAUDE.md documentation
- [x] Configure environment variables (.env.example)

### FAQ Semantic Search (MVP)
- [x] Implement FAQManager with sentence-transformers
- [x] Add support for multiple question variations per FAQ
- [x] Implement cosine similarity matching
- [x] Add confidence threshold filtering (default: 0.7)
- [x] Create demo script to test matching
- [x] Test and validate embedding quality

## 🚧 In Progress

_Nothing currently in progress_

## 📋 Planned

### Twitch Integration
- [ ] Connect to Twitch IRC using TwitchIO
- [ ] Listen to chat messages in configured channel(s)
- [ ] Detect questions from viewers
- [ ] Send automated responses to chat

### Anti-Spam & Rate Limiting
- [ ] Implement cooldown between bot responses
- [ ] Add per-user cooldown tracking
- [ ] Implement max messages per minute limit
- [ ] Add duplicate question detection (don't answer same question twice in short time)

### FAQ Management
- [ ] Move FAQ entries to JSON file instead of hardcoded
- [ ] Create FAQ CRUD utilities (add/edit/remove entries)
- [ ] Add FAQ reload command without restarting bot
- [ ] Support FAQ categories/tags

### Logging & Monitoring
- [ ] Set up structured logging (questions asked, matches found, confidence scores)
- [ ] Log all bot responses for review
- [ ] Create simple stats dashboard (most asked questions, match rate, etc.)
- [ ] Add debug mode for testing

### Improvements & Optimizations
- [ ] Cache embeddings to avoid regenerating on restart
- [ ] Add support for different embedding models
- [ ] Implement question preprocessing (lowercase, punctuation normalization)
- [ ] Add multi-language support

### Advanced Features (Future)
- [ ] RAG implementation: LLM reformulation + synthesis for complex questions
- [ ] Support multiple FAQs above threshold → combine answers
- [ ] Add command for users to trigger bot (!faq, !help, etc.)
- [ ] Support for follow-up questions with context
- [ ] Web UI for FAQ management

## 🎯 Current Focus

**Next milestone:** Twitch integration - Connect bot to Twitch chat and implement basic message listening and response functionality.

## 📝 Notes

- Confidence threshold of 0.7 works well with multiple question variations
- Multiple question variations per FAQ significantly improve match accuracy
- Model: sentence-transformers/all-MiniLM-L6-v2 (lightweight and fast)
