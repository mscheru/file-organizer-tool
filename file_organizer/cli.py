from core import rearrange_files
from pathlib import Path
import argparse

def main() -> None:
  parser = argparse.ArgumentParser()
  parser.add_argument('directory')
  parser.add_argument('-d', '--dry-run', action='store_true')

  args = parser.parse_args()
  target_dir = Path(args.directory)
  dry = args.dry_run
  rearrange_files(target_dir, dry)

if __name__ == '__main__':
  main()