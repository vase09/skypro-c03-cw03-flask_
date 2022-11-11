from project.config import DevelopmentConfig
from project.server import create_app

app = create_app(DevelopmentConfig)
app.config.from_envvar("APP_SETTINGS", silent=True)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port='25000')
