import streamlit as st
import pandas as pd
from textblob import TextBlob
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt

st.set_page_config(page_title="Market Pulse", page_icon="🛍️", layout="wide")
st.title("🛍️ Market Pulse — E-Commerce Sentiment Analyzer")

uploaded_file = st.file_uploader("📂 Upload your CSV file (must contain a 'review' column)", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file, encoding='latin-1', on_bad_lines='skip')
    st.success("✅ File uploaded successfully! Here's a quick preview:")
    st.dataframe(df.head())

    def get_sentiment(text):
        blob = TextBlob(str(text))
        polarity = blob.sentiment.polarity
        if polarity > 0.1:
            return "Positive"
        elif polarity < -0.1:
            return "Negative"
        else:
            return "Neutral"

    df["Sentiment"] = df["review"].apply(get_sentiment)

    st.subheader("📊 Sentiment Distribution")
    fig = px.pie(df, names="Sentiment", title="Customer Sentiment Breakdown", color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("🌈 Word Cloud of Reviews")
    text = " ".join(df["review"].astype(str))
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text)
    fig_wc, ax = plt.subplots()
    ax.imshow(wordcloud, interpolation="bilinear")
    ax.axis("off")
    st.pyplot(fig_wc)

    st.subheader("💡 Quick Insights")
    total = len(df)
    pos = (df["Sentiment"] == "Positive").sum()
    neg = (df["Sentiment"] == "Negative").sum()
    neu = (df["Sentiment"] == "Neutral").sum()
    st.write(f"😊 Positive: {pos/total*100:.1f}% | 😐 Neutral: {neu/total*100:.1f}% | 😡 Negative: {neg/total*100:.1f}%")

    if pos > neg:
        st.success("✅ Overall customer sentiment is positive!")
    else:
        st.warning("⚠️ Negative feedback is higher — potential improvement needed.")
else:
    st.info("👆 Upload your CSV file to start the sentiment analysis.")