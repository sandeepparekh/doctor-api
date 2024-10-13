from slowapi import Limiter
from slowapi.util import get_remote_address

# Initialize the Limiter with the function that fetches the remote address
limiter = Limiter(key_func=get_remote_address)
