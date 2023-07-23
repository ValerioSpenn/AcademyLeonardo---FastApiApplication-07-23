Ciao ragazzi!

Marco mi ha chiesto di sfruttare un piccolo codice che stavo scrivendo per un progetto per darvi un esercizio sulle API!
Spero che vi possa essere utile :)

L'esercizio consiste nello sviluppare delle chiamate API.

In questa repo ho inizializzato un codice che permette di tirare su sul vostro pc un'istanza di fastapi, un framework python per sviluppare delle chiamate API. Il codice è all'interno della cartella src.
L'obiettivo dell'esercizio è sviluppare due chiamate API:
   - Una chiamata API di tipo POST per scrivere su una coda KAFKA, un message broker.
   - Una chiamata API di tipo POST per uploadare una immagine su MINIO.

Queste stesse operazioni, in realtà, sono già state sviluppate come script Python ed è possibile visualizzare gli script nella cartella "kafka_minio_localhost".

# KAFKA
Per quanto riguarda kafka, lo script "kafka_producer" esegue proprio l'operazione di scrivere un messaggio su un topic kafka, mentre kafka consumer va a leggere sulla stessa coda.
Il file docker-compose-kafka permette di tirare su il servizio kafka sul proprio pc, permettendo di poterci interagire.
Le operazioni da eseguire quindi, sono:
1. tirare su kafka con docker-compose-kafka
2. provare il codice kafka-consuemr
3. verificare che il messaggio è stato scritto sulla coda kafka utilizzando lo script kafka_consumer.

Per eseguire il punto 1 eseguire il comando:
"docker-compose -f docker-compose-kafka.yml up" all'interno della cartella dove è presente il file.
Provate anche magari a modificare il topic e vedere se tutto funziona.
Una volta capito "il giro", andate nella cartella src/kafka e modificate il file router.py per sviluppare una chiamata di tipo POST per scrivere sulla coda. Non modificate la firma del metodo. Tenete conto che il framework FASTAPI integra già la libreria Pydantic, una libreria che permette di scrivere codice Python tipizzato.
Esempio:
async def create_tss_vitals_message(tss_vitals: TssVitals, _position_value: Position, _image_name_value: str) -> KafkaMessage:

tss_vitals è una variabile di tipo TssVitals, una classe dichiarata all'interno di src/models.
Altra cosa importante, non modificate la struttura della repo, è ispirata ad un progetto github open-source che descrive le best practice da utilizzare per FastAPI https://github.com/zhanymkanov/fastapi-best-practices#1-project-structure-consistent--predictable.

# MINIO
Per quanto riguarda Minio il discorso è analogo.
All'interno della cartella kafka_minio_localhost sono presenti degli script python che eseguono le stesse operazioni che dovete riprodurre come chiamate API.
In particolare, lo script upload_file.py esegue l'operazione di uploadare una immagine su minio, uno storage. Analogamente, lo script download_file.py esegue l'operazione di scaricare il file.
Le operazioni da eseguire quindi, sono:
1. tirare su minio con docker-compose-minio
2. Provare il codice upload_file.py (scegliere una immagine qualunque sul vostro pc)
3. verificare che l'immagine è stata uploadata eseguendo il file download_file.py
Per eseguire il punto 1 eseguire il comando:
"docker-compose -f docker-compose-minio.yml up" all'interno della cartella dove è presente il file.

Capito il "giro", l'obiettivo è replicare le operazioni all'interno del metodo post dichiarato all'interno di src/minio/upload_file.

# COMMENTO GENERALE:
Per runnare l'app, si installino i pacchetti necessari predisponendo un ambiente venv o conda, installando i pacchetti presenti in requirements, dopodiché si lanci il seguente comando all'interno della cartella SRC:
uvicorn main:app --reload

l'attributo --reload è per la fase di development, permette di possono effettuare modifiche al codice mentre il server è runnato.
http://127.0.0.1:8000.
http://127.0.0.1:8000/docs per lo swagger UI.
http://127.0.0.1:8000/openapi.json

Qualunque pacchetto python utilizziate, aggiungetelo al file requirements.txt.

Infine, potrebbe essere interessante scrivere un file bash.sh per eseguire tutte le operazioni per tirare su l'infrastruttura.
All'interno del file bash potreste scrivere i comandi per tirare su in maniera automatica i servizi di kafka e minio ed avviare il servizio di API (che a sua volta potete dockerizzare facendo un Dockerfile).

Sentitevi liberi di implementare qualsiasi cosa vogliate :D

# IMPORTANTE:
UNA VOLTA PULLATO IL VOSTRO CODICE, CREATE UN BRANCH PER OGNUNO DI VOI.
da Main, staccatevi un branch per uno chiamato main/cognomeinizialedelnome (es. main/deianaa).
Questo sarà il vostro branch principale. Dopo di ché, da questo branch, staccatevi un branch per ogni modifica che effettuate:
esempio: da main/deianaa staccatevi main/spennatov-kafka.
Quando è funzionante da main/deianaa-kafka mergiate il branch dentro quello principale main/deianaa.



