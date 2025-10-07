import os
import requests
import cohere
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import telegram
import schedule
import time

# --- Configuration ---
load_dotenv()
GUARDIAN_API_KEY = os.getenv("GUARDIAN_API_KEY")
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Initialize Cohere client
co = cohere.Client(COHERE_API_KEY)

# --- Step 1: Get News from The Guardian API ---
def get_guardian_news():
    """Fetches top 5 world news articles from The Guardian API."""
    print("Fetching latest news from The Guardian...")
    url = f"https://content.guardianapis.com/search?section=world&page-size=5&show-fields=bodyText&api-key={GUARDIAN_API_KEY}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        articles = response.json()['response']['results']
        # Return a list of dictionaries with title, url, and the full text
        return [{'title': a['webTitle'], 'url': a['webUrl'], 'text': a['fields']['bodyText']} for a in articles]
    except requests.exceptions.RequestException as e:
        print(f"Error fetching from The Guardian API: {e}")
        return []

# --- Step 2: Summarize with Cohere AI ---
def summarize_with_cohere(text):
    """Summarizes a block of text using Cohere."""
    print("  -> Summarizing with Cohere AI...")
    try:
        response = co.summarize(
            text=text,
            model='command',
            length='short',
            format='bullets'
        )
        return response.summary
    except Exception as e:
        return f"Could not summarize. Cohere API Error: {e}"

# --- Step 3: Send Notification via Telegram (Updated) ---
async def send_telegram_message(message):
    """Sends a message to your Telegram account."""
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    try:
        # Change parse_mode to 'HTML'
        await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message, parse_mode='HTML')
        print("Briefing sent successfully to Telegram!")
    except Exception as e:
        print(f"Failed to send Telegram message: {e}")

# --- Step 4: The Main Job Function (Updated) ---
def run_briefing_job():
    """The main function that runs the entire pipeline."""
    import asyncio
    
    # First, send an introductory message
    intro_message = "<b>📰 Your Daily News Briefing</b>"
    asyncio.run(send_telegram_message(intro_message))
    
    articles = get_guardian_news()
    if not articles:
        print("No articles found, skipping briefing.")
        return

    # Loop through articles and send each one as a separate message
    for article in articles:
        summary = summarize_with_cohere(article['text'])
        
        # Build the message for a single article using HTML tags
        single_article_briefing = f"<b>{article['title']}</b>\n\n"
        single_article_briefing += f"{summary}\n\n"
        single_article_briefing += f"<a href='{article['url']}'>Read the full article</a>"
        
        # Send the message for this one article
        asyncio.run(send_telegram_message(single_article_briefing))
        
        # A small delay to avoid sending messages too fast
        time.sleep(2)

# --- The Scheduler ---
print("News briefing script started. Waiting for the scheduled time...")
# Schedule the job to run once every day at 7:30 AM
schedule.every().day.at("07:30").do(run_briefing_job)

# For testing, you can run the job immediately by uncommenting the line below
# run_briefing_job()

while True:
    schedule.run_pending()
    time.sleep(1)