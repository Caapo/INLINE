from domain.entities.user import User
from domain.repositories.i_user_repository import IUserRepository

# ================ CLASS UserService ================ (Utilise le repository pour la persistance)

class UserService:

    def __init__(self, user_repository:IUserRepository):
        self.__user_repository = user_repository

    # ---------------------------------------------------

    #Permet de créer un nouvel utilisateur (vérifie également s'il n'existe pas déjà)
    def create_user(self, email:str, username:str) -> User:
        existing_email = self.__user_repository.find_user_by_email(email)
        if existing_email:
            raise ValueError("Cet email est déjà utilisé. Veuillez en choisir un autre.")
        user = User(email=email, username=username)
        self.__user_repository.save_user(user)
        return user