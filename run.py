from flaskr import create_app
import sys

isinitdb = False
if __name__ == '__main__':
    if len(sys.argv) > 1:
        isinitdb = bool(sys.argv[1])

app = create_app(None, isinitdb)
app.run()
