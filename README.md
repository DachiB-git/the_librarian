# OpenLibrary scraper

A simple html scraper that fetches data from openlibrary main page.




## Usage
To use the scraper, first import the repo.
After successfull import, open up the terminal in the repo root directory and create a virtual environment.
python -m venv .venv
Activate the virtual environment.
./.venv/Scripts/activate
Download all required dependencies listed in the requirements.txt
pip install beautifulsoup4
pip install requests
Activate the main script
python ./main.py
After the script has finished running, you will be presented with the scraped data in the terminal, and also two accompanying data files in csv and json format,
located in ./data/*.
