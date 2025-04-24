from fastapi.testclient import TestClient
from starlette import status

from application import app
from source.database import get_db
from source.models import Base, ToDos
from tests.config import engine, TestingSessionLocal, override_db

from tests.todos_builder import ToDoBuilder


class TestToDo:

    @classmethod
    def setup_class(cls):
        Base.metadata.create_all(bind=engine)
        app.dependency_overrides[get_db] = override_db
        cls.client = TestClient(app)

    @classmethod
    def setup_method(cls):
        db = TestingSessionLocal()
        db.query(ToDos).delete()

        todo1 = ToDoBuilder.create_with_index_and_title(todo_id=0, title='ToDo 0')
        todo2 = ToDoBuilder.create_with_index_and_title(todo_id=1, title='ToDo 1')

        db.add_all([todo1, todo2])
        db.commit()
        db.close()


    def test_read_all_todos_returns_all_todos_in_todos_table(self):
        response = self.client.get("/todos/")
        assert response.status_code == status.HTTP_200_OK

        todos = response.json()
        assert len(todos) == 2

    def test_read_todo_reads_correct_todo(self):
        response = self.client.get("/todos/0")
        assert response.status_code == status.HTTP_200_OK

        todo = response.json()
        assert todo['id'] == 0
        assert todo['title'] == 'ToDo 0'

    def test_create_todo_returns_correct_status(self):
        new_todo = {
            'title': 'new_todo',
            'description': 'new_description',
            'priority': 1,
            'completed': False
        }
        response = self.client.post("/todos/todo", json=new_todo)
        assert response.status_code == status.HTTP_201_CREATED

    def test_created_todo_can_be_retrieved(self):
        new_todo = {
            'id': 2,
            'title': 'new_todo',
            'description': 'new_description',
            'priority': 1,
            'completed': False
        }
        self.client.post("/todos/todo", json=new_todo)

        retrieved_todo = self.client.get("/todos/2").json()

        assert retrieved_todo['id'] == 2
        assert retrieved_todo['title'] == 'new_todo'

    def test_update_todo_returns_correct_status_code(self):
        todo_to_update = {
            'title': 'updated_todo',
            'description': 'updated_description',
            'priority': 2,
            'completed': True
        }
        response = self.client.put("/todos/0", json=todo_to_update)

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_updated_todo_returns_updated_content(self):
        todo_to_update = {
            'title': 'updated_todo',
            'description': 'updated_description',
            'priority': 2,
            'completed': True
        }
        self.client.put("/todos/0", json=todo_to_update)
        updated_todo = self.client.get("/todos/0").json()

        assert updated_todo['title'] == 'updated_todo'
        assert updated_todo['description'] == 'updated_description'
        assert updated_todo['priority'] == 2
        assert updated_todo['completed'] is True

    def test_delete_todo_returns_correct_satus_code(self):
        response = self.client.delete("/todos/0")
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_deleted_todo_cannot_be_found(self):
        self.client.delete("/todos/0")
        response = self.client.get("/todos/0")
        assert response.status_code == status.HTTP_404_NOT_FOUND

