# My Business Website

A professional business website built with Flask, HTML, and CSS.

## Project Structure

```
c:\python\
├── main.py                 # Flask application
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── templates/             # HTML templates
│   ├── base.html         # Base template
│   ├── index.html        # Home page
│   ├── about.html        # About page
│   ├── services.html     # Services page
│   └── contact.html      # Contact page
└── static/               # Static files
    └── style.css         # CSS styling
```

## Setup Instructions

### 1. Activate Virtual Environment

```powershell
cd c:\python
venv\Scripts\Activate.ps1
```

### 2. Install Dependencies

```powershell
pip install -r requirements.txt
```

### 3. Run the Application

```powershell
python main.py
```

The app will start on `http://localhost:5000`

## Features

- 📱 Responsive design (works on mobile and desktop)
- 🎨 Professional HTML/CSS styling
- 📄 Multiple pages (Home, About, Services, Contact)
- 🔧 Easy to customize

## Pages

- **Home** - Hero section with features
- **About** - Company information and mission
- **Services** - Service offerings with pricing
- **Contact** - Contact form and information

## Customization

Edit the following files to personalize your site:
- `templates/base.html` - Navigation and footer
- `templates/index.html` - Home page content
- `templates/about.html` - About page content
- `templates/services.html` - Services and pricing
- `static/style.css` - Colors and styling

## Next Steps

1. Update company name and branding
2. Add your services and pricing
3. Customize colors in `style.css`
4. Deploy to a web server

