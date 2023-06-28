from flask import Flask, render_template, request, redirect
import boto3

app = Flask(__name__)

client = boto3.client('s3')
s3=boto3.resource('s3')

def handle_error(error):
    error_message=str(error)
    return render_template('errors.html',error=error_message)

#main UI
@app.route('/')
def home():
    return render_template('index.html')

#list all the buckets
# @app.route('/list')
# def listing():
#     list_buckets=client.list_buckets()
#     # print(list_buckets)
#     buckets2=list_buckets['Buckets']
#     print(buckets2)
#     return buckets2

# List all the buckets
@app.route('/list')
def listing():
        list_buckets = client.list_buckets()
        buckets = [bucket['Name'] for bucket in list_buckets['Buckets']]
        return render_template('listing.html', buckets=buckets)



#create buckets
@app.route('/create_bucket',methods = ['POST'])
def create_bucket():
    try:
        bucket_name=request.form['bucket_name']
        response = client.create_bucket(
        Bucket=bucket_name,CreateBucketConfiguration={
            'LocationConstraint': 'ap-south-1'    }
        )
        return render_template('sucess.html')
    except Exception as e:
        return render_template('errors.html',error='error creating bucket ')
    except client.exceptions.BucketAlreadyExists as e:
        return render_template('errors.html',error='bucket already exists')


#list objects in bucket
@app.route('/list_obj',methods=['POST'])
def list_obj():
    try:
        bucket_name=request.form['bucket_name']
        response = s3.Bucket(bucket_name)
        obj=[]
        for response in response.objects.all():
             obj.append(response.key)  
        return render_template('list_obj.html',obj=obj)
    except Exception as e:
        return handle_error(error='Failed to list objects in bucket, please check bucket name ')


#upload files to bucket
@app.route('/upload',methods=['POST'])
def upload():
    try:
        bucket_name=request.form['bucket_name']
        file=request.files['file']
        file_name=file.filename
        client.upload_fileobj(file,bucket_name,file_name)
        return render_template('sucess.html')
    except Exception as e:
        return handle_error(error='Failed to upload files, please check bucket name ')
    
# create folders in buckets
@app.route('/create_folder',methods=['POST'])
def folders():
    try:
        bucket_name=request.form['bucket_name']
        folder_name=request.form['folder_name']
        response = client.put_object(
            Bucket=bucket_name,
            Key=(folder_name+'/')
            )
        return render_template('sucess.html')
    except Exception as e:
        return handle_error(error='Failed to create folder, please check bucket name ')
    

#delete objects
@app.route('/delete_obj',methods=['POST'])
def delete_obj():
    try:
        bucket_name=request.form['bucket_name']
        file_name=request.form['filename']
        response = client.delete_object(
            Bucket=bucket_name,
            Key=file_name
            )
        return render_template('sucess.html')
    except Exception as e:
        return handle_error(error='Failed to delete files, please check bucket and file  name ')


#delete bucket
@app.route('/dele_buc',methods=['POST'])
def delete_buc():
    try:
        bucket_name=request.form['bucket_name']
        response = client.delete_bucket(
            Bucket=bucket_name
        )
        return render_template('sucess.html')
    except Exception as e:
        return handle_error(error='Failed to delete bucket, please ensure bucket name is correct and empty ')
    
#copying object
@app.route('/copy_obj',methods=['POST'])
def copy_obj():
    try:
        src_bucket_name=request.form['src_bucket_name']
        src_file_name=request.form['src_filename']
        dest_bucket_name=request.form['dest_bucket_name']
        dest_file_name=request.form['dest_filename']
        response = client.copy_object(
            Bucket=dest_bucket_name,
            Key=dest_file_name,
            CopySource={'Bucket':src_bucket_name, 'Key': src_file_name}
    )
        return render_template('sucess.html')
    except Exception as e:
        return handle_error(error='Failed to copy files  please enter correct names  ')

#move objects
@app.route('/move_obj',methods=['POST'])
def move_obj():
    try:

        src_bucket_name=request.form['src_bucket_name']
        src_file_name=request.form['src_filename']
        dest_bucket_name=request.form['dest_bucket_name']
        dest_file_name=request.form['dest_filename']
        response = client.copy_object(
            Bucket=dest_bucket_name,
            Key=dest_file_name,
            CopySource={'Bucket':src_bucket_name, 'Key': src_file_name}
        )
        return render_template('sucess.html')
    except Exception as e:
        return handle_error(error='Failed to copy files  please enter correct names  ')

