# run.py
# changing for the update

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)