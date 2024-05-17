import boto3
from tkinter import Tk, Label, Button, StringVar, OptionMenu, Frame
from PIL import Image, ImageTk
from tkinter import filedialog
import os
import numpy as np
import cv2


img_paths = []
img_photos = []


def upload_images():
    global img_paths, img_photos
    img_paths = filedialog.askopenfilenames()
    img_photos = []
    for img_path in img_paths:
        img = Image.open(img_path)
        img.thumbnail((100, 100))
        img_photos.append((img_path, ImageTk.PhotoImage(img)))
    display_images()


def display_images():
    for widget in image_frame.winfo_children():
        widget.destroy()

    for img_path, img_photo in img_photos:
        img_label = Label(image_frame, image=img_photo)
        img_label.image = img_photo
        img_label.pack(side='left', padx=5, pady=5)


def start_processing():
    global img_paths
    operation = operation_var.get()
    if img_paths:
        upload_to_s3(img_paths, operation)
        result_label.config(text="Images and operations uploaded successfully.")


def upload_to_s3(file_paths, operation):
    s3 = boto3.client(
        's3',
        aws_access_key_id="AKIAZQ3DOAQLK2OVI2LD",
        aws_secret_access_key="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",
        region_name="eu-north-1"
    )
    bucket_name = 'belalsbucket'
    uploaded_files = []
    for img_path in file_paths:
        file_name = os.path.basename(img_path)
        operation_metadata = {'operation': operation}
        s3_key = f'{file_name}-{operation}'
        with open(img_path, 'rb') as file_data:
            s3.upload_fileobj(file_data, bucket_name, s3_key,
                              ExtraArgs={'Metadata': operation_metadata})
        uploaded_files.append(s3_key)
        print(f"Uploaded {img_path} as {s3_key}")

    sqs = boto3.client(
        'sqs',
        aws_access_key_id="AKIAZQ3DOAQLK2OVI2LD",
        aws_secret_access_key="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",
        region_name="eu-north-1"
    )

    message_count = 0
    print("Waiting for messages")
    while True:
        response = sqs.receive_message(
            QueueUrl="https://sqs.eu-north-1.amazonaws.com/654654178326/belalqueue.fifo",
            AttributeNames=['All'],
            MaxNumberOfMessages=len(uploaded_files),
            WaitTimeSeconds=20
        )
        messages = response.get('Messages', [])
        if messages:
            for message in messages:
                img_rcv = message['Body']
                print(f"Received message for image {img_rcv}")
                try:
                    img = s3.get_object(Bucket='belalsbucket', Key=img_rcv)['Body'].read()
                    nparray = cv2.imdecode(np.asarray(bytearray(img)), cv2.IMREAD_COLOR)
                    cv2.imwrite(f"./output/{img_rcv}.jpg", nparray)
                    print(f"Processed and saved {img_rcv}")

                    # Delete the object and message
                    s3.delete_object(Bucket='belalsbucket', Key=img_rcv)
                    sqs.delete_message(
                        QueueUrl="https://sqs.eu-north-1.amazonaws.com/654654178326/belalqueue.fifo",
                        ReceiptHandle=message['ReceiptHandle']
                    )
                    message_count += 1
                except s3.exceptions.NoSuchKey:
                    print(f"Error: The key {img_rcv} does not exist in the bucket.")

        if message_count == len(uploaded_files):
            break
    print("Messages received")


root = Tk()
root.title("Image Processing")
root.geometry("600x400")

background_image = Image.open("bblue.jpg")
background_photo = ImageTk.PhotoImage(background_image)
background_label = Label(root, image=background_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

upload_button = Button(root, text="Upload Images", command=upload_images)
upload_button.pack(pady=10)

operations = ['Edge Detection', 'Color Inversion', 'Blurring', 'Thresholding', 'Sharpening',
              'Opening', 'Image Enhancement']
operation_var = StringVar(root)
operation_var.set(operations[0])
operation_menu = OptionMenu(root, operation_var, *operations)
operation_menu.pack(pady=10)

process_button = Button(root, text="Upload and Process Images", command=start_processing)
process_button.pack(pady=10)

image_frame = Frame(root)
image_frame.pack(pady=10)

result_label = Label(root)
result_label.pack(pady=10)

root.mainloop()

