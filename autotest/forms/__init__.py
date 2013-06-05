#-*- coding: utf-8 -*-
"""
    forms.py
    ~~~~~~~~~

    autotest model code

    :copyright: (c) 2013
    :license: BSD, see LICENSE for more details.
"""
from .users import LoginForm, ChangePasswordForm, SignupForm, EditAccountForm, EditMyAccountForm
from .admin import AddModuleForm, AddMachineForm, EditMachineForm, EditModuleForm
from .codes import AddCodeForm, EditCodeForm
from .cases import AddCaseForm, EditCaseForm
from .task import AddTaskForm, EditTaskForm
from .feedback import AddQuestionForm
