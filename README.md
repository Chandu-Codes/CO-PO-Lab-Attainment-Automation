# CO-PO Lab Attainment Automation

## Overview

**CO-PO Lab Attainment Automation** is a comprehensive Django-based web application designed to streamline and automate the assessment and tracking of Course Outcomes (CO) and Program Outcomes (PO) attainment in educational laboratory environments.

This system enables educational institutions to:
- Upload and process lab assessment data via Excel
- Automatically calculate CO and PO attainment metrics
- Generate comprehensive reports and analytics
- Track student performance across multiple courses and outcomes
- Facilitate data-driven curriculum improvement

## Features

### 📊 Core Functionality
- **Excel Data Processing**: Upload and parse lab assessment data from Excel files
- **Automated Calculations**: Calculate attainment percentages and statistical metrics
- **Report Generation**: Create detailed reports with visualizations
- **User Dashboard**: Intuitive interface for monitoring attainment data
- **Data Management**: CRUD operations for configurations and assessments

### 🔐 Security & Access Control
- User authentication and authorization
- Role-based access control
- Secure file upload and processing
- Django admin panel for management

### 📈 Reporting & Analytics
- Real-time attainment visualization
- PDF and Excel report generation
- Comparative analysis across courses
- Performance metrics and trends

## Tech Stack

- **Backend**: Django 5.2.12
- **Database**: PostgreSQL (production) / SQLite (development)
- **Frontend**: HTML5, CSS3, JavaScript
- **File Processing**: openpyxl
- **Server**: Gunicorn
- **Deployment**: Render.com

## Installation

### Prerequisites
- Python 3.9+
- pip (Python package manager)
- Virtual environment (recommended)

### Local Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/Chandu-Codes/CO-PO-Lab-Attainment-Automation.git
   cd CO-PO-Lab-Attainment-Automation
   ```

2. **Create and activate virtual environment**
   ```bash
   # Windows
   python -m venv .venv
   .venv\Scripts\activate
   
   # macOS/Linux
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Start development server**
   ```bash
   python manage.py runserver
   ```

   Access the application at `http://localhost:8000`

## Project Structure

```
CO-PO-Lab-Attainment-Automation/
├── apps/
│   └── processing/
│       ├── models.py          # Database models
│       ├── views.py           # View logic
│       ├── urls.py            # URL routing
│       ├── forms.py           # Form definitions
│       ├── calc_engine.py     # Calculation engine
│       ├── excel_reader.py    # Excel parsing
│       ├── excel_writer.py    # Excel generation
│       ├── report_generator.py # Report creation
│       └── migrations/        # Database migrations
├── config/
│   ├── settings.py            # Django settings
│   ├── urls.py                # Main URL configuration
│   ├── wsgi.py                # WSGI configuration
│   └── asgi.py                # ASGI configuration
├── templates/                 # HTML templates
├── static/                    # CSS, JavaScript, images
├── media/                     # User uploads and reports
├── manage.py                  # Django CLI
├── requirements.txt           # Python dependencies
├── Procfile                   # Render deployment config
└── render.yaml               # Render service config
```

## Usage

### Uploading Data
1. Log in to the dashboard
2. Navigate to "Upload" section
3. Select Excel file with lab assessment data
4. Review and confirm upload

### Generating Reports
1. Go to "Reports" section
2. Select course and parameters
3. Click "Generate Report"
4. Download as PDF or Excel

### Managing Configurations
1. Access "Settings" (admin only)
2. Configure CO/PO mappings
3. Set calculation parameters
4. Save changes

## Database Models

### Key Models
- **Assessment**: Stores lab assessment records
- **StudentOutcome**: Tracks individual student attainment
- **CourseOutcome**: Defines course learning outcomes
- **ProgramOutcome**: Defines program learning outcomes
- **Configuration**: System-wide settings

## Deployment

### Deploy to Render.com

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Create Render account** at [render.com](https://render.com)

3. **Connect GitHub repository**
   - Go to Dashboard → New → Web Service
   - Connect your GitHub account
   - Select this repository

4. **Configure deployment**
   - Build command: `pip install -r requirements.txt && python manage.py migrate`
   - Start command: `gunicorn config.wsgi:application`

5. **Set environment variables** in Render dashboard:
   - `SECRET_KEY`: Generate a new Django secret key
   - `DEBUG`: `False`
   - `DATABASE_URL`: Provided by Render PostgreSQL
   - `ALLOWED_HOSTS`: Your Render domain

6. **Deploy**
   - Click "Deploy"
   - Monitor build logs
   - Application will be live in 2-5 minutes

## Environment Variables

Create a `.env` file in the root directory:

```env
# Security
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/co_po_db

# Email (optional)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-password
```

## API Endpoints

### Authentication
- `POST /login/` - User login
- `POST /register/` - User registration
- `GET /logout/` - User logout

### Processing
- `POST /upload/` - Upload assessment data
- `GET /dashboard/` - View dashboard
- `GET /process/` - Process data view

### Reports
- `GET /reports/` - List reports
- `GET /reports/<id>/` - View report details
- `GET /reports/<id>/download/` - Download report

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Roadmap

- [ ] Add REST API endpoints
- [ ] Implement real-time notifications
- [ ] Add data visualization dashboard
- [ ] Support for multiple assessment types
- [ ] Mobile app version
- [ ] Advanced analytics and AI-driven insights

## Troubleshooting

### Common Issues

**Issue**: Database migration errors
- **Solution**: Run `python manage.py migrate --run-syncdb`

**Issue**: Static files not loading
- **Solution**: Run `python manage.py collectstatic --noinput`

**Issue**: Permission denied on file uploads
- **Solution**: Ensure `media/` directory has write permissions: `chmod 755 media/`

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support & Contact

For issues, questions, or suggestions:
- Open an issue on [GitHub Issues](https://github.com/Chandu-Codes/CO-PO-Lab-Attainment-Automation/issues)
- Contact: [Your Email]

## Acknowledgments

- Django community and documentation
- Open-source contributors
- Educational institutions using this system

---

**Made with ❤️ for educational excellence**

Last Updated: June 2026
