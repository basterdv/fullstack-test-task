import pytest
from pathlib import Path
from src.services.storage import FileStorage


@pytest.fixture
def temp_storage(tmp_path):
    """Создает экземпляр FileStorage с временной папкой"""
    return FileStorage(storage_dir=tmp_path / "test_files")


class TestFileStorage:

    def test_init_creates_directory(self, tmp_path):
        """Проверка, что при инициализации создается папка хранилища"""
        storage_dir = tmp_path / "new_storage"
        assert not storage_dir.exists()

        FileStorage(storage_dir)
        assert storage_dir.exists()
        assert storage_dir.is_dir()

    def test_save_file(self, temp_storage):
        """Проверка сохранения контента в файл"""
        filename = "test.txt"
        content = b"hello world"

        temp_storage.save(filename, content)

        expected_path = temp_storage.get_full_path(filename)
        assert expected_path.exists()
        assert expected_path.read_bytes() == content

    def test_delete_file_exists(self, temp_storage):
        """Проверка удаления существующего файла"""
        filename = "delete_me.dat"
        temp_storage.save(filename, b"data")

        full_path = temp_storage.get_full_path(filename)
        assert full_path.exists()

        temp_storage.delete(filename)
        assert not full_path.exists()

    def test_delete_file_not_exists(self, temp_storage):
        """Проверка, что удаление несуществующего файла не вызывает ошибок"""
        temp_storage.delete("non_existent.txt")

    def test_get_full_path(self, temp_storage):
        """Проверка формирования корректного пути"""
        filename = "image.png"
        path = temp_storage.get_full_path(filename)

        assert isinstance(path, Path)
        assert path.name == filename
        assert str(temp_storage.storage_dir) in str(path)
