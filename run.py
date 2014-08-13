#!/Users/machow/venv/splendid/bin/python
import os
from app import app
port = os.environ.get('$PORT') or 5000
app.run(threaded=False, port=port)
