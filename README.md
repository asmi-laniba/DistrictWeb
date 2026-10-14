# Smart District+ Dashboard

An AI-Assisted, Predictive, and Citizen-Centric Web Dashboard for Intelligent District Governance.

## Features
- **Centralized Governance**: Integrated modules for Health, Education, Revenue, Public Works, and Police.
- **AI-Driven Predictions**: Machine learning models to predict project delays and resource shortages.
- **Grievance Management**: Full lifecycle management of citizen complaints with tracking IDs.
- **Role-Based Access Control (RBAC)**: Secure access for District Collectors, Department Heads, Staff, and Citizens.
- **Real-Time Analytics**: Live charts and KPI cards for district performance monitoring.
- **Automated Reporting**: One-click PDF report generation for departmental audits.
- **Security & Auditability**: Comprehensive activity logging and system-wide audit trails.

## Tech Stack
- **Backend**: Python, Django, Django REST Framework
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5, Chart.js
- **AI/ML**: Pandas, Scikit-learn, NumPy
- **Reporting**: ReportLab, xhtml2pdf
- **Database**: SQLite (Default) / PostgreSQL ready

## Quick Start
1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
2. **Setup Database**:
   ```bash
   python manage.py migrate
   python populate_data.py
   ```
3. **Run Server**:
   ```bash
   python manage.py runserver
   ```
4. **Access**:
   - Home: `http://127.0.0.1:8000/`
   - Admin Login: `admin` / `admin123`

## Roles
- **District Collector**: Full visibility and management across all departments.
- **Department Head**: Dedicated access to specific departmental data and projects.
- **Staff**: Operational access for data entry and grievance resolution.
- **Viewer/Citizen**: Public portal for grievance submission and status tracking.
