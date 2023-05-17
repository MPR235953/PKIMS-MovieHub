from website import create_app

# example call: http://www.omdbapi.com/?apikey=8fa3bc0c&t=Spider-Man&y=2002
API_WEBSITE = 'http://www.omdbapi.com'
API_KEY = '8fa3bc0c'

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)