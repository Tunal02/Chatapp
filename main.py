from chatapp import create_app,sio

app = create_app()
sio.run(app)



