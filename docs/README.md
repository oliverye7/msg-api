# iMessage Analytics API Documentation

This API service provides analytics for iMessage conversations, allowing developers to extract insights from message history.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Authentication](#authentication)
3. [API Endpoints](#api-endpoints)
4. [Database Schema](#database-schema)
5. [Development](#development)

## Getting Started

### Prerequisites

- Python 3.8+
- Access to macOS iMessage database (`~/Library/Messages/chat.db`)
- GitHub account (for authentication)

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/msg-api.git
cd msg-api

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Quick Start

1. Set up environment variables:
```bash
export GITHUB_CLIENT_ID="your_github_client_id"
export GITHUB_CLIENT_SECRET="your_github_client_secret"
export SECRET_KEY="your_secret_key"
```

2. Run the server:
```bash
uvicorn app.main:app --reload --port 9000
```

3. Visit `http://localhost:9000/docs` for interactive API documentation.

## Authentication

The API uses GitHub OAuth for authentication. Users must authenticate before accessing any analytics endpoints.

1. Login endpoint: `/api/v1/auth/login/github`
2. Callback endpoint: `/api/v1/auth/github/callback`

After successful authentication, you'll receive a JWT token to use in subsequent requests.

## API Endpoints

### Message Statistics

```http
GET /api/v1/analytics/contacts/{contact_id}/stats
```

Returns message count statistics for a specific contact.

**Response:**
```json
{
    "sent": 42,
    "received": 24
}
```

### Word Frequency Analysis

```http
GET /api/v1/analytics/contacts/{contact_id}/word-frequency
```

Returns most common words used in conversations with a contact.

**Parameters:**
- `limit` (optional): Number of top words to return (default: 10)

**Response:**
```json
{
    "frequencies": [
        {
            "word": "hello",
            "count": 10
        },
        {
            "word": "world",
            "count": 8
        }
    ]
}
```

## Database Schema

The API interacts with the following iMessage database tables:

- `message`: Contains message content and metadata
- `handle`: Contains contact information
- `chat`: Contains conversation/thread information
- `chat_message_join`: Links messages to chats
- `chat_handle_join`: Links contacts to chats

For detailed schema information, see [database_schema.md](database_schema.md).

## Development

### Running Tests

```bash
# Run all tests
python -m pytest

# Run specific test file
python -m pytest app/tests/test_analytics.py

# Run with coverage
python -m pytest --cov=app
```

### Project Structure

```
app/
├── api/
│   └── v1/
│       └── endpoints/
│           ├── analytics.py  # Analytics endpoints
│           ├── auth.py       # Authentication endpoints
│           └── health.py     # Health check endpoint
├── core/
│   ├── auth.py              # Authentication logic
│   └── settings.py          # Application settings
├── db/
│   ├── imessage.py         # iMessage database accessor
│   └── session.py          # Database session management
├── models/
│   └── imessage.py         # SQLAlchemy models
└── schemas/
    └── analytics.py        # Pydantic models
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Write or update tests
5. Submit a pull request

For more detailed information, see [CONTRIBUTING.md](CONTRIBUTING.md).