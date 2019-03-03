from slack_post_json.core import SlackPosts2JSON
from config.setup import SLACK_CHANNEL_ID,TOKEN

def main():
    SlackPosts2JSON(channel_id=SLACK_CHANNEL_ID, token=TOKEN).json_dump()

if __name__ == "__main__":
    main()
