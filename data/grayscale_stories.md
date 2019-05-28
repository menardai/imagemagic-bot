## story_image_dropped_to_grayscale_01
* image_dropped
    - action_image_acknowledged
* convert_image_to_grayscale   
    - convert_image_to_grayscale_form
    - form{"name": "convert_image_to_grayscale_form"}
    - form{"name": null}

## story_image_dropped_to_grayscale_01_instruction
* instruction_convert_image_to_grayscale
    - utter_instruction_convert_image_to_grayscale 
* image_dropped
    - action_image_acknowledged
* convert_image_to_grayscale   
    - convert_image_to_grayscale_form
    - form{"name": "convert_image_to_grayscale_form"}
    - form{"name": null}

## story_image_dropped_to_grayscale_01_help
* help OR advice
    - utter_capabilities
* instruction_convert_image_to_grayscale
    - utter_instruction_convert_image_to_grayscale 
* image_dropped
    - action_image_acknowledged
* convert_image_to_grayscale   
    - convert_image_to_grayscale_form
    - form{"name": "convert_image_to_grayscale_form"}
    - form{"name": null}

## story_image_dropped_to_grayscale_01_help_twice
* help OR advice
    - utter_capabilities
* instruction_convert_image_to_grayscale
    - utter_instruction_convert_image_to_grayscale 
* instruction_drop_image
    - utter_instruction_drop_image
* image_dropped
    - action_image_acknowledged
* convert_image_to_grayscale   
    - convert_image_to_grayscale_form
    - form{"name": "convert_image_to_grayscale_form"}
    - form{"name": null}

## story_image_dropped_to_grayscale_02_instruction
* instruction_convert_image_to_grayscale
    - utter_instruction_convert_image_to_grayscale 
* instruction_drop_image
    - utter_instruction_drop_image
* image_dropped
    - action_image_acknowledged
* convert_image_to_grayscale   
    - convert_image_to_grayscale_form
    - form{"name": "convert_image_to_grayscale_form"}
    - form{"name": null}

## story_image_dropped_to_grayscale_03_instruction
* instruction_convert_image_to_grayscale
    - utter_instruction_convert_image_to_grayscale 
* help OR advice
    - utter_instruction_drop_image
* image_dropped
    - action_image_acknowledged
* convert_image_to_grayscale   
    - convert_image_to_grayscale_form
    - form{"name": "convert_image_to_grayscale_form"}
    - form{"name": null}

## story_image_dropped_to_grayscale_04_instruction
* instruction_convert_image_to_grayscale
    - utter_instruction_convert_image_to_grayscale 
* image_dropped
    - action_image_acknowledged
* convert_image_to_grayscale   
    - convert_image_to_grayscale_form
    - form{"name": "convert_image_to_grayscale_form"}
    - form{"name": null}
* instruction_resize_image
    - utter_instruction_resize_image

## story_instructions_grayscale_only_01
* instruction_resize_image
    - utter_instruction_resize_image
* instruction_convert_image_to_grayscale
    - utter_instruction_convert_image_to_grayscale 

## story_instructions_grayscale_only_02
* instruction_resize_image
    - utter_instruction_resize_image
* instruction_convert_image_to_grayscale
    - utter_instruction_convert_image_to_grayscale 
* image_dropped
    - action_image_acknowledged

## story_instructions_grayscale_only_03
* instruction_resize_image
    - utter_instruction_resize_image
* instruction_convert_image_to_grayscale
    - utter_instruction_convert_image_to_grayscale 
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

## story_image_dropped_to_grayscale_02_instruction
* instruction_convert_image_to_grayscale
    - utter_instruction_convert_image_to_grayscale 
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

## story_image_dropped_to_grayscale_03_instruction
* greet
    - utter_greet
* instruction_convert_image_to_grayscale
    - utter_instruction_convert_image_to_grayscale 
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

## Story from conversation with me on May 24th 2019 - ask instruction

* convert_image_to_grayscale
    - convert_image_to_grayscale_form
    - slot{"requested_slot":"images"}
* instruction_drop_image
    - utter_instruction_drop_image
* image_dropped{"images":[{"name":"debug_image.jpg","size":30038,"width":320,"height":180,"imageid":"FJWQ8J4TW","imagetype":"jpg","local_filename":"user_images/debug_image.jpg"}]}
    - slot{"images":[{"name":"debug_image.jpg","size":30038,"width":320,"height":180,"imageid":"FJWQ8J4TW","imagetype":"jpg","local_filename":"user_images/debug_image.jpg"}]}
    - convert_image_to_grayscale_form
    - slot{"images":[{"height":180,"imageid":"FJWQ8J4TW","imagetype":"jpg","local_filename":"user_images/debug_image.jpg","name":"debug_image.jpg","size":30038,"width":320}]}
    - slot{"requested_slot":null}

## Story from conversation with me on May 24th 2019 - ask for help

* convert_image_to_grayscale
    - convert_image_to_grayscale_form
    - slot{"requested_slot":"images"}
* help
    - utter_instruction_drop_image
* image_dropped{"images":[{"name":"debug_image.jpg","size":30038,"width":320,"height":180,"imageid":"FJWQ8J4TW","imagetype":"jpg","local_filename":"user_images/debug_image.jpg"}]}
    - slot{"images":[{"name":"debug_image.jpg","size":30038,"width":320,"height":180,"imageid":"FJWQ8J4TW","imagetype":"jpg","local_filename":"user_images/debug_image.jpg"}]}
    - convert_image_to_grayscale_form
    - slot{"images":[{"height":180,"imageid":"FJWQ8J4TW","imagetype":"jpg","local_filename":"user_images/debug_image.jpg","name":"debug_image.jpg","size":30038,"width":320}]}
    - slot{"requested_slot":null}

## Story from conversation with me on May 28th 2019

* convert_image_to_grayscale
    - convert_image_to_grayscale_form
    - slot{"dim_state":null}
    - slot{"requested_slot":"images"}
* advice
    - utter_instruction_drop_image
* image_dropped{"images":[{"name":"debug_image.jpg","size":30038,"width":320,"height":180,"imageid":"FJWQ8J4TW","imagetype":"jpg","local_filename":"user_images/debug_image.jpg"}]}
    - convert_image_to_grayscale_form
    - slot{"images":[{"height":180,"imageid":"FJWQ8J4TW","imagetype":"jpg","local_filename":"user_images/debug_image.jpg","name":"debug_image.jpg","size":30038,"width":320}]}
    - slot{"dim_state":"I"}
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
