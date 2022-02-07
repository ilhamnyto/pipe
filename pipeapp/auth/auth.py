from .models import Profile, Peminatan, StatusServer
import requests as req


"""
Authentication using SSO
"""

class Authentication:

    def __init__(self):
        pass

    def Signin(self, username, password, request):
        try:
            user = Profile.objects.get(username=username)

            data = {
            "username": username,
            "password": password
            }

            headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

            login = req.post('https://gateway.telkomuniversity.ac.id/issueauth', data=data, headers=headers)

            token = login.json()

            if 'token' in token:
                if user:
                    request.session['user_login'] = request.POST['username']
                    request.session['role'] = user[0].role
                    return 'success'
                else:

                    bearertoken = {
                                "Authorization": "Bearer {tokens}".format(tokens = token['token']),
                                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
                    }

                    getprofile = req.get('https://gateway.telkomuniversity.ac.id/issueprofile', headers=bearertoken)
                    getposisi = req.get('https://gateway.telkomuniversity.ac.id/issuerole', headers=bearertoken)

                    if getprofile.status_code == 500:
                        return 'fail'

                    profile = getprofile.json()
                    posisi = getposisi.json()
                    
                    if posisi and posisi[0]['role'] == 'MAHASISWA':
                        users = Profile(
                        numberid= profile['numberid'],
                        username=request.POST['username'],
                        fullname= profile['fullname'],
                        studyprogram= profile['studyprogram'],
                        faculty= profile['faculty'],
                        schoolyear= profile['schoolyear'],
                        studentclass= profile['studentclass'],
                        lecturerguardian= profile['lecturerguardian'],
                        photo= profile['photo'],
                        role= posisi[0]['role']
                        )

                        request.session['user_login'] = request.POST['username']
                        request.session['role'] = 'MAHASISWA'
                        users.save()
                    else:
                        users = Profile(
                        numberid= profile['numberid'],
                        username=request.POST['username'],
                        fullname= profile['fullname'],
                        role='DOSEN'
                        )

                        request.session['user_login'] = request.POST['username']
                        request.session['role'] = 'DOSEN'
                        users.save()
                    return 'success'
            else:
                return "fail"
        except:
            pass

    def createStudent(self):
        pass

    def createLecture(self):
        pass

    def Signout(self, request):
        try:
            del request.session['user_login']
            del request.session['role']
        except:
            pass