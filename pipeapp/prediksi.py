from pipeapp.models import Profile
import pandas as pd
from .dburl import engine
from django.shortcuts import redirect, render
from .decorator import login_required, role_required



@login_required()
@role_required(allowed_roles=['ADMIN'])
def prediksikelulusan(request):
  user = Profile.objects.get(username=request.session['user_login'])
  df = pd.read_sql('SELECT * FROM prediksikelulusan', con=engine)
  
  return render(request, 'kelulusan.html', {'user': user, "df": df.to_html(index=False, justify='left', classes='table borderless', table_id='tablekelulusan', border=0)})

@login_required()
@role_required(allowed_roles=['ADMIN'])
def prediksipeminatan(request):
  user = Profile.objects.get(username=request.session['user_login'])
  df = pd.read_sql('SELECT * FROM prediksipeminatan', con=engine)

  return render(request, 'peminatan.html', {'user': user, "df": df.to_html(index=False, justify='left', classes='table borderless', table_id='tablepeminatan', border=0)})