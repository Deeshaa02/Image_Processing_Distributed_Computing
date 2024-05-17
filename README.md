This README will guide you to know what you will change to make this code run in your computer:
1-edit in the Master.py and GUI.py in the part of the s3 bucket and sqs to write your aws_access_key_id, aws_secret_access_key, region_name, and write the name of your s3 bucket and your sqs QueuName.
2-you will get all of this info from your aws web services account and if you don't have s3 or sqs, you must create both of them.
3-you have to open the terminal and run each line in file transfer.sh like this line  "scp -i ./belal.pem ./Master.py ec2-user@ec2-51-20-31-232.eu-north-1.compute.amazonaws.com:/home/ec2-user" but you will change the content after @ till : with the Public IPv4 DNS for each instance, and change "belal.pem" with your key.
4-you have to make this like the transfer.sh file because you will make it the first three times to push the Master.py in the three instances and the second three times to push the Slave.py.
5-then run the GUI.py in your local machine and upload image and it will work with you like i show you in the video.



link of the video:

https://drive.google.com/drive/folders/1-eJitQEzf-pOJwXPyWhRQB3kI2Th25af
