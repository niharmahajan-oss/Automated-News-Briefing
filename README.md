Automated News Briefing 📰🤖
An automated Python script that creates a personalized daily news briefing. It fetches the latest world news, uses AI to summarize the top articles, and delivers the briefing directly to your Telegram account every morning.

This project is an example of a complete, automated data pipeline, moving from data collection to AI processing to final delivery without any manual intervention.

Features
Automated Data Collection: Fetches the latest articles from The Guardian's official news API.

AI-Powered Summarization: Uses the Cohere AI API to generate concise, multi-point summaries of long articles.

Push Notifications: Delivers the final, formatted briefing as a series of messages to a Telegram chat using a custom bot.

Daily Scheduling: Runs automatically once every day at a scheduled time, thanks to the schedule library.

Cloud-Ready: Designed to be deployed on a cloud service like PythonAnywhere for 24/7, hands-off operation.

How It Works (The Data Pipeline)
The script executes a simple, three-step pipeline every day:

Fetch: It makes an API call to The Guardian to get the top 5 latest world news articles, including their titles, links, and full body text.

Summarize: It loops through each article, sending the full text to the Cohere AI API with a prompt asking for a short, bulleted summary.

Deliver: It formats the title, summary, and link for each article into a clean message and sends them one by one to a specified Telegram chat via a bot.

Tech Stack
Primary Language: Python

Key Libraries:

requests: For making HTTP requests to The Guardian API.

cohere: The official Python client for the Cohere AI API.

python-telegram-bot: To interact with the Telegram Bot API.

schedule: For scheduling the script to run at a specific time every day.

python-dotenv: For managing secret API keys.

Setup and Installation
To run this project locally, follow these steps:

1. Prerequisites
Python 3.8+

Git

2. Clone the Repository
git clone [https://github.com/your-username/Automated-News-Briefing.git](https://github.com/your-username/Automated-News-Briefing.git)
cd Automated-News-Briefing

(Replace your-username with your GitHub username.)

3. Create and Activate a Virtual Environment
# Create the environment
python -m venv venv

# Activate on macOS/Linux
source venv/bin/activate

# Activate on Windows
# venv\Scripts\activate

4. Install Dependencies
pip install -r requirements.txt

(You can generate the requirements.txt file by running pip freeze > requirements.txt in your active virtual environment.)

5. Set Up Environment Variables
Create a file named .env in the root of the project folder. This file is for your secret API keys and is not tracked by Git.

Populate it with your credentials:

# From [https://open-platform.theguardian.com/access/](https://open-platform.theguardian.com/access/)
GUARDIAN_API_KEY=YOUR_GUARDIAN_KEY_HERE

# From [https://dashboard.cohere.com/](https://dashboard.cohere.com/)
COHERE_API_KEY=YOUR_COHERE_KEY_HERE

# From Telegram's @BotFather
TELEGRAM_TOKEN=YOUR_TELEGRAM_BOT_TOKEN_HERE

# From Telegram's @userinfobot
TELEGRAM_CHAT_ID=YOUR_PERSONAL_CHAT_ID_HERE

Usage
To run the script, simply execute the main.py file from your terminal:

python main.py

By default, the script is scheduled to run daily at 7:30 AM.

To Test Immediately:
To run the job right away for testing purposes, uncomment the line # run_briefing_job() near the bottom of the main.py script and run it again.

Deployment
This script is designed to be deployed on a cloud service for continuous operation. It can be run as a Scheduled Task on a platform like PythonAnywhere, allowing it to execute every day even when your local computer is off.
