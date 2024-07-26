# Voice_enabled_upi_payment

Click on the image below to watch the video:

[![Watch the video](https://github.com/user-attachments/assets/12109dea-4cd2-412e-b3cf-8c34a5dae19b)](https://drive.google.com/file/d/11--6V_XTbVQDYDbSfbG5CmlAzz6ltXyo/view?usp=sharing)
The audio response from the computer could not be recorded but hope you get the crux of the simulation as this webapp was designed to just get you a view of how the workflow would be of such an application 
+-------------------------+
|      User Input         |
| (Voice command via USB) |
+-----------+-------------+

            |
            v
            
+-----------+-------------+
|    Raspberry Pi         |
| (Processes input via    |
|  Node.js script)        |
+-----------+-------------+
            |
            v
+-----------+-------------+
|    Amazon Lex           |
| (Speech-to-Text and NLU)|
+-----------+-------------+
            |
            v
+-----------+-------------+
|    AWS Lambda           |
| (Validates input and    |
|  interacts with Eyowo)  |
+-----------+-------------+
            |
            v
+-----------+-------------+
|    Eyowo API            |
| (Processes transaction) |
+-----------+-------------+
            |
            v
+-----------+-------------+
|    Raspberry Pi         |
| (Speech synthesis via   |
|  Amazon Lex)            |
+-----------+-------------+
            |
            v
+-----------+-------------+
|    User Output          |
| (Voice response via     |
|  speaker)               |
+-------------------------+
