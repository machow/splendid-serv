#!/Users/machow/venv/splendid/bin/python
import os
from app import app

app.run(debug=False, threaded=False, port=int(os.environ.get('$PORT', 5000)))
