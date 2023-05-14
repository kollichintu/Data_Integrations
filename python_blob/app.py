from azure.storage.blob import  BlobClient, ContainerClient



my_connection = "DefaultEndpointsProtocol=https;AccountName=myblobstorage2023;AccountKey=hbB6ogTZ3x/OxACfxVX0JRLxlAHXbGJe1PGKQYzsHYJRPpwqlx/JJ0NofhplWBdujh/Vj2ajOPjx+AStpR27GQ==;EndpointSuffix=core.windows.net"
my_container = "mycontainer2023"
container_client = ContainerClient.from_connection_string(conn_str=my_connection, container_name=my_container)

# Upload file
input_file_path = "C:/Users/LaxmanKolli/Downloads/Introduction+To+Fastapi.pdf"
output_blob_name = "FASTAPI_Introduction.pdf"

with open(input_file_path, "rb") as data:
    container_client.upload_blob(name=output_blob_name, data=data)

input_file = "C:/Users/LaxmanKolli/Downloads/115601.jpg"
output_blob = "Quote.jpg"

with open(input_file_path, "rb") as data_upload:
    container_client.upload_blob(name=output_blob, data=data_upload)
    

#Download/fetching  a blob/file from your container
blob_downlaodfile = BlobClient.from_connection_string(conn_str=my_connection, container_name=my_container, blob_name="SQL_OrderOf_Execution.jpg")

with open("C:/Users/LaxmanKolli/Downloads/SQL_OrderOf_Execution.jpg", "wb") as my_blob:
    blob_data = blob_downlaodfile.download_blob()
    blob_data.readinto(my_blob)


    

# delete the blob from conatinmer
blob_deletefile = "Upload_to_delete.xml"
container_client.delete_blob(blob = blob_deletefile)


# Enumerating/getting  blobs
blob_list = container_client.list_blobs()
for blob in blob_list:
    print(blob.name + '\n')

    



