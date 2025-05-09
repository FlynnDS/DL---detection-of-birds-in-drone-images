from typing import Dict, List, Tuple
from pydantic import BaseModel
import os
import random
import shutil
from IPython.display import Image, display
from PIL import Image as PILImage
import numpy as np

class ImageData(BaseModel):
    image_name: str
    image_paths: List[str] = list()
    label_text: str
    bird_class: int = None # 0 = crow, 1 = , 2 = , 3 = pigeon, 4 = other
    cleaned_file: str = ""

    def model_post_init(self, context):
        self.bird_class = int(self.label_text[0])

        return super().model_post_init(context)

    def get_random_image_path(self):
        random_image = random.choice(self.image_paths)
        random_image = self.image_paths[0]

        return self.image_name, random_image, self.label_text, self.bird_class

    def get_cleaned_image(self):
        display(Image(filename=self.cleaned_file))

    def get_cleaned_scaled_image(self, new_width, new_height):
        img = PILImage.open(self.cleaned_file)
        wpercent = (new_width / float(img.size[0]))
        hsize = int((float(img.size[1]) * float(wpercent)))
        img_resized = img.resize((new_width, hsize), PILImage.Resampling.LANCZOS)
        display(img_resized)

    def get_cropped_images(self, new_width):
        img = PILImage.open(self.cleaned_file)
        img_width, img_height = img.size

        bounding_boxes = self.label_text.split("\n")
        # You only want to take one of the bounding boxes to display because we only want to add one picture into another picture
        # So we take the largest one, which has the highest probability to be one that is the most complete bird
        sorted_bounding_boxes = sorted(bounding_boxes, reverse=True, key= lambda x: x[3])
        for largest_bounding_box in sorted_bounding_boxes:
            # when the data is in incorrect format
            if len(largest_bounding_box.split(" ")) != 5:
                return False
            bird_class, x_center_rel, y_center_rel, width_rel, height_rel = map(float, largest_bounding_box.split(" "))
            x_center = x_center_rel * img_width
            y_center = y_center_rel * img_height
            width = width_rel * img_width
            height = height_rel * img_height

            x_short = x_center - (0.5 * width)
            x_long = x_center + (0.5 * width)
            y_short = y_center - (0.5 * height)
            y_long = y_center + (0.5 * height)
            cropped_img = img.crop((x_short, y_short, x_long, y_long))

            # now we are scaling the cropped image to the correct size
            wpercent = (new_width / float(img_width))
            hsize = int((float(img_height) * wpercent))
            img_resized = cropped_img.resize((new_width, hsize), PILImage.Resampling.LANCZOS)
            if cropped_img.mode != "RGBA":
                print("image is in mode: ", cropped_img.mode, "converting to RGBA")
                cropped_img = cropped_img.convert("RGBA")
            # Extract alpha channel (opacity)
            alpha = img_resized.getchannel("A")

            # Convert to numpy array for efficient computation
            alpha_np = np.array(alpha, dtype=np.float32) / 255.0  # Normalize to [0,1]

            # Calculate average opacity
            avg_opacity = np.mean(alpha_np)

            # Skip image if average opacity is less than 0.05
            if avg_opacity < 0.05:
                print("the opacity is too little for the largest bounding box")
                continue

            return img_resized
        return False

class AllImages(BaseModel):
    images_dict: Dict[str, ImageData] = dict()

    def get_image_list_index(self, bird_classes: Tuple[int] = (0, 1, 2, 3, 4), cleaned_file=False):
        """gets a list of bird images that satisify the requirement of input"""
        if cleaned_file:
            found_image_dict = {index: image_name
                        for index, (image_name, image)
                          in enumerate(self.images_dict.items())
                          if image.bird_class in bird_classes and image.cleaned_file != ""}
        else:
            found_image_dict = {index: image_name
                            for index, (image_name, image)
                            in enumerate(self.images_dict.items())
                            if image.bird_class in bird_classes}
        return found_image_dict

    def get_random_instance(self, bird_classes: Tuple[int] = (0, 1, 2, 3, 4), cleaned_file=False):
        found_image_dict = self.get_image_list_index(bird_classes, cleaned_file)
        random_key = random.choice(list(found_image_dict.keys()))
        found_image = found_image_dict[random_key]
        return self.images_dict[found_image]
    
    def get_random_picture(self, bird_classes: Tuple[int] = (0, 1, 2, 3, 4)):
        
        found_image = self.get_random_instance(bird_classes)
        image_name, found_image_path, label_text, bird_class = found_image.get_random_image_path()
        display(Image(filename=found_image_path))
        return found_image_path
    
    def get_random_clean_image(self, new_width, new_height):
        image = self.get_random_instance((0, 3), True)
        print(image.image_name)
        print(image.cleaned_file)
        image.get_cleaned_scaled_image(new_width, new_height)

    def get_random_cropped_images(self, new_width):
        image = self.get_random_instance((0, 3), True)

        # Sometimes the cropped image is in the wrong format. So we recursively call this function to retry another one
        for i in range(10):
            cropped_image = image.get_cropped_images(new_width)
            if cropped_image:
                return cropped_image
        
    def get_list_of_paths_crows_pigeons(self):
        """returns all of the information of the files as a list of lists. 
        only includes pigeons and crows"""
        found_images_objects = self.get_image_list_index((0, 3))
        image_paths = [self.images_dict[image].get_random_image_path() for image in list(found_images_objects.values())]
        return image_paths
    
    def copy_crows_pigeons(self, destination_folder: str):
        crows_pigeon_paths = self.get_list_of_paths_crows_pigeons()
        crows_path = f"{destination_folder}/crows"
        pigeons_path = f"{destination_folder}/pigeons"
        if not os.path.exists(destination_folder):
            os.mkdir(destination_folder)
            os.mkdir(crows_path)
            os.mkdir(f"{crows_path}/labels")
            os.mkdir(pigeons_path)
            os.mkdir(f"{pigeons_path}/labels")
        else:
            raise Exception("folder already exists")
        
        
        for index, (image_name, image_path, label_text, bird_class) in enumerate(crows_pigeon_paths):
            bird_cat = "c" if bird_class == 0 else "p"
            image_name = f"{bird_cat}_{index}"
            if bird_class == 0:
                #shutil.copy(image_path, f"{crows_path}/{image_name}.jpg")
                shutil.copy(image_path, crows_path)
                with open(f"{crows_path}/labels/{image_name}.txt", "w") as f:
                    f.write(label_text)

            elif bird_class == 3:
                #shutil.copy(image_path, f"{pigeons_path}/{image_name}.jpg")
                shutil.copy(image_path, pigeons_path)

                with open(f"{pigeons_path}/labels/{image_name}.txt", "w") as f:
                    f.write(label_text)

    def load_removed_background_pictures(self, path: str):
        """give the folder of where the pictures are that have removed the background
        the path folder should contain two folders "pigeons" and "crows"
        """
        folders = os.listdir(path)
        if not ("pigeons" in folders and "crows" in folders):
            raise Exception("pigeons and crows doesn't exist in folder")
        
        for file in os.listdir(f"{path}/pigeons"):
            if ".DS_Store" in file:
                continue
            first_file_name = file.split(".")[0]
            self.images_dict[first_file_name].cleaned_file = f"{path}/pigeons/{file}"

        for file in os.listdir(f"{path}/crows"):
            if ".DS_Store" in file:
                continue
            first_file_name = file.split(".")[0]
            self.images_dict[first_file_name].cleaned_file = f"{path}/crows/{file}"

    def get_files_in_data_folder(self, path: str):
        images_paths = [f"{path}/images/{file_path}" for file_path in os.listdir(f"{path}/images")]
        label_file_names = [file_path for file_path in os.listdir(f"{path}/labels")]

        for label_file in label_file_names:
            if ".DS_Store" in label_file:
                continue
            # the same picture has the first part the same but might have had different augmentation
            first_file_name = label_file.split(".")[0]
            if first_file_name in self.images_dict:
                image = self.images_dict[first_file_name]
            else:
                with open(f"{path}/labels/{label_file}") as f:
                    label_text = f.read()
                image = ImageData(image_name=first_file_name,
                                  label_text=label_text)
            label_file_no_ext = os.path.splitext(label_file)[0]
            found_image = [file_name for file_name in images_paths if label_file_no_ext in file_name][0]
            image.image_paths.append(found_image)
            self.images_dict[first_file_name] = image
