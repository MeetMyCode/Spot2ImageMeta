import os
import subprocess
import xattr
import plistlib
import pyexiv2

def get_spotlight_comment(image_path):
    try:
        # AppleScript command to retrieve the Spotlight comment
        applescript = f'''
            tell application "Finder"
                set commentText to comment of (POSIX file "{image_path}" as alias)
            end tell
            return commentText
        '''

        # Execute the AppleScript command and capture the output
        result = subprocess.run(['osascript', '-e', applescript], stdout=subprocess.PIPE, text=True)

        # Extract the Spotlight comment from the output
        spotlight_comment = result.stdout.strip()
        print(f"Spotlight comment retrieved via applescript is: {spotlight_comment}")
        
        return spotlight_comment
    except Exception as e:
        print(f"Error retrieving Spotlight comment for {image_path}: {str(e)}")



def update_caption_metadata(image_path, new_caption):
    try:
        
        # Open the image using pyexiv2
        image = pyexiv2.Image(image_path)

        # Update the IPTC caption metadata
        image.modify_iptc({'Iptc.Application2.Caption':new_caption})
        #image['Iptc.Application2.Caption'] = new_caption
        
        # Close the image to free uo memory and avoid a leak.
        image.close()

        print(f"Updated caption metadata for: {image_path}")
        
    except Exception as e:
        print(f"Error updating caption metadata for {image_path}: {str(e)}")


def copy_spotlight_comment(image_path):
    spotlight_comment = get_spotlight_comment(image_path)
    #print(f"spotlight_comment is: {spotlight_comment}")
    #print(f"type is: {type(spotlight_comment)}")

        
    if type(spotlight_comment) == str and len(spotlight_comment) > 0:
        try:            
            update_caption_metadata(image_path, spotlight_comment)
            
            # AppleScript to delete the Spotlight comment
            applescript = f'''
                tell application "Finder"
                    set comment of (POSIX file "{image_path}" as alias) to ""
                end tell
            '''

            # Execute the AppleScript through subprocess
            subprocess.run(['osascript', '-e', applescript])

            
            print(f"Processed: {image_path}")
            
        except Exception as e:
            print(f"Error processing {image_path}: {str(e)}")
            
    else:
        print(f"No spotlight comment found for: {image_path}")

def process_directory(directory):
    for root, _, files in os.walk(directory):
        for file_name in files:
            # Check if the file is an image (you can add more image extensions if needed)
            if file_name.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                image_path = os.path.join(root, file_name)
                print(f"image_path is: {image_path}")
                copy_spotlight_comment(image_path)

if __name__ == "__main__":
    from PIL import Image, ImageOps  # Import Image here to avoid previous issues
    input_directory = "./"
    process_directory(input_directory)


print("Spotlight comments removed from all images in the directory and its subdirectories.")




