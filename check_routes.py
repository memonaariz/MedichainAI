import app as application
a = application.create_app() if hasattr(application, 'create_app') else application.app
routes = [str(r) for r in a.url_map.iter_rules()]
tele = [r for r in routes if 'telemedicine' in r]
print("Telemedicine routes:", tele)
