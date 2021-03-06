import webbrowser
import logging
import argparse
import pandas as pd
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

Authenticate = GoogleAuth()
Authenticate.LocalWebserverAuth()
drive = GoogleDrive(Authenticate)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


class AutoDownload(object):
    """ Class to download file/files from Google drive with the help of file URL(for single file)/
    link of Spreadsheet on google drive consisting of files URLs in case of multiple files """
    @staticmethod
    def get_file_id(url):
        """ Extracts the unique file ID from the given URL
        :param url
        :return unique file ID
        """
        file_id = url.split('/')[-2]
        return file_id

    def initiate_download(self, url):
        """ Initiates download for the given URL
        :param url
        """
        logging.info('Downloading, Please check Downloads Folder')
        webbrowser.open(r"https://drive.google.com/uc?export=download&id={}"
                        .format(self.get_file_id(url)))

    def read_checkout_xl(self, ss_url):
        """ Read the spreadsheet with file name & URL details, available on google drive,
        Extracts the file URL & name of file, with the help of file URL initiate the download for all the available URL's.
        :param ss_url
        """
        readable_url = ss_url.replace('/edit?usp=sharing', '/export?format=csv&gid=0')
        df = pd.read_csv(readable_url)
        logging.info("Reading csv for file URL's")
        x = df[['name', 'link']]
        dict_info_tst = {str(j): str(i)for i, j in
                         zip(x['name'], x['link'])}
        logging.info("Downloading {} files".format(len(dict_info_tst.keys())))
        for i in dict_info_tst.keys():
            self.initiate_download(i)
        return readable_url, bool(dict_info_tst)

    @staticmethod
    def initiate_folder_download(url):
        """ Initiates download for all files of the given folder URL(Private/Public)
            :param url
        """
        data = {}
        logging.info('Downloading all the contents of given folder')
        folder_id = (url.split('/')[-1]).replace('?usp=sharing', '')
        file_lst = drive.ListFile(
            {'q': "'{}' in parents and trashed=false".format(folder_id)}).GetList()
        for i in file_lst:
            data['id'] = i['id']
            fil_obj = drive.CreateFile(data)
            fil_obj.GetContentFile(i['title'])
            data.clear()

    def initiate_pvt_file_download(self, url):
        """ Initiates download for given private file URL
        :param url[0] URL
        :param url[1] File Name
        """
        data = {}
        data['id'] = self.get_file_id(url[0])
        fil_obj = drive.CreateFile(data)
        fil_obj.GetContentFile(url[1])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script to download file/files from Google Drive")
    parser.add_argument("--file_link", help="link to file on Drive")
    parser.add_argument("--spreadsheet", help="Link to Spreadsheet on Google drive consisting of "
                        "details of files & links")
    parser.add_argument("--folder_link", help="link to Folder (Either shared or Private) on Drive")
    parser.add_argument("--private_file_link", nargs=2, help="link to private file on Drive")
    parser.add_argument("--test", default=False, help="Initiates test")

    args = parser.parse_args()
    obj = AutoDownload()
    if args.file_link is not None:
        obj.initiate_download(args.file_link)
    if args.spreadsheet is not None:
        obj.read_checkout_xl(args.spreadsheet)
    if args.folder_link is not None:
        obj.initiate_folder_download(args.folder_link)
    if args.private_file_link is not None:
        obj.initiate_pvt_file_download(args.private_file_link)
    if args.test == 'True':
        logging.info('Testing Method: get_file_id')
        ret_id = obj.get_file_id('https://drive.google.com/file/d/1ELFoAY5e423yt0PgzzBVlspEDy7TUhke/view?usp=sharing')
        assert ret_id == '1ELFoAY5e423yt0PgzzBVlspEDy7TUhke', 'Function is returning wrong Key please check'
        logging.info('Testing Method:read_checkout_xl')
        url_val = obj.read_checkout_xl("https://docs.google.com/spreadsheets/d/1ZmjlFlHx-RY19apRQt1mUUg2i-hSti2iFNxLT96Pxws/edit?usp=sharing")
        assert '/export?format=csv&gid=0' in url_val[0], "Generated URL is not Readable by Pandas Please check the url"
        assert url_val[1]is True, "Dictionary object is Empty, Unable to Extract Data"