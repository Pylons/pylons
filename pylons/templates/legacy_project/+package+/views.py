from repoze.bfg.view import bfg_view as pylons_view # ;-)

@pylons_view(route_name='new', renderer='templates/index.pt')
def index_view(request):
    return {}


    
    
