import socket

class Client:
    """
    Le client est grossièrement le joueur. Le code comprendra les actions suivantes :
    - call (suivre, s'aligner sur la mise précédente. Si pas assez d'argent all in et création d'un side pot)
    - check (check, quand ta mise est égale à la mise générale ne rien faire)
    - fold (se coucher)
    - bet (miser, quand la mise est à 0, au minimum la grosse blinde)
    - raise (relancer: première relance : le double; après : relance d'au moins la différence en plus)

    """
    def __init__(self) -> None:
        
    
    def receive(self, server, data_size):
        received_encoded = server.recv(data_size)
        received = received_encoded.decode("utf8")
        self.manage(received)
    
    def send(self, server, data):
        data_encoded = data.encode("utf8")
        server.sendall(data_encoded)
