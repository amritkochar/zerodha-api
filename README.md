# Zerodha API Client

This repository contains a Python-based client for interacting with the Zerodha Kite API. It provides functionality to fetch and display user profile details, holdings, positions, and mutual fund holdings. The client also includes caching mechanisms to reduce API calls and improve performance.

## Features

- **User Profile**: Fetch and display the user's profile information.
- **Holdings**: Retrieve and display equity holdings.
- **Positions**: Fetch current day's positions.
- **Mutual Fund Holdings**: Retrieve and display mutual fund holdings in a tabular format.
- **Caching**: Cache API responses (e.g., holdings, mutual fund holdings) to reduce redundant API calls.
- **Authentication**: Securely handle API authentication using encrypted tokens.


## Explanation of Key Files and Directories

- **`kite_client/`**: Contains the core logic for interacting with the Zerodha Kite API.
  - `__init__.py`: Marks the directory as a Python package.
  - `auth.py`: Handles user authentication and encryption of sensitive data like tokens.
  - `cache.py`: Implements caching to reduce redundant API calls and improve performance.
  - `client.py`: Contains the main logic for making API requests and processing responses.
  - `config.py`: Stores configuration details such as API keys and redirect URIs.
  - `__pycache__/`: Contains compiled Python files for faster execution (ignored by Git).

- **`.kite_cache/`**: Stores cached API responses to minimize API calls.
  - `holdings.json`: Cached data for equity holdings.
  - `mf_holdings.json`: Cached data for mutual fund holdings.

- **`runner.py`**: A command-line interface (CLI) script to interact with the Zerodha Kite API. Provides options to fetch user profile, holdings, positions, and mutual fund holdings.

- **`kite_access_token.json`**: Stores the encrypted access token required for API authentication (ignored by Git for security).

- **`kite_secret.key`**: Stores the encryption key used to secure the access token (ignored by Git for security).

- **`.gitignore`**: Specifies files and directories to be excluded from version control, such as sensitive credentials and cache files.

- **`LICENSE`**: Contains the license information for the repository (MIT License).

- **`README.md`**: Provides documentation for the repository, including setup instructions, usage, and features.

## Prerequisites

1. **Python 3.10+**: Ensure you have Python installed on your system.
2. **Dependencies**: Install the required Python packages using `pip`.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/zerodha-api.git
   cd zerodha-api
2. Set up your API credentials:
    ```
    API_KEY = "your_api_key"
    API_SECRET = "your_api_secret"
    REDIRECT_URI = "http://localhost:8000/"
    ```
3. Generate the encryption key:
    ```
    python -c "from kite_client.auth import generate_key; generate_key()"
    ```
4. Auth with Zerodha
    ```
    python3 runner.py
    ```
5. Run:
    ```
    python3 runner.py
    ```

## CLI Options

1. **Show Profile**: Displays the user's profile information.
2. **Show Holdings**: Fetches and displays equity holdings.
3. **Show Positions**: Fetches and displays current day's positions.
4. **Show MF Holdings**: Fetches and displays mutual fund holdings in a tabular format.
5. **Exit**: Exits the CLI.

## Caching

- API responses for holdings and mutual fund holdings are cached in the `.kite_cache/` directory.
- Cache expiration is set to **1 hour** (3600 seconds).

## Security

- The `kite_access_token.json` and `kite_secret.key` files are ignored by Git to prevent accidental exposure of sensitive credentials.
- Tokens are encrypted using the `Fernet` encryption scheme.

## License

This project is licensed under the [MIT License](LICENSE).

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

## Disclaimer

This project is not affiliated with Zerodha. Use it at your own risk.