# OpenLibrary scraper

A simple html scraper that fetches data from openlibrary main page.




## Usage
To use the scraper, first import the repo.
<br>
After successfull import, open up the terminal in the repo root directory and create a virtual environment.
<br>
python -m venv .venv
<br>
Activate the virtual environment.
<br>
./.venv/Scripts/activate
<br>
Download all required dependencies listed in the requirements.txt
<br>
pip install beautifulsoup4
<br>
pip install requests
<br>
Activate the main script
<br>
python ./main.py
<br>
After the script has finished running, you will be presented with the scraped data in the terminal, and also two accompanying data files in csv and json format,
located in ./data/*.
