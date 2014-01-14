#-*- coding: utf-8 -*-
"""
    __init__.py
    ~~~~~~~~~~~~~

    Foreign available classes

    :copyright: (c) 2013
    :license: BSD, see LICENSE for more details.
"""
from .users import LoginForm, ChangePasswordForm, SignupForm, EditAccountForm, EditMyAccountForm
from .admin import AddModuleForm, AddMachineForm, EditMachineForm, EditModuleForm
from .codes import AddCodeForm, EditCodeForm
from .cases import AddCaseForm, EditCaseForm
from .task import AddTaskForm, EditTaskForm
from .feedback import AddQuestionForm
from .tool import PmcForm, UlcCookieForm, UlcIPUAForm
