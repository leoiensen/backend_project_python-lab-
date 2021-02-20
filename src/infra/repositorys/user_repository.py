# pylint: disable=E1101

from typing import List
from sqlalchemy.orm.exc import NoResultFound
from src.domain.models import Users
from src.infra.entities import Users as UsersModel
from src.infra.configs import DBConnectionHandler
from src.data.interfaces import UserRepositoryInterface


class UserRepository(UserRepositoryInterface):
    """ Class to manage User Repository """

    @classmethod
    def insert_user(cls, name: str, password: str) -> Users:
        """
        Insert data in user entity
        :param  - name: person name
                - password: user password
        :return - tuple with new user inserted informations
        """

        # Creating a Return Tuple With Informations

        with DBConnectionHandler() as db_connection:
            try:
                new_user = UsersModel(name=name, password=password)
                db_connection.session.add(new_user)
                db_connection.session.commit()

                return Users(
                    id=new_user.id, name=new_user.name, password=new_user.password
                )

            except Exception as ex:
                db_connection.session.rollback()
                print(ex)
                raise
            finally:
                db_connection.session.close()

        return None

    @classmethod
    def select_user(cls, user_id: int = None, name: str = None) -> List[Users]:
        """
        Select data in user entity by id and/or name
        :param  - id: Id of the registry
                - name: User name in database
        :return - List with UsersModel selected
        """

        try:
            query_data = None

            if user_id and not name:
                # Select user by id
                with DBConnectionHandler() as db_connection:
                    data = (
                        db_connection.session.query(UsersModel)
                        .filter_by(id=user_id)
                        .one()
                    )
                    query_data = [data]

            elif not user_id and name:
                # Select user by name
                with DBConnectionHandler() as db_connection:
                    data = (
                        db_connection.session.query(UsersModel)
                        .filter_by(name=name)
                        .all()
                    )
                    query_data = data

            elif user_id and name:
                # Select user by id and name
                with DBConnectionHandler() as db_connection:
                    data = (
                        db_connection.session.query(UsersModel)
                        .filter_by(id=user_id, name=name)
                        .one()
                    )
                    query_data = [data]

            return query_data

        except NoResultFound:
            return []
        except Exception as ex:
            db_connection.session.rollback()
            print(ex)
            raise
        finally:
            db_connection.session.close()

        return None
