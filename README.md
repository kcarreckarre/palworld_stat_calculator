
# Project Documentation

## Overview

This project includes several scripts for various purposes such as data scraping, statistical calculations, and application output processing.

### Scripts

1. **scrape_pals.js**: This script uses Puppeteer to scrape data from the PalWorld website for a list of pals and save the data into a JSON file.
2. **store_pal_database.py**: This script handles the storage of pal data into a database using SQLite and downloads images using `requests`.
3. **stat_calcul.py**: This script performs various statistical calculations using `numpy` and SQLite.
4. **appli_output.py**: This script processes the output of the application using `tkinter`, `ttkbootstrap`, and SQLite.

## Requirements

The project requires the following packages:
- puppeteer==13.0.0
- fs==0.0.1-security
- requests
- numpy
- ttkbootstrap

## Usage

### scrape_pals.js
To run the scraper script:
```bash
node scrape_pals.js
```

### store_pal_database.py
To store the pal data into a database:
```bash
python store_pal_database.py
```

### stat_calcul.py
To perform statistical calculations:
```bash
python stat_calcul.py
```

### appli_output.py
To process application output:
```bash
python appli_output.py
```
