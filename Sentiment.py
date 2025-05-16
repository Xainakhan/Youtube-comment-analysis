# ***************************************************************
# ---------------YOUTUBE SENTIMENT ANALYSIS----------------------
# ***************************************************************
import tkinter as tk
from tkinter import messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time
from googleapiclient.discovery import build
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
import re  # For removing emojis
from tkinter import ttk  # For creating tables
from googletrans import Translator  # For translation

# Initialize VADER sentiment analyzer
nltk.download('vader_lexicon')  # Download VADER lexicon if not already downloaded
sia = SentimentIntensityAnalyzer()

# Initialize the Google Translator
translator = Translator()

# YouTube Data API Key
youtube_api_key = 'api key'  

# Initialize YouTube API client
youtube = build('youtube', 'v3', developerKey=youtube_api_key)

# Emoji sentiment mapping
emoji_sentiment_map = {
    # Positive Emojis
    '💫': 'Positive', '⭐': 'Positive', '🌟': 'Positive', '✨': 'Positive',
    '⚡': 'Positive', '💥': 'Positive', '🔥': 'Positive', '🌈': 'Positive',
    '🖊': 'Positive', '🖋': 'Positive', '✒': 'Positive', '🖌': 'Positive',
    '🖍': 'Positive', '🩷': 'Positive', '❤': 'Positive', '🧡': 'Positive',
    '💛': 'Positive', '💚': 'Positive', '🩵': 'Positive', '💙': 'Positive',
    '💜': 'Positive', '🖤': 'Positive', '🩶': 'Positive', '🤍': 'Positive',
    '🤎': 'Positive', '❤‍🔥': 'Positive', '❤‍🩹': 'Positive', '❣': 'Positive',
    '💕': 'Positive', '💞': 'Positive', '💓': 'Positive', '💗': 'Positive',
    '💖': 'Positive', '💘': 'Positive', '💝': 'Positive', '💟': 'Positive',
    '💯': 'Positive', '❇': 'Positive', '😀': 'Positive', '😃': 'Positive',
    '😄': 'Positive', '😁': 'Positive', '😆': 'Positive', '🥹': 'Positive',
    '😅': 'Positive', '😂': 'Positive', '🤣': 'Positive', '🥲': 'Positive',
    '☺': 'Positive', '😊': 'Positive', '😇': 'Positive', '🙂': 'Positive',
    '🙃': 'Positive', '😉': 'Positive', '😌': 'Positive', '😍': 'Positive',
    '🥰': 'Positive', '😘': 'Positive', '😗': 'Positive', '😙': 'Positive',
    '😚': 'Positive', '😋': 'Positive', '😎': 'Positive', '🤓': 'Positive',
    '🤪': 'Positive', '🤑': 'Positive', '🤠': 'Positive', '😈': 'Positive',
    '😜': 'Positive', '😝': 'Positive', '😛': 'Positive', '🤩': 'Positive',
    '🥳': 'Positive', '🤭': 'Positive', '🤗': 'Positive', '🫠': 'Positive',
    '😺': 'Positive', '😸': 'Positive', '😹': 'Positive', '🫶🏻': 'Positive',
    '🤲🏻': 'Positive', '👐🏻': 'Positive', '🙌🏻': 'Positive', '👏🏻': 'Positive',
    '🤝': 'Positive', '👍🏻': 'Positive', '✊🏻': 'Positive', '🤛🏻': 'Positive',
    '🤜🏻': 'Positive', '🫷🏻': 'Positive', '🫸': 'Positive', '🤞': 'Positive',
    '✌': 'Positive', '🫰🏻': 'Positive', '🙏🏻': 'Positive', '💁🏻‍♀': 'Positive',
    '🙅🏻‍♀': 'Positive', '🌟': 'Positive', '💥': 'Positive', '☀': 'Positive',
    '✨': 'Positive', '⚡': 'Positive', '😻': 'Positive', '😽': 'Positive',
    
    # Negative Emojis
    '🤨': 'Negative', '🧐': 'Negative', '😞': 'Negative', '😒': 'Negative',
    '👿': 'Negative', '😏': 'Negative', '😼': 'Negative', '🙀': 'Negative',
    '😾': 'Negative', '👎🏻': 'Negative', '👊🏻': 'Negative', '🥸': 'Negative',
    '😫': 'Negative', '😖': 'Negative', '😣': 'Negative', '☹': 'Negative',
    '🫨': 'Negative', '😬': 'Negative', '🙄': 'Negative', '😐': 'Negative',
    '🫤': 'Negative', '😑': 'Negative', '😶': 'Negative', '🤥': 'Negative',
    '😪': 'Negative', '🤤': 'Negative', '🥱': 'Negative', '😴': 'Negative',
    '😮‍💨': 'Negative', '😵': 'Negative', '😵‍💫': 'Negative', '🤐': 'Negative',
    '😲': 'Negative', '😮': 'Negative', '🥴': 'Negative', '🤢': 'Negative',
    '🤮': 'Negative', '🤧': 'Negative', '😷': 'Negative', '🤒': 'Negative',
    '🤕': 'Negative', '🙁': 'Negative', '😕': 'Negative', '😟': 'Negative',
    '😔': 'Negative', '😩': 'Negative', '🥺': 'Negative', '😢': 'Negative',
    '😭': 'Negative', '😤': 'Negative', '😠': 'Negative', '😡': 'Negative',
    '🤬': 'Negative', '😰': 'Negative', '😨': 'Negative', '😱': 'Negative',
    '😶‍🌫': 'Negative', '🥶': 'Negative', '🥵': 'Negative', '😳': 'Negative',
    '🤯': 'Negative', '😥': 'Negative', '😓': 'Negative', '🫢': 'Negative',
}

# Function to fetch all comments
def get_all_comments(video_id):
    comments = []
    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=100,
        textFormat="plainText"
    )

    while request is not None:
        try:
            response = request.execute()
            for item in response.get('items', []):
                comment_data = item['snippet']['topLevelComment']['snippet']
                original_comment = comment_data.get('textOriginal', '')  # Fetch the original comment
                if original_comment:  # Ensure comment is not empty
                    comments.append(original_comment)

            # Check if there is a next page
            request = youtube.commentThreads().list_next(request, response)
            time.sleep(1)  # Avoid rate limiting
        except Exception as e:
            print(f"An error occurred: {e}")
            time.sleep(5)

    return comments

# Function to remove emojis from text
def remove_emojis(text):
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F700-\U0001F77F"  # alchemical symbols
        u"\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
        u"\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
        u"\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
        u"\U0001FA00-\U0001FA6F"  # Chess Symbols
        u"\U00002702-\U000027B0"  # Dingbats
        "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)  # Replace emojis with empty string

# Define a function to predict the sentiment using VADER and emojis
def predict_sentiment(comment):
    # Check for emoji sentiments
    emoji_found = [e for e in emoji_sentiment_map.keys() if e in comment]
    
    if emoji_found:
        return emoji_sentiment_map[emoji_found[0]]  # Return the sentiment of the first emoji found

    # Remove emojis for text analysis
    cleaned_comment = remove_emojis(comment)
    score = sia.polarity_scores(cleaned_comment)
    compound_score = score['compound']
    
    # Heuristic to detect if a comment is a query (question)
    is_query = "?" in comment or "how" in comment.lower() or "why" in comment.lower() or "what" in comment.lower()

    if is_query:
        return "Query"
    elif compound_score >= 0.05:
        return "Positive"
    elif compound_score <= -0.05:
        return "Negative"
    else:
        return "Neutral"

# Function to translate comments
def translate_comment(comment):
    try:
        translated = translator.translate(comment, src='ur', dest='en')
        return translated.text
    except Exception as e:
        print(f"Error during translation: {e}")
        return comment  # Return original comment if translation fails

# Function to process the video URL and display results
def analyze_video():
    video_url = entry.get()
    if "v=" not in video_url:
        messagebox.showerror("Error", "Please enter a valid YouTube URL")
        return
    
    video_id = video_url.split("v=")[1]
    video_id = video_id.split("&")[0]  # In case there are extra parameters
    
    comments = get_all_comments(video_id)
    total_comments = len(comments)
    
    if total_comments == 0:
        messagebox.showinfo("No Comments", "No comments found for the provided video.")
        return
    
    # Analyze sentiments and translate comments
    comment_sentiments = []
    translated_comments = []

    for comment in comments:
        sentiment = predict_sentiment(comment)
        translated_comment = translate_comment(comment)
        comment_sentiments.append(sentiment)
        translated_comments.append(translated_comment)

    # Count the occurrences of each sentiment
    positive_comments = sum(1 for sentiment in comment_sentiments if sentiment == 'Positive')
    negative_comments = sum(1 for sentiment in comment_sentiments if sentiment == 'Negative')
    neutral_comments = sum(1 for sentiment in comment_sentiments if sentiment == 'Neutral')
    query_comments = sum(1 for sentiment in comment_sentiments if sentiment == 'Query')

    # Print the counts of comments and sentiments
    report_text = (f"Total Comments: {total_comments}\n"
                   f"Positive Comments: {positive_comments}\n"
                   f"Negative Comments: {negative_comments}\n"
                   f"Neutral Comments: {neutral_comments}\n"
                   f"Query Comments: {query_comments}")
    
    output_label.config(text=report_text)

    # Create and display the comments table
    for widget in table_frame.winfo_children():
        widget.destroy()  # Clear the previous table contents

    columns = ('Original Comment', 'Translated Comment', 'Predicted Sentiment')
    table = ttk.Treeview(table_frame, columns=columns, show='headings')
    table.heading('Original Comment', text='Original Comment')
    table.heading('Translated Comment', text='Translated Comment')
    table.heading('Predicted Sentiment', text='Predicted Sentiment')
    
    for original_comment, translated_comment, sentiment in zip(comments, translated_comments, comment_sentiments):
        table.insert('', tk.END, values=(original_comment, translated_comment, sentiment))

    table.pack()

    # Plot a pie chart with specified colors
    labels = ['Positive', 'Negative', 'Neutral', 'Query']
    sizes = [positive_comments, negative_comments, neutral_comments, query_comments]
    colors = ['green', 'red', 'skyblue', 'yellow']

    # Create a new figure for the pie chart
    fig = Figure(figsize=(6, 4))
    ax = fig.add_subplot(111)
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
    ax.set_title("Sentiment Analysis of YouTube Comments")

    # Embed the pie chart in the tkinter window
    chart = FigureCanvasTkAgg(fig, root)
    chart.get_tk_widget().pack(pady=20)

# Create the main window with YouTube light mode theme
root = tk.Tk()
root.title("YouTube Sentiment Analysis")
root.configure(bg="#FFFFFF")  # YouTube light mode background color

# Style for the labels and buttons
label_style = {'bg': '#FFFFFF', 'fg': '#000000', 'font': ('Arial', 12)}  # Light background, dark text
button_style = {'bg': '#FF0000', 'fg': '#FFFFFF', 'font': ('Arial', 10, 'bold'), 'activebackground': '#FF4D4D'}  # Red button

# Create and place widgets
tk.Label(root, text="Enter YouTube Video URL:", **label_style).pack(pady=10)
entry = tk.Entry(root, width=50, bg='#F9F9F9', fg='#000000', insertbackground='black')
entry.pack(pady=5)

analyze_button = tk.Button(root, text="Analyze Comments", command=analyze_video, **button_style)
analyze_button.pack(pady=10)

output_label = tk.Label(root, text="", justify=tk.LEFT, **label_style)
output_label.pack(pady=10)

# Create a frame for the comments table
table_frame = tk.Frame(root)
table_frame.pack(pady=10)

# Run the application
root.mainloop()
