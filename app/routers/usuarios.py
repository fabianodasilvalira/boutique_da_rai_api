from datetime import datetime, timedelta
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.repositories.repositories import UsuarioRepository
from app.services.services import UsuarioService
from app.schemas.schemas import UsuarioCreate, UsuarioUpdate, UsuarioInDB, Token, TokenData

# Configuração para JWT
SECRET_KEY = "CHAVE_SECRETA_TEMPORARIA_DEVE_SER_SUBSTITUIDA_EM_PRODUCAO"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter(
    prefix="/usuarios",
    tags=["usuarios"],
    responses={404: {"description": "Usuário não encontrado"}}
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_usuario_service(db: Session = Depends(get_db)):
    repository = UsuarioRepository(db)
    return UsuarioService(repository)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciais inválidas",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    
    repository = UsuarioRepository(db)
    service = UsuarioService(repository)
    user = service.get_by_email(email=token_data.email)
    if user is None:
        raise credentials_exception
    return user


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    service: UsuarioService = Depends(get_usuario_service)
):
    user = service.authenticate(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/", response_model=List[UsuarioInDB])
def read_usuarios(
    skip: int = 0, 
    limit: int = 100, 
    service: UsuarioService = Depends(get_usuario_service),
    current_user: UsuarioInDB = Depends(get_current_user)
):
    """
    Retorna todos os usuários.
    """
    usuarios = service.get_all(skip=skip, limit=limit)
    return usuarios


@router.get("/me", response_model=UsuarioInDB)
def read_users_me(current_user: UsuarioInDB = Depends(get_current_user)):
    """
    Retorna o usuário atual.
    """
    return current_user


@router.get("/{usuario_id}", response_model=UsuarioInDB)
def read_usuario(
    usuario_id: int, 
    service: UsuarioService = Depends(get_usuario_service),
    current_user: UsuarioInDB = Depends(get_current_user)
):
    """
    Retorna um usuário específico pelo ID.
    """
    usuario = service.get(usuario_id)
    if usuario is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuário com ID {usuario_id} não encontrado"
        )
    return usuario


@router.post("/", response_model=UsuarioInDB, status_code=status.HTTP_201_CREATED)
def create_usuario(
    usuario: UsuarioCreate, 
    service: UsuarioService = Depends(get_usuario_service)
):
    """
    Cria um novo usuário.
    """
    db_user = service.get_by_email(usuario.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já registrado"
        )
    return service.create(usuario)


@router.put("/{usuario_id}", response_model=UsuarioInDB)
def update_usuario(
    usuario_id: int, 
    usuario: UsuarioUpdate, 
    service: UsuarioService = Depends(get_usuario_service),
    current_user: UsuarioInDB = Depends(get_current_user)
):
    """
    Atualiza um usuário existente.
    """
    db_usuario = service.update(usuario_id, usuario)
    if db_usuario is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuário com ID {usuario_id} não encontrado"
        )
    return db_usuario


@router.delete("/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_usuario(
    usuario_id: int, 
    service: UsuarioService = Depends(get_usuario_service),
    current_user: UsuarioInDB = Depends(get_current_user)
):
    """
    Remove um usuário.
    """
    success = service.delete(usuario_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuário com ID {usuario_id} não encontrado"
        )
    return None
