# Flask Mobile Application

This project is a mobile application built using Flask, designed to operate separately from an existing web application on the same router network.

## Project Structure

```
flask-mobile-app
├── app
│   ├── __init__.py
│   ├── routes.py
│   ├── models.py
│   └── static
│       └── (empty)
│   └── templates
│       └── (empty)
├── requirements.txt
├── config.py
└── README.md
```

## Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd flask-mobile-app
   ```

2. **Create a Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the Application**
   Update the `config.py` file with your specific settings, such as database connection details.

5. **Run the Application**
   ```bash
   flask run
   ```

## Usage Guidelines

- Access the mobile application through the designated endpoint on your local network.
- Refer to the `app/routes.py` file for available routes and their functionalities.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.