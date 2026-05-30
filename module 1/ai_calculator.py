def estimate_ai_cost(messages, model="claude-sonnet-4-6", price_per_million=3.00):
    total_chars = 0
    for message in messages:
        total_chars = total_chars + len(message)
    estimated_tokens = total_chars // 4
    cost = round((estimated_tokens / 1_000_000) * price_per_million, 6)
    print(f"Model    : {model}")
    print(f"Messages : {len(messages)}")
    print(f"Tokens   : ~{estimated_tokens}")
    print(f"Cost     : ${cost:.6f}")

estimate_ai_cost(["What is AI?", "How do I learn Python?", "Tell me about Claude."])