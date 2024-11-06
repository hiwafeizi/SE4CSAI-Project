from app import create_app

app = create_app()

if __name__ == "__main__":
    # Get the port from the environment variable, default to 8080 if not set
    port = 8080
    app.run(host='0.0.0.0', port=port)

# if __name__ == '__main__':
#     app.run(debug=True)
