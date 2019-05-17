## story_greet <!--- The name of the story. It is not mandatory, but useful for debugging. --> 
* greet <!--- User input expressed as intent. In this case it represents users message 'Hello'. --> 
    - utter_greet <!--- The response of the chatbot expressed as an action. In this case it represents chatbot's response 'Hello, how can I help?' --> 
 
## story_goodbye
* goodbye
    - utter_goodbye

## story_thanks
* thanks
    - utter_thanks
 
## story_name
* name{"name":"Sam"}
    - utter_greet_name
 

## story_image_dropped
* image_dropped
    - action_image_acknowledged


## story_resize_01
* resize
    - resize_form
    - form{"name": "resize_form"}
    - form{"name": null}


## story_resize_02
* greet
    - utter_greet
* name{"name":"Anne"} <!--- User response with an entity. In this case it represents user message 'My name is Lucy.' --> 
    - utter_greet_name
* resize
    - resize_form
    - form{"name": "resize_form"}
    - form{"name": null}
* thanks
    - utter_thanks
* goodbye
    - utter_goodbye 


## story_image_dropped_resize_01  <!-- happy path -->
* image_dropped
    - action_image_acknowledged
* resize
    - resize_form
    - form{"name": "resize_form"}
    - form{"name": null}
