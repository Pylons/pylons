from pylons.events import NewRequest, NewResponse, subscriber


@subscriber(NewRequest)
def add_reggy(event):
    event.request.reg = True

@subscriber(NewResponse)
def add_respy(event):
    event.response.reg = True
