from pydantic import BaseModel

# Token schemas used for JWT authentication responses and payloads.
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenPayload(BaseModel):
    sub: str | None = None