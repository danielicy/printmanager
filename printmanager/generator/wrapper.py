

import uuid
import logging
from PIL import Image, ImageDraw, ImageFont
import os
from jobs.models import ContentStore,JobsStatus, SessionKeyValueLog
from common.functions import get_jobstatus, get_jobtype
from common import settings 
log = logging.getLogger(__name__)



     

def process(t):
  
    try :
        log.info(f">>>>>>>>>>>>  Starting - generator_ {t} >>>>>>>>>>>>>>>>>>>>>>>>>" )
        generateImage('')
        log.info(f"********************* generating image finished *********************")
   
    except Exception as e :
        log.exception(f"exception in process generator_ # e :" + e)
        raise e
   

def process_job(job_id,t):        
    try:
        generateImage(job_id)
    except :
        pass
    log.error(f"If you see a lot of this messages probably you need implement inputWatcher process_job function.[job_id=%i]" % (job_id))
        


def generateImage(job_id):
    current_directory = os.path.dirname(os.getcwd())
    print(current_directory)
    path =os.path.join(current_directory, r'docs')
    background_path = os.path.join(path, "beamer.jpg")
    person_image_path = os.path.join(path, "Quantum Team.png")
    output_path = os.path.join(path, "output.jpg")

    # Load images
    background = Image.open(background_path).convert("RGB")
    person_image = Image.open(person_image_path).convert("RGB")

    # Resize person image
    picture_width = 360
    picture_height = 352
    person_image = person_image.resize((picture_width, picture_height), Image.LANCZOS)

    # Overlay person image onto background
    picture_x = 330
    picture_y = 300
    background.paste(person_image, (picture_x, picture_y))

    # Add text over the image
    text = "Quantum Leap"
    text_x = 380
    text_y = 830
    font_size = 30
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        font = ImageFont.load_default()
    draw = ImageDraw.Draw(background)
    draw.text((text_x, text_y), text, font=font, fill=(255, 255, 255))

    # Save the final image
    background.save(output_path, "JPEG")        