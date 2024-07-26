# Voice_enabled_upi_payment

Click on the image below to watch the video:

[![Watch the video](https://github.com/user-attachments/assets/12109dea-4cd2-412e-b3cf-8c34a5dae19b)](https://drive.google.com/file/d/11--6V_XTbVQDYDbSfbG5CmlAzz6ltXyo/view?usp=sharing)
The audio response from the computer could not be recorded but hope you get the crux of the simulation as this webapp was designed to just get you a view of how the workflow would be of such an application 
+--------------------------+
|  Start                   |
+--------------------------+
            |
            
            v
            
+--------------------------+
|  User speaks to the app
|
+--------------------------+
            |
            
            v
            
+--------------------------+
|  Convert speech to text  |
|  using SpeechRecognition |
+--------------------------+
            |
            v
+--------------------------+
|  Process the text        |
|  - Identify intent       |
|  - Extract entities      |
+--------------------------+
            |
            v
+--------------------------+
|  Perform action based    |
|  on intent               |
|  - Get balance           |
|  - Make transfer         |
+--------------------------+
            |
            v
+--------------------------+
|  Call Eyowo API          |
|  to perform action       |
+--------------------------+
            |
            v
+--------------------------+
|  Convert response text   |
|  to speech using gTTS    |
+--------------------------+
            |
            v
+--------------------------+
|  Speak the response      |
|  to the user             |
+--------------------------+
            |
            v
+--------------------------+
|  End                     |
+--------------------------+

