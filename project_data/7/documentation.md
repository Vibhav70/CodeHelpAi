Project Documentation

This document provides a high-level overview of the codebase, generated from AI-powered summaries.

File: D:\Projects\Xbot\x_agent\core\agents\research_agent.py

Classes

class ResearchAgent

Summary: This Python code defines a `ResearchAgent` class that uses the Tavily API to perform web searches, specifically targeting educational, governmental, and organizational websites. It retrieves and sorts search results based on their relevance score, returning the top 5 results.

 Full Source Code:

python

class ResearchAgent:

    def __init__(self):
        self.client = TavilyClient(api_key=Config.TAVILY_API_KEY)

    async def search(self, query: str) -> List[Dict]:
        """Search with Tavily including Gemini-optimized params"""
        response = await self.client.search_async(
            query=f"{query} site:.edu OR site:.gov OR site:.org",
            search_depth=Config.TAVILY_SEARCH_DEPTH,
            include_raw_content=True,
            include_answer=True,
            max_results=5
        )
        return sorted(
            response["results"],
            key=lambda x: x["score"],
            reverse=True
        )

File: D:\Projects\Xbot\x_agent\core\agents\filter_agent.py

Classes

class TrendFilter

Summary: This code defines a `TrendFilter` class with a `filter` method that takes a list of trends and returns a new list containing only the trends that contain at least one allowed category (case-insensitive) and do not contain any blacklisted words (case-insensitive). Essentially, it filters a list of trends based on inclusion and exclusion criteria.

 Full Source Code:

python

class TrendFilter:
    def filter(self, trends: list) -> list:
        return [
            t for t in trends
            if (any(cat in t.lower() for cat in ALLOWED_CATEGORIES))
            and not any(bl in t.lower() for bl in BLOCKLIST)
        ]

File: D:\Projects\Xbot\x_agent\core\workflows.py

Standalone Functions

check_approval()

Summary: This function, `check_approval`, takes a state dictionary as input and returns a string indicating the next action based on the "approval_status" key in the state. It returns "end" if approved, "revise" if revision is needed, and "review" otherwise.

python

def check_approval(state: State) -> str:
    if state["approval_status"] == "approved":
        return "end"
    elif state["approval_status"] == "revise":
        return "revise"
    else:
        return "review"

Classes

class State

Summary: This code defines a `State` type using `TypedDict` to represent the structure of a state object. The state object contains information about trends, context, a tweet draft, and its approval status, likely used for managing a process involving trending topics and tweet generation.

 Full Source Code:

python

class State(TypedDict):
    trends: list[str]
    current_trend: str
    context: list[dict]
    tweet_draft: str
    approval_status: str

File: D:\Projects\Xbot\x_agent\core\agents\trend_agent.py

Classes

class TrendAgent

Summary: This code defines a `TrendAgent` class that uses the Twitter API v1.1 to fetch and filter trending topics for a given location (WOEID), prioritizing trends with significant tweet volume and excluding promoted content. It returns a list of the top 5 most relevant trend names.

 Full Source Code:

python

class TrendAgent:
    def __init__(self):
        # Initialize Twitter API v1.1 client
        self.auth = tweepy.OAuth1UserHandler(
            consumer_key=os.getenv("TWITTER_API_KEY"),
            consumer_secret=os.getenv("TWITTER_API_SECRET"),
            access_token=os.getenv("TWITTER_ACCESS_TOKEN"),
            access_token_secret=os.getenv("TWITTER_ACCESS_SECRET")
        )
        self.api = tweepy.API(self.auth)

    def get_trends(self, woeid: int = INDIA_WOEID) -> List[dict]:
        """
        Fetch trending topics for a specific WOEID using Twitter API v1.1
        Returns list of trend objects with name, url, tweet_volume etc.
        """
        try:
            trends = self.api.get_place_trends(id=woeid)
            return self._filter_trends(trends[0]["trends"])
        except tweepy.TweepyException as e:
            print(f"Twitter API Error: {e}")
            return []

    def _filter_trends(self, trends: List[dict]) -> List[dict]:
        """
        Filter trends to:
        - Exclude promoted content
        - Include only trends with significant volume (when available)
        - Limit to top 5 most relevant
        """
        filtered = [
            t for t in trends 
            if not t["promoted_content"] and 
               (t["tweet_volume"] is None or t["tweet_volume"] > 10000)
        ]
        return sorted(
            filtered,
            key=lambda x: x["tweet_volume"] if x["tweet_volume"] else 0,
            reverse=True
        )[:5]

    async def fetch_trend_names(self) -> List[str]:
        """Get just the trend names (compatibility with existing code)"""
        trends = self.get_trends()
        return [t["name"] for t in trends if not t["name"].startswith(("#", "@"))]

File: D:\Projects\Xbot\x_agent\config.py

Classes

class Config

Summary: This code defines a `Config` class that stores and manages configuration settings for various services like Twitter, Telegram, Gemini, News API, Tavily, and Redis, retrieving values from environment variables. It also includes lists for filtering trends based on allowed categories and a blocklist, along with a `validate` method to ensure required environment variables are set.

 Full Source Code:

python

class Config:
    # Twitter
    TWITTER_BEARER_TOKEN: str = os.getenv("TWITTER_BEARER_TOKEN")
    TWITTER_API_CREDS: dict = {
        "api_key": os.getenv("TWITTER_API_KEY"),
        "api_secret": os.getenv("TWITTER_API_SECRET"),
        "access_token": os.getenv("TWITTER_ACCESS_TOKEN"),
        "access_secret": os.getenv("TWITTER_ACCESS_SECRET")
    }
    INDIA_WOEID: Final[int] = int(os.getenv("INDIA_WOEID", 23424848))
    
    # Telegram
    TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN")
    TELEGRAM_CHAT_ID: str = os.getenv("TELEGRAM_CHAT_ID")
    
    # Gemini
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY")
    GEMINI_MODEL: str = "gemini-1.5-pro"  # or "gemini-pro"
    GEMINI_SAFETY_SETTINGS = {
        "HARASSMENT": "block_none",
        "HATE_SPEECH": "block_none",
        "SEXUAL": "block_none",
        "DANGEROUS": "block_none"
    }
    
    @staticmethod
    def validate():
        required = [
            # ... replace OPENAI_API_KEY with:
            "GEMINI_API_KEY"
        ]
    # News API
    NEWS_API_KEY: str = os.getenv("NEWS_API_KEY")

    TAVILY_API_KEY: str = os.getenv("TAVILY_API_KEY")
    TAVILY_SEARCH_DEPTH: str = "advanced"  # "basic" or "advanced"
    TAVILY_INCLUDE_RAW_CONTENT: bool = True
    
    @staticmethod
    def validate():
        required = [
            # ... other required vars
            "TAVILY_API_KEY"  # Add Tavily to required
        ]
    
    # Redis
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    
    # Trend Filtering
    ALLOWED_CATEGORIES: List[str] = [
        "tech", "technology", "ai", "programming",
        "book", "books", "literature",
        "sports", "cricket", "football"
    ]
    
    BLOCKLIST: List[str] = [
        "politics", "election", "modi", "congress",
        "religious", "controversy"
    ]
    
    @staticmethod
    def validate():
        """Check required env vars"""
        required = [
            "TWITTER_BEARER_TOKEN",
            "OPENAI_API_KEY",
            "TELEGRAM_BOT_TOKEN"
        ]
        for var in required:
            if not os.getenv(var):
                raise ValueError(f"Missing required environment variable: {var}")

File: D:\Projects\Xbot\x_agent\core\agents\tweet_agent.py

Classes

class GeminiAgent

Summary: This code defines a `GeminiAgent` class that leverages the Gemini AI model to generate viral tweets based on a given trend and relevant research. It formats the research, constructs a prompt with specific guidelines, and then uses the Gemini model to generate a tweet, returning the generated text.

 Full Source Code:

python

class GeminiAgent:
    def __init__(self):
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(Config.GEMINI_MODEL)
        self.safety_settings = Config.GEMINI_SAFETY_SETTINGS

    async def generate_tweet(self, trend: str, research: List[Dict]) -> str:
        """Generate tweet using Gemini with research context"""
        research_str = "

".join(
            f"📌 {res['title']} (Relevance: {res['score']}/100)

"
            f"{res['content'][:200]}...

🔗 {res['url']}

" 
            for res in research[:3]  # Top 3 sources
        )

        response = await self.model.generate_content_async(
            f"""Create a viral tweet about '{trend}' using this research:
            {research_str}
            
            Guidelines:
            1. Start with eye-catching hook (emoji + stat/question)
            2. Keep under 250 characters
            3. Include 2-3 hashtags
            4. Use casual, engaging tone
            """,
            safety_settings=self.safety_settings
        )
        
        return response.text

File: D:\Projects\Xbot\x_agent\services\telegram.py

Classes

class TelegramBot

Summary: This code defines a `TelegramBot` class that facilitates tweet review workflows by sending tweet drafts to Telegram users for approval or revision via specific commands, storing pending reviews and processing user responses accordingly. It uses a Telegram bot to send messages containing tweet drafts and interprets user replies starting with "/approve" or "/edit" to determine the next action.

 Full Source Code:

python

class TelegramBot:
    def __init__(self):
        self.bot = Bot(token=TELEGRAM_BOT_TOKEN)
        self.pending_reviews = {}  # {chat_id: (tweet, context)}

    async def send_for_review(self, chat_id: int, tweet: str):
        """Send tweet draft to user"""
        await self.bot.send_message(
            chat_id=chat_id,
            text=f"**Tweet Draft**

{tweet}

Reply:

- '/approve' to post

- '/edit [suggestions]' to revise",
            parse_mode="Markdown"
        )
        self.pending_reviews[chat_id] = tweet

    async def handle_response(self, update: Update):
        """Process user reply"""
        text = update.message.text
        chat_id = update.message.chat_id
        
        if text.startswith("/approve"):
            return {"status": "approved", "tweet": self.pending_reviews.pop(chat_id)}
        elif text.startswith("/edit"):
            return {"status": "revise", "feedback": text[6:].strip()}