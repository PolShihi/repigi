import zipfile
import os


class ZipSerializer:
    def __init__(self, filename="output.txt", zip_path="output.zip"):
        '''
        Initializes a ZipSerializer object.

        Parameters:
        filename (str, optional): The name of the file to be archived. Default is "output.txt".
        zip_path (str, optional): The path to the ZIP archive. Default is "output.zip".
        '''

        self.filename = filename
        self.zip_path = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), zip_path)

    def archive_file(self):
        '''
        Archives the specified file in fields.
        '''

        with zipfile.ZipFile(self.zip_path, 'w') as zipf:
            zipf.write(os.path.join(os.path.dirname(os.path.abspath(
                __file__)), self.filename), arcname=self.filename)

    def get_file_info_in_archive(self):
        '''
        Retrieves information about a specific file in the ZIP archive.

        Returns:
        file_info (dict): A dictionary containing information about the file.
            ['filename'] (str): The name of the file in the archive.
            ['file_size'] (int): The size of the file in bytes.
            ['compress_size'] (int): The compressed size of the file in bytes.
            ['date_time'] (tuple): The date and time of the last modification in the format (year, month, day, hour, minute, second).
        None: if file was not founded.
        '''

        with zipfile.ZipFile(self.zip_path, 'r') as zipf:
            file_info = {}
            for file in zipf.infolist():
                if file.filename == 'output.txt':
                    file_info['filename'] = file.filename
                    file_info['file_size'] = file.file_size
                    file_info['compress_size'] = file.compress_size
                    file_info['date_time'] = file.date_time
                    break
            else:
                return None

        return file_info
