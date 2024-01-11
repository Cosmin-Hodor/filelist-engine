from filelist import Filelist

if __name__ == "__main__":
    filelist = Filelist()
    filelist.search('linux', 'all')
    filelist.download_torrent(filelist.url_dl + '60739')
