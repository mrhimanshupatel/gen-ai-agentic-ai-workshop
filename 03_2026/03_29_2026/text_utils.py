"""
Text processing utilities for encoding and embedding examples.
This is a reusable Python module (.py file) with clean, production-ready functions.
"""

def clean_text(text):
    """Remove extra whitespace and convert to lowercase."""
    return " ".join(text.lower().split())

def count_words(text):
    """Count the number of words in text."""
    return len(text.split())

def get_text_stats(text):
    """
    Get comprehensive statistics about a text string.
    
    Args:
        text (str): Input text to analyze
        
    Returns:
        dict: Dictionary containing text statistics
    """
    cleaned = clean_text(text)
    return {
        "original_length": len(text),
        "cleaned_length": len(cleaned),
        "word_count": count_words(cleaned),
        "char_count": len(cleaned.replace(" ", "")),
        "avg_word_length": len(cleaned.replace(" ", "")) / max(count_words(cleaned), 1)
    }

if __name__ == "__main__":
    # This runs only when script is executed directly
    sample_text = "  Hello   WORLD!  This is an Example.  "
    print("Original:", repr(sample_text))
    print("Cleaned:", clean_text(sample_text))
    print("Stats:", get_text_stats(sample_text))
