# steam-wishlist-auto 🎮

This Python script automates the process of collecting and sending information about a user's Steam wishlist. It logs into the user's Steam account, retrieves data about wishlist items, and sends this data via email.

## Features

- **Automatic Steam Login**: Logs into the user's Steam account using the provided credentials.
- **Wishlist Data Collection**: Uses Selenium and BeautifulSoup to extract game data from the wishlist, including name, original price, discount price, and discount percentage.
- **Email Sending**: Formats the collected data and sends it to the user's email using `smtplib` and `email.mime`.

## Prerequisites

- Python 3.7 or higher
- `chromedriver` (place it in the `drivers` folder)
- `.env` file configured with your email details

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/steam-wishlist-auto.git
   cd steam-wishlist-auto
