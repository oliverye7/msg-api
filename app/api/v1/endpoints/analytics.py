from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, List
from app.db.imessage import IMessageDB
from app.core.auth import get_current_user
from app.schemas.analytics import MessageStats, WordFrequency, WordFrequencyList

router = APIRouter()

@router.get("/contacts/{contact_id}/stats", response_model=MessageStats)
async def get_contact_stats(
    contact_id: str,
    current_user = Depends(get_current_user)
) -> MessageStats:
    """Get message statistics for a specific contact.
    
    Args:
        contact_id: Phone number or email of the contact
        
    Returns:
        MessageStats containing sent and received message counts
    """
    try:
        with IMessageDB() as db:
            stats = db.get_message_count_by_contact(contact_id)
            return MessageStats(**stats)
    except FileNotFoundError:
        raise HTTPException(
            status_code=503,
            detail="iMessage database not accessible"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error accessing message data: {str(e)}"
        )

@router.get("/contacts/{contact_id}/word-frequency", response_model=WordFrequencyList)
async def get_word_frequency(
    contact_id: str,
    limit: int = 10,
    current_user = Depends(get_current_user)
) -> WordFrequencyList:
    """Get most common words used in conversations with a contact.
    
    Args:
        contact_id: Phone number or email of the contact
        limit: Number of top words to return (default: 10)
        
    Returns:
        WordFrequencyList containing word frequency data
    """
    try:
        with IMessageDB() as db:
            frequencies = db.get_word_frequency(contact_id, limit)
            word_freqs = [
                WordFrequency(word=word, count=count)
                for word, count in frequencies
            ]
            return WordFrequencyList(frequencies=word_freqs)
    except FileNotFoundError:
        raise HTTPException(
            status_code=503,
            detail="iMessage database not accessible"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error accessing message data: {str(e)}"
        )
