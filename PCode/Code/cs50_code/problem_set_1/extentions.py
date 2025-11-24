file = input("What's your file called?").split(".")
file = file[-1]


if file == "gif":
    print("image/gif")
elif file == "jpg":
    print("image/jpg")
elif file == "jpeg":
    print("image/jpeg")
elif file == "png":
    print("image/png")
elif file == "pdf":
    print("application/pdf")
elif file == "txt":
    print("text/plain")
elif file == "zip":
    print("application/zip")
else:
    print("application/octet-stream")