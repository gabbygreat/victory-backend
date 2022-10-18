import cloudinary
import cloudinary.uploader
import cloudinary.api

cloudinary.config( 
  cloud_name = "duxqhu7ht", 
  api_key = "686591122674433", 
  api_secret = "iyfnRpQzIEio6wGnjxka0LIl00M" 
)

cloudinary.uploader.upload("C:/Users/HP/Downloads/images.png", 
  folder = "myfolder/mysubfolder/", 
  public_id = "my_dog",
  overwrite = True, 
  notification_url = "https://mysite.example.com/notify_endpoint", 
  resource_type = "image")