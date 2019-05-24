## story_image_dropped_to_grayscale_01
* image_dropped
    - action_image_acknowledged
* convert_image_to_grayscale   
    - convert_image_to_grayscale_form
    - form{"name": "convert_image_to_grayscale_form"}
    - form{"name": null}

## story_image_dropped_to_grayscale_02
* image_dropped
    - action_image_acknowledged
* convert_image_to_grayscale   
    - convert_image_to_grayscale_form
    - form{"name": "convert_image_to_grayscale_form"}
    - form{"name": null}
* thanks
    - utter_thanks
* goodbye
    - utter_goodbye

## story_image_dropped_to_grayscale_03
* greet
    - utter_greet
* image_dropped
    - action_image_acknowledged
* convert_image_to_grayscale   
    - convert_image_to_grayscale_form
    - form{"name": "convert_image_to_grayscale_form"}
    - form{"name": null}

## Story from conversation with me on May 24th 2019

* convert_image_to_grayscale
    - convert_image_to_grayscale_form
    - slot{"requested_slot":"images"}
* image_dropped{"images":[{"name":"debug_image.jpg","size":30038,"width":320,"height":180,"imageid":"FJWQ8J4TW","imagetype":"jpg","local_filename":"user_images/debug_image.jpg"}]}
    - slot{"images":[{"name":"debug_image.jpg","size":30038,"width":320,"height":180,"imageid":"FJWQ8J4TW","imagetype":"jpg","local_filename":"user_images/debug_image.jpg"}]}
    - convert_image_to_grayscale_form
    - slot{"images":[{"height":180,"imageid":"FJWQ8J4TW","imagetype":"jpg","local_filename":"user_images/debug_image.jpg","name":"debug_image.jpg","size":30038,"width":320}]}
    - slot{"requested_slot":null}

## Story from conversation with me on May 24th 2019

* greet
    - utter_greet
* convert_image_to_grayscale
    - convert_image_to_grayscale_form
    - slot{"requested_slot":"images"}
* image_dropped{"images":[{"name":"debug_image.jpg","size":30038,"width":320,"height":180,"imageid":"FJWQ8J4TW","imagetype":"jpg","local_filename":"user_images/debug_image.jpg"}]}
    - slot{"images":[{"name":"debug_image.jpg","size":30038,"width":320,"height":180,"imageid":"FJWQ8J4TW","imagetype":"jpg","local_filename":"user_images/debug_image.jpg"}]}
    - convert_image_to_grayscale_form
    - slot{"images":[{"height":180,"imageid":"FJWQ8J4TW","imagetype":"jpg","local_filename":"user_images/debug_image.jpg","name":"debug_image.jpg","size":30038,"width":320}]}
    - slot{"requested_slot":null}
