import boto3

def detect_labels(bucket,photo):
    rekog =boto3.client('rekognition')
    response = rekog.detect_labels(Image = {'S3Object' : {'Bucket': bucket, 'Name': photo}},MinConfidence=80,MaxLabels=3)

    #keep labels in dictionary
    result={}
    for labels in response['Labels']:
        result.update({labels['Name']:round(labels['Confidence'],2)})
    print('Detected labels for ',photo, result)

    return result


    
