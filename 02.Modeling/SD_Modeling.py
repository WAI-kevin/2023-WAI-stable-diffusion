import numpy as np
import torch
from torch import autocast
from PIL import Image
from random import randint

import os
import argparse
    
class Text_To_Image :
    
    def __init__(self, token, prompt, seed):
        self.token = token
        self.prompt = prompt
        self.seed = seed
        pass
    
    # Text To Image
    def sd_texttoimg_pipeline(self, token):
        from accelerate import Accelerator
        from diffusers import StableDiffusionPipeline
        device = "cuda"
        accelerator = Accelerator()
        device = accelerator.device

        model_id = "CompVis/stable-diffusion-v1-4"
        pipe = StableDiffusionPipeline.from_pretrained(
            model_id,
            revision = 'fp16', 
            torch_dtype = torch.float16,
            use_auth_token=token
        ).to(device)

        return pipe
    
    def sd_texttoimg_function(self, pipe, prompt, seed):
        device = "cuda"

        if seed == "":
            seed_no = randint(1, 999999999)
        else:
            seed_no = int(seed)

        generator = torch.Generator(device=device).manual_seed(seed_no)
        with autocast(device):
            image = pipe(prompt=prompt, generator=generator)['images'][0]

        return image

class Image_To_Image :
    
    def __init__(self, token, file_name, prompt, strength, seed):
        self.token = token
        self.file_name = file_name
        self.prompt = prompt      
        self.strength = strength
        self.seed = seed
        
    
    # Text To Image
    def sd_imgtoimg_pipeline(self, token):
        from diffusers import StableDiffusionImg2ImgPipeline
        from accelerate import Accelerator
        device = "cuda"
        accelerator = Accelerator()
        device = accelerator.device
        
        model_id = "CompVis/stable-diffusion-v1-4"
        pipe = StableDiffusionImg2ImgPipeline.from_pretrained(
            model_id,
            revision="fp16", 
            torch_dtype=torch.float16,
            use_auth_token=token
        ).to(device)
        
        return pipe
    
    def sd_imgtoimg_function(self, pipe, prompt, file_name, strength, seed):
        image = Image.open(file_name).convert("RGB").resize((512,512), resample=Image.LANCZOS)

        device = "cuda"

        if seed == "" or seed == None:
            seed_no = randint(1, 999999999)
        else:
            seed_no = int(seed)

        generator = torch.Generator(device=device).manual_seed(seed_no)
        with autocast(device):
            image = pipe(prompt=prompt, init_image=image, strength=strength, guidance_scale=7.5, generator=generator).images[0]
        
        print("kr_prompt : ", prompt)    
        print("seed : ", seed_no)

        return image
    
class Image_Inpaint:
    
    def __init__(self, token, prompt, image_dir, mask_dir, seed):
        self.token = token
        self.prompt = prompt
        self.image_dir = image_dir
        self.mask_dir = mask_dir
        self.seed = seed
    
    def sd_inpaint_pipeline(self, token):
        from diffusers import StableDiffusionInpaintPipeline
        from accelerate import Accelerator
        device = "cuda"
        accelerator = Accelerator()
        device = accelerator.device
        model_id = "runwayml/stable-diffusion-inpainting"

        pipe = StableDiffusionInpaintPipeline.from_pretrained(
            model_id,
            revision="fp16", 
            torch_dtype=torch.float16,
            use_auth_token=token
        ).to(device)
        
        return pipe
    
    def sd_inpaint_function(self, pipe, prompt, image_dir, mask_dir, seed):
        import os
        from PIL import Image
        
        from accelerate import Accelerator
        
        if seed == "" or seed == None:
            seed_no = randint(0,9999999999)
        else:
            seed_no = int(seed)
        
        image = Image.open(image_dir).convert("RGB")
        mask_img = Image.open(mask_dir).convert("RGB")
                                                
        image_width, image_height = image.size
        
        resize_width = 8 * (image_width // 8)
        resize_height = 8 * (image_height // 8)
                                                
        resize_image = image.resize((resize_width, resize_height))
        resize_mask = mask_img.resize((resize_width, resize_height))
        
        device = "cuda"
        accelerator = Accelerator()
        device = accelerator.device
        generator = torch.Generator(device=device).manual_seed(seed_no) # change the seed to get different results

        result_image = pipe(
            prompt=prompt,
            image=resize_image,
            mask_image=resize_mask,
            width = resize_width,
            height = resize_height,
            guidance_scale=7.5,
            generator=generator,
            num_images_per_prompt=1,
        ).images[0]
        
        result_image.resize((image_width, image_height))                                      
        return result_image

def line_logging(*messages):
        import datetime
        import sys
        today = datetime.datetime.today()
        log_time = today.strftime('[%Y/%m/%d %H:%M:%S]')
        log = []
        for message in messages:
            log.append(str(message))
        print(log_time + '::' + ' '.join(log) + '')
        sys.stdout.flush()


def text_to_image(token, prompt, seed):

    diffusion = Text_To_Image(token, prompt, seed)
    
    try:
        image = diffusion.sd_texttoimg_function(pipe_t2i, prompt, seed)
    except:
        pipe_t2i = diffusion.sd_texttoimg_pipeline(token)
        image = diffusion.sd_texttoimg_function(pipe_t2i, prompt, seed)
        

    
    return image


def image_to_image(token, prompt, file_name, strength, seed):
    
    diffusion = Image_To_Image(token, file_name, prompt, strength, seed)
    
    try:
        image = diffusion.sd_imgtoimg_function(pipe_i2i, prompt, file_name, strength, seed)
    except:
        pipe_i2i = diffusion.sd_imgtoimg_pipeline(token)
        image = diffusion.sd_imgtoimg_function(pipe_i2i, prompt, file_name, strength, seed)
        
    return image


def image_inpaint(token, prompt, image_dir, mask_dir, seed):
    
    diffusion = Image_Inpaint(token, prompt, image_dir, mask_dir, seed)
    
    try:
        image = diffusion.sd_inpaint_function(pipe_iip, prompt, image_dir, mask_dir, seed)
    except:
        pipe_iip = diffusion.sd_inpaint_pipeline(token)
        image = diffusion.sd_inpaint_function(pipe_iip, prompt, image_dir, mask_dir, seed)
        
    return image


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--module",
        required=True,
        type=str
    )
    parser.add_argument(
        "--token",
        type=str
    )
    parser.add_argument(
        "--prompt",
        type=str
    )
    parser.add_argument(
        "--img_dir",
        type=str
    )
    parser.add_argument(
        "--mask_dir",
        type=str
    )
    parser.add_argument(
        "--seed",
        default = None,
        type=str
    )
    parser.add_argument(
        "--strength",
        type=str,
        default="0.6"
    )
    
    args = parser.parse_args()
    
    return args


def main():
    args = parse_args()
    
    # Text to Image
    if args.module == "texttoimage":
        image = text_to_image(args.token, args.prompt, args.seed)
        return image
    
    elif args.module == "imagetoimage":
        image = image_to_image(args.token, args.prompt, args.img_dir, float(args.strength), args.seed)
        return image
    
    elif args.module == "imageinpaint":
        image = image_inpaint(args.token, args.prompt, args.image_dir, args.mask_dir, args.seed)
        return image
    
    else:
        print("argument module must be 'texttoimage', 'imagetoimage', 'imageinpaint'.")
        
if __name__ == "__main__":
    main()
