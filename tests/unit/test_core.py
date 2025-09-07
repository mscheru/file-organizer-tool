import unittest
from pathlib import Path
from shutil import move
from file_organizer import core

import unittest.mock as mock


class TestFileOrganizer(unittest.TestCase):
  
  @mock.patch("file_organizer.core.Path")  
  def test_get_files_returns_only_files(self, mock_path_cls):
    fake_file = mock.Mock(spec=Path)
    fake_file.is_file.return_value = True
    fake_file.name = "file.txt"

    fake_hidden_file = mock.Mock(spec=Path)
    fake_hidden_file.is_file.return_value = True
    fake_hidden_file.name = ".hidden"

    fake_inner_dir = mock.Mock(spec=Path)
    fake_inner_dir.is_file.return_value = False

    fake_dir = mock.Mock(spec=Path)
    fake_dir.iterdir.return_value = [fake_file, fake_hidden_file, fake_inner_dir]

    mock_path_cls.return_value = fake_dir

    result = core.get_files("fake_dir")

    self.assertEqual(result, [fake_file])  
    fake_file.is_file.assert_called() 

  @mock.patch("file_organizer.core.Path")  
  def test_get_files_raises_error_when_directory_does_not_exist(self, mock_path_cls):
    mock_path_cls.side_effect = OSError("Directory does not exist")

    result = core.get_files("fake_dir")

    self.assertEqual(result, [])  


if __name__ == '__main__':
  unittest.main()