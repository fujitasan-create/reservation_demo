"""Usecase層のカスタム例外"""


class ResourceNotFoundError(Exception):
    """リソースが見つからない場合の例外"""

    pass


class ReservationNotFoundError(Exception):
    """予約が見つからない場合の例外"""

    pass


class ReservationConflictError(Exception):
    """予約の時間が重複している場合の例外"""

    pass


class InvalidReservationTimeError(Exception):
    """予約時間が無効な場合の例外"""

    pass


class UserNotFoundError(Exception):
    """ユーザーが見つからない場合の例外"""

    pass


class InvalidCredentialsError(Exception):
    """認証情報が無効な場合の例外"""

    pass


class UserAlreadyExistsError(Exception):
    """ユーザーが既に存在する場合の例外"""

    pass


class UnauthorizedError(Exception):
    """認証が必要な場合の例外"""

    pass


class ForbiddenError(Exception):
    """権限が不足している場合の例外"""

    pass
