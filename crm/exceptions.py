# -*- coding: utf-8 -*-


class CRMException(Exception):
    pass


class NotAllowed(CRMException):
    pass


class LoginRequired(CRMException):
    pass