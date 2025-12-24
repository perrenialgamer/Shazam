from threading import Thread

# Import the Flask app objects from the two modules. Importing will not
# start the servers because both modules only call run() under
# `if __name__ == "__main__"`.
from app import app as app1
from app2 import app2 as app2


def run_app(flask_app, port):
    flask_app.run(port=port, debug=False, use_reloader=False)


if __name__ == "__main__":
    t1 = Thread(target=run_app, args=(app1, 5000), daemon=True)
    t2 = Thread(target=run_app, args=(app2, 5001), daemon=True)

    t1.start()
    t2.start()

    print("Started app1 at http://127.0.0.1:5000 and app2 at http://127.0.0.1:5001")
    try:
        t1.join()
        t2.join()
    except KeyboardInterrupt:
        print("Shutting down")
from threading import Thread
import sys

# Import the Flask app objects from the two modules. Importing will not
# start the servers because both modules only call run() under
# `if __name__ == "__main__"`.
from app import app as app1
from app2 import app2 as app2


def run_app(flask_app, port):
    flask_app.run(port=port, debug=False, use_reloader=False)


if __name__ == "__main__":
    t1 = Thread(target=run_app, args=(app1, 5000), daemon=True)
    t2 = Thread(target=run_app, args=(app2, 5001), daemon=True)

    t1.start()
    t2.start()

    print("Started app1 at http://127.0.0.1:5000 and app2 at http://127.0.0.1:5001")
    try:
        t1.join()
        t2.join()
    except KeyboardInterrupt:
        print("Shutting down")
