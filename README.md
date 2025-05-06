# Cuban FX Market Analytics Dashboard

A Python-based web application that scrapes, processes, and analyzes foreign exchange market data from social media, performs statistical simulations, and visualizes key market metrics through an interactive dashboard.

## Features

- **Web Scraping**: Extracts currency exchange messages from social media platforms
- **Data Processing**: Cleans and structures raw market data for analysis
- **Economic Modeling**:
  - Walrasian auction simulations
  - Hidden Markov models for market state detection
  - Empirical Mode Decomposition for time series analysis
- **Interactive Dashboard**:
  - Real-time market metrics visualization
  - Time series plots of prices and volumes
  - Supply and demand curves
  - Statistical distributions (histograms)
  - Model visualizations

## Project Structure
cuban_fx_app/
├── app.py # Main application entry point
├── assets/ # Static assets (images, CSS, etc.)
├── callback/ # Dash callback functions
├── components/ # Reusable UI components
├── config/ # Configuration files
├── data/ # Data storage and processing
│ ├── raw/ # Raw scraped data
│ ├── processed/ # Cleaned and processed data
│ └── simulations/ # Simulation results
├── data_storage.py # Data persistence utilities
├── layouts/ # Dashboard page layouts
├── notebook/ # Jupyter notebooks for analysis
├── reactivity/ # Reactive components
├── routes/ # Application routing
├── services/ # Business logic services
│ ├── scraping/ # Web scraping services
│ ├── analysis/ # Statistical analysis
│ └── simulation/ # Economic simulations
├── tasks/ # Background tasks
├── tests/ # Unit and integration tests
├── docker-compose.yml # Docker compose configuration
├── dockerfile # Docker configuration
├── main.py # Alternative entry point
├── Makefile # Build automation
├── requirements.txt # Python dependencies
└── README.md # This file


## Prerequisites

- Python 3.11.11
- PostgreSQL (or your preferred database) <!-- Specify if you use a different DB -->
- Redis (for caching, if applicable) <!-- Remove if not used -->
- Chrome/Firefox for web scraping

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/cuban_fx_app.git
   cd cuban_fx_app

