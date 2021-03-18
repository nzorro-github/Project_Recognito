import boto3

bucket = 'chatlekha' 

def detect_labels(bucket):
    #---------------------------------------------
    #              Get bucket name
    #---------------------------------------------
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket)
    bucket_name = str(bucket.name)

    #---------------------------------------------
    #       Get the list of images in bucket
    #---------------------------------------------
    
    photoList = [obj.key for obj in bucket.objects.all()]

    i=1
    for photo in photoList:
        print(i,photo)
        i+=1

    #----------------------------------------------
    #    Use aws-rekognition to detect labels
    #----------------------------------------------
    rekog =boto3.client('rekognition')
    s3 = boto3.client('s3')

    #analyse the first image appears on the list
    photo_analyse = photoList[0] 
    response = rekog.detect_labels(Image = {'S3Object' : {'Bucket': bucket_name, 'Name': photo_analyse}},MinConfidence=80,MaxLabels=3)

    #keep labels in dictionary
    result={}
    for labels in response['Labels']:
        result.update({labels['Name']:round(labels['Confidence'],2)})
    print('Detected labels for ',photo_analyse, result)

    return result

detect_labels(bucket)


    