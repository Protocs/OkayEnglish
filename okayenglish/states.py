from okayenglish.scenariomachine import *

ChoiceState(
    name="START",
    text="Хайооойо",
    choices=[
        Choice(
            hint="Да",
            match="да",
            next="yes",
        ),
        Choice(
            hint="Нет",
            match="не",
            next="no",
        ),
    ],
)

FinalState(
    name="yes",
    text="Чи да",
)

FinalState(
    name="no",
    text="Да чо нет та",
)
