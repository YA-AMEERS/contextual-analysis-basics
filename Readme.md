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

Once the API is running, wether on cloud on locally, it will automatically start querying and updating the news articles in the database. You can interact with the database directly using SQLAlchemy queries or through a separate application that consumes the data stored in the database.

Here are some potential challenges, pros and cons, and possible solutions for this News Aggregation API:

### Challenges

1. **Performance Issues**:
   - Web scraping and processing large amounts of text can be computationally intensive, leading to potential performance bottlenecks.
   - Relying on third-party services like Google Search and OpenAI GPT-3.5 Turbo introduces external dependencies that may impact performance and reliability.

2. **Third-Party Service Limitations**:
   - Google Search may implement rate-limiting or anti-scraping measures, which could disrupt the API's functionality.
   - OpenAI GPT-3.5 Turbo has usage limits and costs associated with it, which could impact the API's scalability and budget constraints.

3. **Data Quality and Accuracy**:
   - The accuracy of the extracted news articles and their summaries heavily relies on the quality of the Google Search results and the performance of the OpenAI GPT-3.5 Turbo model.
   - Potential inaccuracies or biases in the data sources or the NLP model could lead to incorrect or misleading information being stored in the database.

4. **Maintenance and Updates**:
   - The API relies on several external libraries and services, which may require regular updates or maintenance to ensure compatibility and security.
   - Keeping up with changes in the data sources (e.g., news websites, Google Search algorithms) may require frequent adjustments to the scraping and processing mechanisms.

### Pros and Cons

**Pros**:
- Automated news aggregation and summarization from multiple sources.
- Leverages the power of natural language processing for text understanding and generation.
- Categorizes news articles based on state, news channel, and news section.
- Stores news articles in a structured database for easy retrieval and analysis.
- Scalable architecture with the potential to expand to more news sources and categories.

**Cons**:
- Reliance on third-party services (Google Search, OpenAI GPT-3.5 Turbo) introduces external dependencies and potential costs.
- Performance and reliability may be impacted by the limitations of web scraping and external service usage constraints.
- Accuracy and quality of the news articles and summaries depend on the data sources and the performance of the NLP model.
- Maintenance and updates may be required to address changes in data sources, external service APIs, or underlying libraries.

### Possible Solutions

1. **Caching and Performance Optimization**:
   - Implement caching mechanisms to store and reuse search results and processed text, reducing the load on external services and improving performance.
   - Explore techniques like asynchronous processing, parallel processing, or worker queues to distribute the workload and improve efficiency.

2. **Fallback Mechanisms and Redundancy**:
   - Implement fallback mechanisms to handle situations where external services are unavailable or rate-limited.
   - Explore alternative data sources or scraping techniques to reduce reliance on a single provider like Google Search.
   - Implement redundancy by utilizing multiple NLP models or services for text processing and summarization.

3. **Data Quality and Validation**:
   - Implement data validation and cleaning mechanisms to identify and handle potential inaccuracies or biases in the extracted news articles and summaries.
   - Explore techniques like human-in-the-loop review or feedback mechanisms to improve the quality of the extracted information over time.

4. **Monitoring and Alerting**:
   - Implement monitoring systems to track the performance, reliability, and accuracy of the API, external services, and data sources.
   - Set up alerts and notifications to quickly identify and address issues or outages.

5. **Scalability and Cost Management**:
   - Explore cost-effective alternatives or pricing plans for external services like OpenAI GPT-3.5 Turbo, based on your usage and budget constraints.
   - Implement scaling strategies, such as load balancing or autoscaling, to handle increasing demand and workloads efficiently.

6. **Continuous Integration and Deployment**:
   - Implement continuous integration and deployment practices to streamline the process of updating and deploying the API with new features, bug fixes, and library updates.
   - Automate testing and validation processes to ensure the API's reliability and functionality after updates.

By addressing these challenges, weighing the pros and cons, and implementing appropriate solutions, we can improve the performance, reliability, and scalability of our News Aggregation API, while maintaining data quality and mitigating the risks associated with relying on third-party services.



## Measures we took in the code

Here are some potential measures taken to address the challenges and possible improvement approaches we can consider:

1. **Performance Optimization**:
   - We are currently using the `time.sleep()` function in certain places, which could be an attempt to introduce delays and prevent overwhelming external services or mitigating rate-limiting issues.
   - Improvement: Instead of using sleep delays, consider implementing a more robust rate-limiting mechanism or a queue system to manage the requests to external services.

2. **Error Handling and Fallback Mechanisms**:
   - We includes try-except blocks in various places, such as when making Google searches or generating summaries with OpenAI GPT-3.5 Turbo. These blocks handle potential exceptions and provide fallback mechanisms to retry the operation after a certain delay.
   - Improvement: Consider implementing more sophisticated fallback mechanisms, such as retrying with an exponential backoff strategy or switching to alternative data sources or NLP models in case of persistent failures.

3. **Caching**:
   - We currently do not have any explicit caching mechanisms for search results or processed text.
   - Improvement: Implement caching strategies to store and reuse search results and processed text, reducing the load on external services and improving performance. You can use in-memory caches, distributed caches, or database caching solutions depending on your requirements.

4. **Data Validation and Cleaning**:
   - Improvement: Implement data validation and cleaning mechanisms to identify and handle potential inaccuracies or biases in the extracted news articles and summaries. This could involve techniques like regular expression filtering, sentiment analysis, or fact-checking against reputable sources.

5. **Monitoring and Alerting**:
   - Improvement: Implement monitoring systems to track the performance, reliability, and accuracy of the API, external services, and data sources. Set up alerts and notifications to quickly identify and address issues or outages. You can use logging frameworks, monitoring tools, or cloud-based monitoring services.

6. **Scalability and Cost Management**:
   - We do not currently have any explicit scalability or cost management Implementation in place.
   - Improvements: Explore cost-effective alternatives or pricing plans for external services like OpenAI GPT-3.5 Turbo, based on your usage and budget constraints. Implement scaling strategies, such as load balancing or autoscaling, to handle increasing demand and workloads efficiently.

7. **Parallel Processing**:
   - We are currently performing sequential searches and updates for each combination of state, news channel, and news section.
   - Improvements: Explore techniques like asynchronous processing or parallel processing to distribute the workload and improve efficiency, especially when performing multiple searches and updates simultaneously.

