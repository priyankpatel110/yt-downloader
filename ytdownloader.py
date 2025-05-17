import yt_dlp

link = input("Enter your link here:")

yt_dlp.YoutubeDL({'format': 'best', 'outtmpl': '%(title)s.%(ext)s'}).download([link])