## story_image_dropped
* image_dropped
    - action_image_acknowledged

## story_resize_01
* resize_image
    - resize_image_form
    - form{"name": "resize_image_form"}
    - form{"name": null}

## story_resize_02
* greet
    - utter_greet
* name{"name":"Anne"} <!--- User response with an entity. In this case it represents user message 'My name is Lucy.' --> 
    - utter_greet_name
* resize_image
    - resize_image_form
    - form{"name": "resize_image_form"}
    - form{"name": null}
* thanks
    - utter_thanks
* goodbye
    - utter_goodbye

<!-- resize image - happy path -->

## story_image_dropped_resize_01
* image_dropped
    - action_image_acknowledged
* resize_image
    - resize_image_form
    - form{"name": "resize_image_form"}
    - form{"name": null}

## Story from conversation with me on May 23rd 2019

* greet
    - utter_greet
* image_dropped{"images":[{"name":"debug_image.jpg","size":30038,"width":320,"height":180,"imageid":"FJWQ8J4TW","imagetype":"jpg","local_filename":"user_images/debug_image.jpg"}]}
    - slot{"images":[{"name":"debug_image.jpg","size":30038,"width":320,"height":180,"imageid":"FJWQ8J4TW","imagetype":"jpg","local_filename":"user_images/debug_image.jpg"}]}
    - action_image_acknowledged
* resize_image{"width":800,"height":600}
    - slot{"height":600}
    - slot{"width":800}
    - resize_image_form
    - slot{"width":800}
    - slot{"height":600}
    - slot{"images":[{"height":180,"imageid":"FJWQ8J4TW","imagetype":"jpg","local_filename":"user_images/debug_image.jpg","name":"debug_image.jpg","size":30038,"width":320}]}
    - slot{"width":800}
    - slot{"height":600}
    - slot{"requested_slot":null}
* thanks
    - utter_thanks

## Story from conversation with me on May 23rd 2019

* resize_image{"width":800,"height":600}
    - slot{"height":600}
    - slot{"width":800}
    - resize_image_form
    - slot{"width":800}
    - slot{"height":600}
    - slot{"width":800}
    - slot{"height":600}
    - slot{"requested_slot":"images"}
* image_dropped{"images":[{"name":"debug_image.jpg","size":30038,"width":320,"height":180,"imageid":"FJWQ8J4TW","imagetype":"jpg","local_filename":"user_images/debug_image.jpg"}]}
    - slot{"images":[{"name":"debug_image.jpg","size":30038,"width":320,"height":180,"imageid":"FJWQ8J4TW","imagetype":"jpg","local_filename":"user_images/debug_image.jpg"}]}
    - resize_image_form
    - slot{"images":[{"height":180,"imageid":"FJWQ8J4TW","imagetype":"jpg","local_filename":"user_images/debug_image.jpg","name":"debug_image.jpg","size":30038,"width":320}]}
    - slot{"requested_slot":null}

## Story from conversation with me on May 23rd 2019

* greet
    - utter_greet
* resize_image{"width":800,"height":600}
    - slot{"height":600}
    - slot{"width":800}
    - resize_image_form
    - slot{"width":800}
    - slot{"height":600}
    - slot{"width":800}
    - slot{"height":600}
    - slot{"requested_slot":"images"}
* image_dropped{"images":[{"name":"debug_image.jpg","size":30038,"width":320,"height":180,"imageid":"FJWQ8J4TW","imagetype":"jpg","local_filename":"user_images/debug_image.jpg"}]}
    - slot{"images":[{"name":"debug_image.jpg","size":30038,"width":320,"height":180,"imageid":"FJWQ8J4TW","imagetype":"jpg","local_filename":"user_images/debug_image.jpg"}]}
    - resize_image_form
    - slot{"images":[{"height":180,"imageid":"FJWQ8J4TW","imagetype":"jpg","local_filename":"user_images/debug_image.jpg","name":"debug_image.jpg","size":30038,"width":320}]}
    - slot{"requested_slot":null}

## Story from conversation with me on May 23rd 2019

* resize_image
    - resize_image_form
    - slot{"requested_slot":"images"}
* image_dropped{"images":[{"name":"debug_image.jpg","size":30038,"width":320,"height":180,"imageid":"FJWQ8J4TW","imagetype":"jpg","local_filename":"user_images/debug_image.jpg"}]}
    - slot{"images":[{"name":"debug_image.jpg","size":30038,"width":320,"height":180,"imageid":"FJWQ8J4TW","imagetype":"jpg","local_filename":"user_images/debug_image.jpg"}]}
    - resize_image_form
    - slot{"images":[{"height":180,"imageid":"FJWQ8J4TW","imagetype":"jpg","local_filename":"user_images/debug_image.jpg","name":"debug_image.jpg","size":30038,"width":320}]}
    - slot{"requested_slot":"width"}
* single_number_answer
    - resize_image_form
    - slot{"width":"800"}
    - slot{"requested_slot":"height"}
* single_number_answer
    - resize_image_form
    - slot{"height":"600"}
    - slot{"requested_slot":null}

## Story from conversation with me on May 23rd 2019

* image_dropped{"images":[{"name":"debug_image.jpg","size":30038,"width":320,"height":180,"imageid":"FJWQ8J4TW","imagetype":"jpg","local_filename":"user_images/debug_image.jpg"}]}
    - slot{"images":[{"name":"debug_image.jpg","size":30038,"width":320,"height":180,"imageid":"FJWQ8J4TW","imagetype":"jpg","local_filename":"user_images/debug_image.jpg"}]}
    - action_image_acknowledged
* resize_image{"width":800}
    - slot{"width":800}
    - resize_image_form
    - slot{"images":[{"height":180,"imageid":"FJWQ8J4TW","imagetype":"jpg","local_filename":"user_images/debug_image.jpg","name":"debug_image.jpg","size":30038,"width":320}]}
    - slot{"width":800}
    - slot{"width":800}
    - slot{"requested_slot":"height"}
* single_number_answer
    - resize_image_form
    - slot{"height":"600"}
    - slot{"requested_slot":null}

## Story from conversation with me on May 23rd 2019

* resize_image{"height":600}
    - slot{"height":600}
    - resize_image_form
    - slot{"height":600}
    - slot{"height":600}
    - slot{"requested_slot":"images"}
* image_dropped{"images":[{"name":"debug_image.jpg","size":30038,"width":320,"height":180,"imageid":"FJWQ8J4TW","imagetype":"jpg","local_filename":"user_images/debug_image.jpg"}]}
    - slot{"images":[{"name":"debug_image.jpg","size":30038,"width":320,"height":180,"imageid":"FJWQ8J4TW","imagetype":"jpg","local_filename":"user_images/debug_image.jpg"}]}
    - resize_image_form
    - slot{"images":[{"height":180,"imageid":"FJWQ8J4TW","imagetype":"jpg","local_filename":"user_images/debug_image.jpg","name":"debug_image.jpg","size":30038,"width":320}]}
    - slot{"requested_slot":"width"}
* single_number_answer
    - resize_image_form
    - slot{"width":"800"}
    - slot{"requested_slot":null}
* thanks
    - utter_thanks

## Story from conversation with me on May 23rd 2019

* resize_image{"height":600}
    - slot{"height":600}
    - resize_image_form
    - slot{"height":600}
    - slot{"height":600}
    - slot{"requested_slot":"images"}
* image_dropped{"images":[{"name":"debug_image.jpg","size":30038,"width":320,"height":180,"imageid":"FJWQ8J4TW","imagetype":"jpg","local_filename":"user_images/debug_image.jpg"}]}
    - slot{"images":[{"name":"debug_image.jpg","size":30038,"width":320,"height":180,"imageid":"FJWQ8J4TW","imagetype":"jpg","local_filename":"user_images/debug_image.jpg"}]}
    - resize_image_form
    - slot{"images":[{"height":180,"imageid":"FJWQ8J4TW","imagetype":"jpg","local_filename":"user_images/debug_image.jpg","name":"debug_image.jpg","size":30038,"width":320}]}
    - slot{"requested_slot":"width"}
* resize_image{"width":800}
    - slot{"width":800}
    - resize_image_form
    - slot{"width":800}
    - slot{"requested_slot":null}

## Story from conversation with me on May 23rd 2019

* image_dropped{"images":[{"name":"debug_image.jpg","size":30038,"width":320,"height":180,"imageid":"FJWQ8J4TW","imagetype":"jpg","local_filename":"user_images/debug_image.jpg"}]}
    - slot{"images":[{"name":"debug_image.jpg","size":30038,"width":320,"height":180,"imageid":"FJWQ8J4TW","imagetype":"jpg","local_filename":"user_images/debug_image.jpg"}]}
    - action_image_acknowledged
* resize_image
    - resize_image_form
    - slot{"images":[{"height":180,"imageid":"FJWQ8J4TW","imagetype":"jpg","local_filename":"user_images/debug_image.jpg","name":"debug_image.jpg","size":30038,"width":320}]}
    - slot{"requested_slot":"width"}
* resize_image{"width":800}
    - slot{"width":800}
    - resize_image_form
    - slot{"width":800}
    - slot{"requested_slot":"height"}
* resize_image{"height":600}
    - slot{"height":600}
    - resize_image_form
    - slot{"height":600}
    - slot{"requested_slot":null}

