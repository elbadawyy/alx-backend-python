from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth import logout

@login_required
def delete_user(request):
    user = request.user
    logout(request)      # log them out first
    user.delete()        # triggers post_delete signal
    return redirect("/") # redirect anywhere you want
