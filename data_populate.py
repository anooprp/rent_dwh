from rent_json import RentData
from util import s3_file_download,s3_delete_file

bucket='bi.redmart.com'
s3_file_path = 'Alpha/pandas/{file_name}'.format(file_name='immobilienscout24_berlin_20190113.json')
output_file='/data/CSV/immobilienscout24_berlin_20190113.json'

md=RentData()
filename=s3_file_download(bucket,s3_file_path,output_file)
s3_delete_file(bucket,s3_file_path)