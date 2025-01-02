"""
Sample usage of the iMessage Analytics API and direct database access.
This file demonstrates both how to use the API as a client and how to use
the database accessor directly in your own code.
"""

import requests
import asyncio
from app.db.imessage import IMessageDB

# ============================================================================
# Example 1: Using the API as a client
# ============================================================================

def api_example():
    """Example of how to use the API endpoints."""
    # Replace with your actual API token
    TOKEN = "your_github_oauth_token"
    BASE_URL = "http://localhost:9000/api/v1"
    HEADERS = {"Authorization": f"Bearer {TOKEN}"}

    # Example 1: Get message statistics for a contact
    contact_id = "+1234567890"  # Replace with actual phone number or email
    response = requests.get(
        f"{BASE_URL}/analytics/contacts/{contact_id}/stats",
        headers=HEADERS
    )
    if response.status_code == 200:
        stats = response.json()
        print(f"\nMessage stats for {contact_id}:")
        print(f"Sent messages: {stats['sent']}")
        print(f"Received messages: {stats['received']}")

    # Example 2: Get word frequency analysis
    response = requests.get(
        f"{BASE_URL}/analytics/contacts/{contact_id}/word-frequency",
        headers=HEADERS,
        params={"limit": 5}  # Get top 5 most common words
    )
    if response.status_code == 200:
        word_stats = response.json()
        print(f"\nMost common words in conversation with {contact_id}:")
        for word_freq in word_stats["frequencies"]:
            print(f"{word_freq['word']}: {word_freq['count']} times")

# ============================================================================
# Example 2: Using the database accessor directly
# ============================================================================

def direct_db_example():
    """Example of how to use the database accessor directly."""
    # Using context manager for safe database access
    with IMessageDB() as db:
        contact_id = "+1234567890"  # Replace with actual phone number or email
        
        # Get message statistics
        stats = db.get_message_count_by_contact(contact_id)
        print(f"\nDirect DB access - Message stats for {contact_id}:")
        print(f"Sent messages: {stats['sent']}")
        print(f"Received messages: {stats['received']}")
        
        # Get word frequency
        word_frequencies = db.get_word_frequency(contact_id, limit=5)
        print(f"\nDirect DB access - Most common words:")
        for word, count in word_frequencies:
            print(f"{word}: {count} times")

# ============================================================================
# Example 3: Custom analysis using the database accessor
# ============================================================================

def custom_analysis_example():
    """Example of how to perform custom analysis using the database accessor."""
    from collections import defaultdict
    from datetime import datetime
    
    with IMessageDB() as db:
        contact_id = "+1234567890"  # Replace with actual phone number or email
        
        # Get all messages for time-based analysis
        session = db.SessionLocal()
        messages = (session.query(db.Message)
                   .filter(db.Message.handle_id == contact_id)
                   .all())
        
        # Example: Messages by hour of day
        messages_by_hour = defaultdict(int)
        for msg in messages:
            if msg.date:  # Unix timestamp
                hour = datetime.fromtimestamp(msg.date).hour
                messages_by_hour[hour] += 1
        
        print("\nCustom analysis - Messages by hour:")
        for hour in sorted(messages_by_hour.keys()):
            print(f"{hour:02d}:00 - {messages_by_hour[hour]} messages")

def main():
    print("=== iMessage Analytics API Examples ===")
    
    print("\n1. API Client Examples:")
    try:
        api_example()
    except Exception as e:
        print(f"API example failed: {e}")
    
    print("\n2. Direct Database Access Examples:")
    try:
        direct_db_example()
    except Exception as e:
        print(f"Direct DB example failed: {e}")
    
    print("\n3. Custom Analysis Example:")
    try:
        custom_analysis_example()
    except Exception as e:
        print(f"Custom analysis failed: {e}")

if __name__ == "__main__":
    main()