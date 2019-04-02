class FormError(BaseException):
    def __init__(this, msg):
        this.msg = msg
