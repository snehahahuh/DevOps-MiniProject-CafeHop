# ☕ CafeHop

CafeHop is a Flask-based cafe discovery web application.

## Features

- Cafe discovery homepage
- Search cafes by name, location, or category
- Category filtering
- Minimum rating filtering
- Highest and lowest rating sorting
- Favorite cafes
- Dedicated favorites page
- Cafe details page
- Google Maps directions
- No-results handling
- Automated testing with pytest
- GitHub Actions CI

## Technologies Used

- Python
- Flask
- HTML
- CSS
- Jinja2
- JSON
- Pytest
- Git
- GitHub
- GitHub Actions

## Project Structure

```text
CafeHop/
├── .github/
│   └── workflows/
│       └── ci.yml
├── data/
│   └── cafes.json
├── static/
│   └── style.css
├── templates/
│   ├── cafe.html
│   ├── favorites.html
│   └── index.html
├── tests/
│   └── test_app.py
├── .gitignore
├── app.py
├── README.md
└── requirements.txt
