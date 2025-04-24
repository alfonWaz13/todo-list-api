from source.models import ToDos


class ToDoBuilder:

    @staticmethod
    def create_with_index_and_title(todo_id: int, title: str) -> ToDos:
        return ToDos(
            id=todo_id,
            title=title,
            description='ToDo Description',
            priority=1,
            completed=False,
        )
