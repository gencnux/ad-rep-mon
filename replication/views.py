from django.shortcuts import render
from .utils import get_replication_status

def dashboard(request):
    result = get_replication_status()
    
    if 'error' in result:
        error_msg = result['error']
        if 'No replication data found' in error_msg:
            context = {'warning': 'Replication data not found, but connection successful'}
        else:
            context = {'error': error_msg}
    else:
        context = {'replication_data': result['data']}
    
    return render(request, 'replication/dashboard.html', context)