from pathlib import Path
from shutil import move

FILE_TO_ORGANIZE = Path('/Users/meghanacheruvu/Downloads/Test_script')
EXTENSION_MAP = {
    # Documents
    ".pdf": "Documents",
    ".doc": "Documents",
    ".docx": "Documents",
    ".txt": "Documents",
    ".rtf": "Documents",
    ".odt": "Documents",
    ".ppt": "Documents",
    ".pptx": "Documents",
    ".xls": "Documents",
    ".xlsx": "Documents",
    ".csv": "Documents",

    # Images
    ".jpg": "Images",
    ".jpeg": "Images",
    ".png": "Images",
    ".gif": "Images",
    ".bmp": "Images",
    ".tiff": "Images",
    ".svg": "Images",
    ".heic": "Images",
    ".webp": "Images",

    # Audio
    ".mp3": "Audio",
    ".wav": "Audio",
    ".aac": "Audio",
    ".flac": "Audio",
    ".ogg": "Audio",
    ".wma": "Audio",
    ".m4a": "Audio",

    # Video
    ".mp4": "Video",
    ".mkv": "Video",
    ".mov": "Video",
    ".avi": "Video",
    ".wmv": "Video",
    ".flv": "Video",
    ".webm": "Video",

    # Archives/Compressed
    ".zip": "Archives",
    ".rar": "Archives",
    ".7z": "Archives",
    ".tar": "Archives",
    ".gz": "Archives",
    ".bz2": "Archives",

    # Code/Programming
    ".py": "Code",
    ".js": "Code",
    ".ts": "Code",
    ".java": "Code",
    ".c": "Code",
    ".cpp": "Code",
    ".cs": "Code",
    ".html": "Code",
    ".css": "Code",
    ".php": "Code",
    ".sh": "Code",
    ".bat": "Code",
    ".rb": "Code",
    ".go": "Code",
    ".rs": "Code",
    ".swift": "Code",

    # Executables/Installers
    ".exe": "Executables",
    ".msi": "Executables",
    ".apk": "Executables",
    ".dmg": "Executables",
    ".pkg": "Executables",
    ".app": "Executables",

    # System/Disk Images
    ".iso": "Disk Images",
    ".img": "Disk Images",
    ".vhd": "Disk Images",
    ".vhdx": "Disk Images",

    # Fonts
    ".ttf": "Fonts",
    ".otf": "Fonts",
    ".woff": "Fonts",
    ".woff2": "Fonts",
}
CATEGORIES = [
  'Documents', 'Images', 
  'Audio', 'Video', 'Archives', 
  'Code', 'Executables', 
  'Disk Images', 'Fonts',
  'Other'
]

def get_files(dir_path: str) -> list[Path]:
  '''Returns all files in provided directory in a list'''
  try:
    directory = Path(dir_path)
    files = []

    for item in directory.iterdir():
      if item.is_file() and not item.name.startswith('.'):
        files.append(item)

    return files

  except OSError:
    print(f'The directory you\'re trying to organize ({dir_path}) does not exist.')
    return []

def create_categories(dir_path: str) -> None:
  '''Create subfolders if the directory does 
  not already have them'''
  directory = Path(dir_path)
  dir_names = set()

  for item in directory.iterdir():
    if item.is_dir():
      dir_names.add(item.name)

  for category in CATEGORIES:
    if category not in dir_names:
      new_folder_path = directory / category
      new_folder_path.mkdir(parents=True, exist_ok=False)

      print(f'Making new {category} folder')

def map_files(files: list[Path], base_path: Path) -> dict[Path, Path]:
  '''Maps the source files to their intended destination during movement'''
  movement_map = {}

  for file in files:
    extension = file.suffix.lower()
    category = EXTENSION_MAP.get(extension, 'Other')
    destination_path = base_path / category / file.name

    movement_map[file] = destination_path

  return movement_map

def display_planned_moves(moves: dict[Path, Path], base_path: Path) -> None:
  '''Explains to the user the intended rearrangement of files'''
  print('The files will be rearranged as follows:')

  for source, destination in moves.items():
    destination_name = destination.relative_to(base_path)
    print(f"{source.name} -> {destination_name}")

def confirm_move() -> str:
  '''Ask user to confirm moving the files'''
  answer = None
  while answer not in ('y', 'n'):
    answer = input('Would you like to proceed to move the files? Y/N ').lower()

  return answer

def get_unique_destination(destination: Path) -> Path:
  '''Renames file if duplicate exists in subfolder'''
  count = 0
  new_destination = destination

  while new_destination.exists():
    new_destination = destination.with_stem(destination.stem + f'_{count}')
    count += 1

  return new_destination
  
def move_files(moves: dict[Path, Path], base_path: Path) -> dict[Path, Path]:
  '''Moves files to appropriate subfolders'''
  successful_moves = {}

  for source, destination in moves.items():
    destination = get_unique_destination(destination)

    try:
      move(source, destination)
    except FileNotFoundError:
      print(f'{source.name} does not exist')
      continue
    except PermissionError:
      print(f'You do not have permission to move {source.name}')
    except Exception as e:
      print(f'{source.name} could not be moved to {destination.relative_to(base_path)}: {e}')
      continue
    else:
      successful_moves[source] = destination

  return successful_moves

def generate_summary(successes: dict[Path, Path], base_path: Path) -> None:
  '''Tells user how the files were rearranged'''
  print('The files were rearranged as follows:')

  for source, destination in successes.items():
    destination_name = destination.relative_to(base_path)
    print(f"{source.name} -> {destination_name}")

def rearrange_files(curr_dir: Path) -> None:
  '''Calls all relevant functions to rearrange directory'''
  files = get_files(curr_dir)
  create_categories(curr_dir)
  moves = map_files(files, curr_dir)

  display_planned_moves(moves, curr_dir)
  answer = confirm_move()
  if answer == 'n':
    print('Quitting file rearranger...')
    return
  
  successes = move_files(moves, curr_dir)
  generate_summary(successes, curr_dir)

  print('Rearrangement complete')

if __name__ == '__main__':
  rearrange_files(FILE_TO_ORGANIZE)


  
  



