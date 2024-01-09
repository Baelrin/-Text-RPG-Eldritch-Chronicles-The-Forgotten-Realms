from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from langchain.memory import CassandraChatMessageHistory, ConversationBufferMemory
import json

cloud_config = {
    'secure_connect_bundle': 'secure-connect-the-forgotten-realms.zip'
}

with open("The_Forgotten_Realms-token.json") as f:
    secrets = json.load(f)

CLIENT_ID = secrets["clientId"]
CLIENT_SECRET = secrets["secret"]
ASTRA_DB_KEYSPACE = 'database'
OPENAI_API_KEY = ''

auth_provider = PlainTextAuthProvider(CLIENT_ID, CLIENT_SECRET)
cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
session = cluster.connect()

message_history = CassandraChatMessageHistory(
    session_id='my_session',
    session=session,
    keyspace=ASTRA_DB_KEYSPACE,
    ttl_second=3600
)

message_history.clear()

cass_buff_memory = ConversationBufferMemory(
    memory_key='chat_history',
    chat_memory=message_history
)
