from users.repository import UsersRepository


class UserUtils:

    @staticmethod
    def get_user_by_id(user_id):
        return UsersRepository.get_user_by_id(user_id)