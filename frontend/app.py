from main import create_app
import os
#form dotenv import load_dotenv

app = create_app()
app.app_context().push()

if __name__=='__main__':
    app.run(debug=True, port = os.getenv('PORT'))

#load_dotenv()
#if __name__=='__main__':
#    app.run(debug=True, port = os.getenv('PORT'))