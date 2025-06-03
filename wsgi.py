from src.app import app

# This is for Vercel
app = app

if __name__ == "__main__":
    app.run(debug=True) 