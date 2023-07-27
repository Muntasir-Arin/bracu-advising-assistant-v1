# Course Scheduling Tool for BRACU
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)
## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact) 
## Introduction
Bracu-advising-assistant-v1 is a Python-based web scraping application designed to collect advising-related information from the university website and create efficient course schedules for students. This tool utilizes Selenium to navigate through the university website, extract course data, and then find the best combination of courses that minimizes waiting time and the number of class days. The resulting schedules are then stored in the output folders for easy access.

With this tool, students can optimize their course schedules, avoid unnecessary waiting periods between classes, and ensure a balanced and efficient routine for their academic semester.

## Features

- Web scraping of university website (USIS) for course information
- Finding best possible combination from available courses.
- Efficient course scheduling based on preferences
- Elimination of excessive waiting time between classes
- Reduction of the number of class days
- Minimum numbers of lab

## Requirements

- Python 3.x
- Selenium
- ChromeDriver (for running the Selenium WebDriver with Chrome)
- bs4 (BeautifulSoup)
- Pillow

## Installation

1. Make sure you have Python 3.x installed on your system.
2. Clone this repository to your local machine or download the ZIP file and extract it.
3. Navigate to the project directory:

```bash
cd university-web-scraping-tool
```

4. Install the required dependencies:

```bash
pip install -r requirements.txt
```

5. Download the appropriate version of ChromeDriver from the official website and place it in the project directory.

## Contributing

Contributions are welcome! If you find any bugs or have suggestions for improvement, please open an issue or a pull request on the GitHub repository.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For any inquiries or questions, please contact us at [muntasirarin@gmail.com](mailto:muntasirarin@gmail.com).
