YouTube Sentiment Analysis

This project is a **desktop application** built using **Python** and **Tkinter** that analyzes the sentiment of YouTube video comments using the **VADER Sentiment Analyzer**, **Google Translate**, and the **YouTube Data API**. It also supports **emoji-based sentiment detection** and visualizes results in a pie chart.

Features

- Fetches top-level comments from a YouTube video
- Translates comments (from Urdu to English by default)
- Detects sentiment using:
- VADER sentiment analysis for text
- Custom emoji sentiment mapping
- Displays sentiment distribution in a pie chart
- Shows original and translated comments with predicted sentiment in a table
- GUI made with Tkinter styled to resemble YouTube's light mode

---

## How to Run

### Prerequisites

Make sure you have the following installed:

- Python 3.7 or above
- pip (Python package installer)

### Installation

1. Clone the repository or download the code.

2. Install required libraries:

```bash
pip install google-api-python-client nltk googletrans==4.0.0-rc1 matplotlib
```
