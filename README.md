# Email Newsletter Application

This is a Python-based web application built with Streamlit to create and manage email newsletters. Users can create news blocks, review the main page, and send newsletters to recipients. Sent news blocks are marked as sent and no longer appear in the list.

## Features
- Create and manage news blocks.
- Review and preview the main page of the newsletter before sending.
- Send email newsletters to a list of recipients.
- Prevents resending of already sent news blocks.
- Automatically deletes news images upon request.

## Prerequisites
Before you begin, ensure you have met the following requirements:
- Python 3.x installed.
- Dependencies listed in the `requirements.txt` file installed. You can install them using the following command:

    ```bash
    pip install -r requirements.txt
    ```

## Setup

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/email-newsletter-app.git
    ```

2. Navigate to the project directory:
    ```bash
    cd email-newsletter-app
    ```

3. Configure the database and email settings in the `config.py` file:
    - Set up your database connection string.
    - Configure SMTP settings for sending emails.

4. Run the application:
    ```bash
    streamlit run main.py
    ```

5. Access the application at `http://localhost:8501`.

## Project Structure

- **main.py**: Main entry point for the Streamlit application.
- **email_sender.py**: Contains logic for sending emails to recipients.
- **html_builder_email_main.py**: Handles HTML generation for the main page of the newsletter.
- **html_builder_email_preview.py**: Handles the preview HTML generation for news blocks.
- **db.py**: Database connection and query logic.
- **model.py**: SQLAlchemy models for news blocks, main page, and recipients.
- **tools.py**: Utility functions for handling images and other common tasks.
- **config.py**: Configuration file for database and email settings.
- **constant.py**: Stores constants used throughout the application.

## Usage

1. **Creating News Blocks**: Users can add new news blocks through the "News Block" tab.
2. **Previewing the Newsletter**: The "Preview" tab allows users to review the newsletter before sending.
3. **Sending the Newsletter**: Once reviewed, the director can send the email using the "Send Email" tab. After sending, the news blocks are marked as sent and won't appear in future lists.
4. **Managing Images**: The application automatically handles the uploading and deletion of images related to news blocks.

## Database Models

- **NewsBlock**: Represents each news block with fields like title, description, and status (`is_send`).
- **NewsMainPage**: Represents the main page of the newsletter.
- **Recipients**: Contains the list of email recipients.

## Error Handling

- **Email Sending**: The application logs any errors during the email sending process and notifies the user.
- **Database Errors**: Errors during database queries are logged, and the session is safely closed.

## Future Improvements

- Add retry logic for failed email sending attempts.
- Enhance validation for input fields (e.g., valid URLs, email addresses).
- Improve image handling for larger datasets.

## Contributing

1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.