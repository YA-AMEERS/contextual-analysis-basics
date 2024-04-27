Sure, I can provide a comprehensive and professional README for your API documentation. Here's a detailed breakdown:

# News Aggregation API

This API is designed to query breaking news from various news outlets through Google, process the news articles, structure them, and store them in a database. The API uses natural language processing (NLP) techniques to extract relevant information from the news articles and categorize them based on their content.

## Architecture

The API is built using the following components:

- **Flask**: A lightweight Python web framework used for building the API.
- **SQLAlchemy**: A Python SQL toolkit and Object-Relational Mapper (ORM) used for interacting with the database.
- **Flask-Migrate**: A Flask extension that handles SQLAlchemy database migrations.
- **BeautifulSoup**: A Python library for web scraping, used to extract data from HTML and XML documents.
- **OpenAI GPT-3.5 Turbo**: A natural language processing model used for text generation and summarization tasks.

## Tools and Libraries Used

- **Flask**: The primary web framework used for building the API.
- **SQLAlchemy**: An ORM used for database operations.
- **Flask-Migrate**: A Flask extension used for handling database migrations.
- **requests**: A Python library used for sending HTTP requests.
- **BeautifulSoup**: A Python library used for web scraping and data extraction from HTML and XML documents.
- **dateutil**: A Python library used for parsing and manipulating dates.
- **OpenAI GPT-3.5 Turbo**: A natural language processing model used for text generation and summarization tasks.
- **hashlib**: A Python library used for secure hashing and message digests.
- **random**: A Python library used for generating random numbers.
- **dotenv**: A Python library used for loading environment variables from a `.env` file.

## Processes

1. **Google Search**: The API performs a Google search for breaking news based on the specified search query, which includes the state, news channel, and news section (e.g., Business, Security, Health care). The search results are then scraped using BeautifulSoup to extract the relevant text.

2. **Text Processing**: The extracted text from the search results is passed to the OpenAI GPT-3.5 Turbo model, which processes the text and generates a JSON response containing the headlines, stories, and sources of the news articles.

3. **Database Storage**: The processed news articles are stored in two SQLAlchemy models: `UptodateNews` and `AllNews`. The `UptodateNews` model stores the most recent news articles, with a limit of 50 rows. When the row count exceeds 50, the table is cleared, and new news articles are added. The `AllNews` model stores all news articles without any row limit.

4. **Scheduled Updates**: The API includes a function called `updateNews()` that periodically updates the news articles in the database. This function is responsible for calling the `searchSequentially()` function, which performs the Google search, text processing, and database storage for each combination of state, news channel, and news section.

## API Endpoints

The API does not expose any specific endpoints. Instead, it runs the `updateNews()` function on startup, which continuously updates the news articles in the database.

## Setup and Installation

1. Clone the repository to your local machine.
2. Create a virtual environment and activate it.
3. Install the required dependencies by running `pip install -r requirements.txt`.
4. Set up the database by running the necessary SQLAlchemy migrations.
5. Create a `.env` file in the project root directory and add your OpenAI API key with the variable name `OPENAI-API-KEY`.
6. Run the Flask application using `python app.py`.

## Usage

Once the API is running, it will automatically start querying and updating the news articles in the database. You can interact with the database directly using SQLAlchemy queries or through a separate application that consumes the data stored in the database.

## Contributing

Contributions are welcome! If you find any issues or want to add new features, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).
