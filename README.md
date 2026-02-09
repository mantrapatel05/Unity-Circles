# Unity Circles

A Django-based community and mentorship platform designed to connect students, foster collaboration, and facilitate meaningful mentorship relationships.

## Features

- **Communities**: Create and join communities based on interests
- **Mentorship**: Connect mentors with mentees for guidance and support
- **Direct Messaging**: Real-time messaging between users
- **Meetings**: Schedule and organize community meetings
- **Posts & Comments**: Share content and engage with the community
- **User Profiles**: Customize your profile and showcase your expertise
- **Onboarding**: Smooth onboarding experience for new users

## Tech Stack

- **Backend**: Django 5.1 + Django REST Framework
- **Database**: SQLite
- **Frontend**: HTML, CSS, JavaScript
- **Python**: 3.14+

## Quick Start

### Windows
```bash
scripts/RUN_ME.bat
```

### Mac/Linux
```bash
bash scripts/RUN_ME.sh
```

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/mantrapatel05/Unity-Circles.git
   cd Unity-Circles
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run migrations:
   ```bash
   python manage.py migrate
   ```

4. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

5. Start the development server:
   ```bash
   python manage.py runserver
   ```

Visit `http://localhost:8000` in your browser.

## Project Structure

```
Unity-Circles/
├── accounts/          # User authentication and profiles
├── chat/              # Direct messaging functionality
├── core/              # Communities, posts, meetings
├── mentorship/        # Mentorship connections
├── onboarding/        # User onboarding flow
├── static/            # CSS and JavaScript files
├── templates/         # HTML templates
├── scripts/           # Utility scripts (.bat and .sh)
└── unity_circles/     # Main Django project settings
```

## Troubleshooting

If you encounter Django errors with Python 3.14, check the `DJANGO_FIX_README.md` file for solutions.

## Contributing

Feel free to fork, create a branch, and submit a pull request with improvements.

## License

This project is open source and available under the MIT License.

## Contact

For questions or support, reach out to the maintainers on GitHub.
