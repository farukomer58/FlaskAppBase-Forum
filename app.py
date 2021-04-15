from app import create_app

app = create_app()

# This pretty much check if this python file is being runned DIRECTLY
if __name__ == '__main__':
    app.run(debug=True)
    print('Runned Directly')
else:
    print('Runned From Import other module/python file')