from ....model import (
    MF_String,
    MF_Text,
)

class MF_FirstName(MF_String):
    name = 'first_name'

class MF_LastName(MF_String):
    name = 'last_name'

class MF_Patronymic(MF_String):
    name = 'patronymic'

class MF_Post(MF_Text):
    name = 'post'


mf_first_name = MF_FirstName()
mf_last_name = MF_LastName()
mf_patronymic = MF_Patronymic()
mf_post = MF_Post()
