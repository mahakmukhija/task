import streamlit as st
import tweepy
import requests
import json

st.set_page_config(page_title="Social Media Poster", layout="centered")
st.title("📲 Post on Instagram, X (Twitter), Facebook")

platform = st.selectbox("Select Platform", ["X (Twitter)", "Facebook", "Instagram"])

if platform == "X (Twitter)":
    st.header("Post a Tweet")
    bearer_token = st.text_input("Twitter Bearer Token", type="password")
    tweet_text = st.text_area("Tweet Text")

    if st.button("Post Tweet"):
        if not bearer_token or not tweet_text:
            st.error("Please provide all details!")
        else:
            client = tweepy.Client(bearer_token)
            try:
                client.create_tweet(text=tweet_text)
                st.success("Tweet posted successfully!")
            except Exception as e:
                st.error(f"Failed to post tweet: {e}")

elif platform == "Facebook":
    st.header("Post on Facebook Page")
    page_access_token = st.text_input("Facebook Page Access Token", type="password")
    page_id = st.text_input("Facebook Page ID")
    post_message = st.text_area("Post Message")

    if st.button("Post to Facebook"):
        if not (page_access_token and page_id and post_message):
            st.error("Please fill all fields!")
        else:
            url = f"https://graph.facebook.com/{page_id}/feed"
            payload = {
                "message": post_message,
                "access_token": page_access_token
            }
            response = requests.post(url, data=payload)
            if response.status_code == 200:
                st.success("Post published on Facebook!")
            else:
                st.error(f"Failed to post: {response.text}")

elif platform == "Instagram":
    st.header("Post Image to Instagram Business Account")
    instagram_account_id = st.text_input("Instagram Account ID")
    page_access_token = st.text_input("Facebook Page Access Token", type="password")
    image_url = st.text_input("Image URL to Post (publicly accessible)")
    caption = st.text_area("Caption")

    if st.button("Post to Instagram"):
        if not (instagram_account_id and page_access_token and image_url):
            st.error("Please fill all fields!")
        else:
            try:
                # Step 1: Create media object container
                media_url = f"https://graph.facebook.com/v16.0/{instagram_account_id}/media"
                media_payload = {
                    "image_url": image_url,
                    "caption": caption,
                    "access_token": page_access_token
                }
                media_res = requests.post(media_url, data=media_payload)
                media_json = media_res.json()
                if "id" not in media_json:
                    st.error(f"Failed to create media object: {media_json}")
                    st.stop()

                creation_id = media_json["id"]

                # Step 2: Publish media object
                publish_url = f"https://graph.facebook.com/v16.0/{instagram_account_id}/media_publish"
                publish_payload = {
                    "creation_id": creation_id,
                    "access_token": page_access_token
                }
                publish_res = requests.post(publish_url, data=publish_payload)
                publish_json = publish_res.json()
                if "id" in publish_json:
                    st.success("Instagram post published successfully!")
                else:
                    st.error(f"Failed to publish post: {publish_json}")
            except Exception as e:
                st.error(f"Error: {e}")
