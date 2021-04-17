# audio-transcription

This project is intended to become a basic otter.ai clone, for 
speech-to-text in the browser and persisting transcriptions.

### Design

Currently the 'AI' is just the Web Speech API, and persistence is as object storage with minio. 

The Web Speech API generates for each transcription in progress both 'interim results', which are mutable, and 'final results', which are immutable. Hence this introduces a tradeoff of immutability vs. delay (wait for the Web Speech API to correct itself or persist what we currently have). Currently interim results are submitted every 5 seconds, final results upon stopping recording.

Results are submitted to the backend as HTTP post requests. May be sensible to change this to persistent connections, like Websockets.

Results are submitted to a backend server (flask), which writes to a task queue (rabbitmq) requests for persistence to minio, handled by celery workers.

```
     
Object storage
 
   /    \
   W1   Wk
    \   /
      MQ  
      |
    
    |app|
    
      |

    |web|

```



### Build and Run

Build and run with docker-compose

```docker-compose up --build```

Authenticate to the minio object storage server using the minio access key and secret key
specified by environment variables in the [docker-compose.yml](docker-compose.yml).
You should be able to access a minio UI at [http://localhost:8080](http://localhost:8080).


You should be able then start audio transcription in the browser from 
[http://localhost](http://localhost), and then see saved transcriptions 
in the 'final' and 'interim' buckets in minio through the minio UI.



Or if you don't care about saving transcriptions, launch just the frontend directly [here](https://redwrasse.github.io/audio-transcription/), hosted on github pages.




