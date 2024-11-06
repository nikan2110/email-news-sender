# Email Newsletter Application

This Python-based web application, built with Streamlit, enables users to create, manage, and send email newsletters. The application supports creating news blocks, reviewing the main page, and sending newsletters to recipients. News blocks that have been sent are marked as such and will not reappear in the list.

## Features

- **Create and manage news blocks**: Easily add, edit, and organize news content.
- **Preview the main page**: Review the full newsletter layout before sending.
- **Send newsletters**: Email newsletters to a predefined list of recipients.
- **Prevent duplicate sends**: Sent news blocks are automatically marked as sent.
- **Manage images**: Delete news images automatically as needed.

## Prerequisites

Ensure you have the following set up before starting:

- **Python 3.x** installed.
- Install dependencies from `requirements.txt` with:

    ```bash
    pip install -r requirements.txt
    ```

## Setup

1. **Clone the repository**:

    ```bash
    git clone https://github.com/nikan2110/email-news-sender.git
    ```

2. **Navigate to the project directory**:

    ```bash
    cd email-news-sender
    ```

3. **Configure the application**:
   - In `config.py`, set up:
     - **Database connection**: Define your database connection string.
     - **Email settings**: Configure SMTP settings to enable email sending.

4. **Run the application**:

    ```bash
    streamlit run main.py
    ```

5. **Access the app**: Visit `http://localhost:8501` to use the application.

## Project Structure

- **main.py**: Entry point for launching the Streamlit application.
- **email_sender.py**: Contains the email sending logic.
- **html_builder_email_main.py**: Generates HTML for the main newsletter page.
- **html_builder_email_preview.py**: Generates HTML previews for individual news blocks.
- **db.py**: Manages database connections and queries.
- **model.py**: Defines SQLAlchemy models for news blocks, main page, and recipients.
- **tools.py**: Utility functions for image handling and other common tasks.
- **config.py**: Stores database and email configuration settings.
- **constant.py**: Holds constants used across the application.

## Usage

1. **Create News Blocks**: Use the "News Block" tab to add and manage news entries.
2. **Preview Newsletter**: In the "Preview" tab, review the newsletter before sending.
3. **Send Newsletter**: Once ready, the director can send the newsletter from the "Send Email" tab. Sent news blocks will be marked and removed from the list for future sends.
4. **Manage Images**: The application automates image uploads and deletion for associated news blocks.

## Database Models

- **NewsBlock**: Represents each news item, including fields like title, description, and `is_send` status.
- **NewsMainPage**: Stores information about the main page of the newsletter.
- **Recipients**: Manages the list of recipients for the newsletter.

## Error Handling

- **Email Sending**: Logs any issues during email dispatch and provides user notifications for errors.
- **Database Queries**: Logs errors encountered during database interactions and safely closes sessions.

## Future Enhancements

- Add retry functionality for email dispatch failures.
- Strengthen input validation (e.g., URL and email address validation).
- Optimize image handling for larger datasets.

## Contributing

1. **Fork the repository**.
2. **Create your feature branch**: (`git checkout -b feature/your-feature`).
3. **Commit your changes**: (`git commit -m 'Add some feature'`).
4. **Push to the branch**: (`git push origin feature/your-feature`).
5. **Open a Pull Request**.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
