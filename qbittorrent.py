# pyright: reportMissingImports=false
import qbittorrentapi
import logging

log = logging.getLogger(__name__)

def sizeof_fmt(num, suffix="B"):
    for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f}Yi{suffix}"

class Qbitorrent:
    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password

    def statistics(self):
        qbt_client = qbittorrentapi.Client(host=self.host, username=self.username, password=self.password)

        try:
            qbt_client.auth_log_in()
        except qbittorrentapi.LoginFailed as e:
            print(e)

        transferinfo = qbt_client.transfer_info()
        download_speed = sizeof_fmt(transferinfo.get('dl_info_speed'))
        download_total = sizeof_fmt(transferinfo.get('dl_info_data'))
        upload_speed = sizeof_fmt(transferinfo.get('up_info_speed'))+"/s"
        upload_total = sizeof_fmt(transferinfo.get('up_info_data'))
        stats = ("Download Speed: " + str(download_speed) + "\nTotal Download: " + str(download_total) + "\nUpload Speed: " + str(upload_speed) + "\nTotal Upload: " + str(upload_total))
        return(stats)