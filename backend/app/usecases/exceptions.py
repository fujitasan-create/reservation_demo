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

