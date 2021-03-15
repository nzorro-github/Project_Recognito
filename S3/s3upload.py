import logging
import boto3
from botocore.exceptions import ClientError
import subprocess

# this function return the list of objects (files) already existing in the given bucket
def get_existing_objects(bucket_name):
    existing_objs_list = []

    s3_resource = boto3.resource('s3')

    # get the bucket with name = bucket_name
    bucket = s3_resource.Bucket(bucket_name)

    # prefix in AWS S3 is a way to organize objects (files) in a sort of folders
    prefix = 'images/'

    # get filenames (keys) of all objects with Prefix = prefix
    for obj in bucket.objects.filter(Prefix = prefix):
        object_name = obj.key.replace(prefix,'')    # remove prefix from object key to get just the key
        if len(object_name) > 0:    
            existing_objs_list.append(object_name)


    return existing_objs_list


# the function to upload the file to the given bucket
def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True



# START OF MAIN

print('### Utility to Upload files to S3: ###\n')

# getting the list of files to choose from the local computer
path = '/Users/Nzorro/Pictures/S3Uploads/'
output = subprocess.run(['ls',path],stdout=subprocess.PIPE, text=True).stdout.split('\n')

# the bucket where the uploads are going to
bucket_name = 'nz-images-bucket'

options_list = []
for file in output:
    if len(file) > 0:
        options_list.append(file)

print('The existing files are:')
for num, option in enumerate(options_list):
    print(str(num+1) + " - "  + option)

file_option = int(input('\nEnter the file option (e.g. 1) from the list provided:'))


if file_option > 0 and file_option <= len(options_list): # If valid file option
    file_name = options_list[file_option - 1]
    print('File to Upload: ', file_name)
    uploadYN = input('Proceed with Upload Y/N?').upper()

    if uploadYN == 'Y':

        #get the list of existing file to compare to the file we want to upload
        existing_objs_list = get_existing_objects(bucket_name)

        if not file_name in existing_objs_list: #if file to upload doesn't exist in the existing_obj_list
            print('\nUploading ' + file_name + '...')

            prefix = 'images/'
            if upload_file(path + file_name, bucket_name, prefix + file_name):
                print('Upload Successful!')
            else:
                print('Error trying to upload!')
        else:
            print(f'{file_name} already exists in {bucket_name}')
            print('Upload aborted!')

else:
    print('Invalid option!')