import os
import random
from datetime import datetime

from telegram import Bot
from apscheduler.schedulers.blocking import BlockingScheduler
import pytz
import requests  # for making API calls if needed (not used in this sample)

# Load environment variables (Telegram bot token and target chat ID)
BOT_TOKEN = os.getenv("8028954287:AAHzmvwla65L8oY0LDpqXT-TDzOrDzRUwt4")
USER_CHAT_ID = os.getenv("931449387")

if not BOT_TOKEN or not USER_CHAT_ID:
    print("Missing 8028954287:AAHzmvwla65L8oY0LDpqXT-TDzOrDzRUwt4 or 931449387 environment variable.")
    exit(1)

# Initialize the Telegram Bot
bot = Bot(token=8028954287:AAHzmvwla65L8oY0LDpqXT-TDzOrDzRUwt4)

def compose_message():
    """Compose the content of the scheduled message (simulate data)."""
    # Simulate data for gold price (triệu VNĐ per lượng), BTC price (USD), and USD/VNĐ exchange rate
    gold_price = round(random.uniform(55, 60), 2)     # e.g., 56.78 triệu VNĐ/lượng
    btc_price = round(random.uniform(30000, 35000), 2)  # e.g., 32000.45 USD
    usd_rate = round(random.uniform(23000, 24000), 2)   # e.g., 23500.00 VNĐ per USD

    # Placeholder texts for other information
    macro_news = "Đang cập nhật tin tức."  # Macro news placeholder
    trend_info = "Thị trường đang trong xu hướng tăng."  # Trend information
    reversal_warning = "Chưa có cảnh báo đảo chiều."     # Reversal warning
    short_term_strategy = "Tiếp tục quan sát và giữ vị thế hiện tại."  # Short-term strategy

    # Construct the message string with multiple lines
    message = (
        f"Giá vàng: {gold_price} triệu VNĐ/lượng\n"
        f"Giá BTC: {btc_price} USD\n"
        f"Tỷ giá USD/VNĐ: {usd_rate}\n"
        f"Tin tức vĩ mô: {macro_news}\n"
        f"Xu hướng: {trend_info}\n"
        f"Cảnh báo đảo chiều: {reversal_warning}\n"
        f"Chiến lược ngắn hạn: {short_term_strategy}"
    )
    return message

def send_message():
    """Send the composed message to the user via Telegram."""
    text = compose_message()
    try:
        bot.send_message(chat_id=USER_CHAT_ID, text=text)
        # Log the sending time
        print(f"Sent message at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    except Exception as e:
        # Log any error if sending fails
        print(f"Failed to send message: {e}")

# Set up the scheduler with Vietnam timezone
tz = pytz.timezone("Asia/Ho_Chi_Minh")
scheduler = BlockingScheduler(timezone=tz)

# Schedule jobs:
# 1. Send message every 2 hours
scheduler.add_job(send_message, "interval", hours=2)
# 2. Send message at 7:30, 13:30, and 19:30 every day
scheduler.add_job(send_message, "cron", hour=7, minute=30)
scheduler.add_job(send_message, "cron", hour=13, minute=30)
scheduler.add_job(send_message, "cron", hour=19, minute=30)

if __name__ == "__main__":
    try:
        print("Scheduler started...")
        scheduler.start()  # Start the scheduler (blocking current thread)
    except (KeyboardInterrupt, SystemExit):
        # Graceful shutdown on exit
        scheduler.shutdown()
        print("Scheduler stopped.")
