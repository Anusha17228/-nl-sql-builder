# NL → SQL Query Builder

Convert natural language questions into SQL queries using AI! Built with Streamlit and Groq API.

## 🚀 Live Demo

**[Try the app on Streamlit Cloud](https://share.streamlit.io/anusha17228/-nl-sql-builder)**

## ✨ Features

- 📝 **Natural Language to SQL** - Ask questions in plain English, get SQL queries
- 🔒 **SQL Safety Validation** - Only SELECT queries allowed, prevents malicious code
- 📊 **Automatic Visualizations** - Charts generated from query results
- 📥 **Database Upload** - Upload SQLite databases to query
- 💾 **CSV Export** - Download results as CSV
- 📜 **Query History** - Keep track of your queries
- ✅ **Query Explanation** - AI explains generated SQL in simple terms

## 🛠️ Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io/) - Python web framework
- **LLM**: [Groq API](https://console.groq.com/) - Fast AI model (Llama 3.3 70B)
- **Database**: SQLite
- **Visualization**: Plotly
- **Data Processing**: Pandas

## 📋 Prerequisites

- Python 3.8+
- Groq API Key (get one free at [console.groq.com](https://console.groq.com/keys))

## ⚙️ Installation & Setup (Local)

1. **Clone the repository**
   ```bash
   git clone https://github.com/Anusha17228/-nl-sql-builder.git
   cd -nl-sql-builder
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up Groq API key**
   ```bash
   mkdir -p .streamlit
   echo 'GROQ_API_KEY = "your_groq_api_key_here"' > .streamlit/secrets.toml
   ```

5. **Run the app**
   ```bash
   streamlit run app.py
   ```

## 🌐 Deployment to Streamlit Cloud

1. **Push to GitHub** (already done ✅)
   ```bash
   git add .
   git commit -m "Deploy to Streamlit Cloud"
   git push origin main
   ```

2. **Go to [Streamlit Cloud](https://share.streamlit.io/)**
   - Click "New app"
   - Connect your GitHub account
   - Select repository: `-nl-sql-builder`
   - Select branch: `main`
   - Set main file: `app.py`
   - Click "Deploy"

3. **Add Secrets**
   - Once deployed, click ⚙️ Settings → Secrets
   - Add your Groq API key:
     ```
     GROQ_API_KEY = "your_groq_api_key_here"
     ```

## 📁 Project Structure

```
.
├── app.py              # Main Streamlit application
├── sql_agent.py        # Groq API integration for SQL generation
├── safety.py           # SQL validation & safety checks
├── charts.py           # Visualization generation
├── utils.py            # Database utilities
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## 🔑 Environment Variables

- `GROQ_API_KEY` - Your Groq API key (required)

## 📝 How to Use

1. **Upload a Database**: Click the file uploader to select your SQLite database file
2. **View Schema**: The app displays the database schema automatically
3. **Ask a Question**: Type your question in plain English (e.g., "Show all students with GPA > 3.5")
4. **View Results**: See the generated SQL query and results
5. **Export**: Download results as CSV or view charts

## 🛡️ Safety Features

- Only **SELECT** queries are allowed
- Blocked dangerous keywords: DROP, DELETE, UPDATE, INSERT, ALTER, etc.
- Multiple statement protection
- SQL validation before execution

## 🐛 Troubleshooting

**AuthenticationError with Groq?**
- Make sure `GROQ_API_KEY` is added to Streamlit Cloud secrets
- Check that your API key is valid at [console.groq.com](https://console.groq.com/)

**SQL Query not executing?**
- Check the schema matches your database
- Ensure you're asking valid SQL questions
- View error messages for more details

## 📄 License

MIT License - feel free to use this project!

## 🤝 Contributing

Found a bug or have a feature request? Feel free to open an issue or submit a PR!

---

**Made with ❤️ using Streamlit & Groq API**