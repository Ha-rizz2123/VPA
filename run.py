from app import create_app

app = create_app()

if __name__ == "__main__":
    print("Registered Routes:")
    for rule in app.url_map.iter_rules():
        print(f"{rule} -> {rule.endpoint}")
    app.run(debug=True)
