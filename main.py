import json
from pathlib import Path
import csv
from typing import List, Dict

class RecordManager:
    def __init__(self, state_file: str = "app_state.json"):
        self.state_file = Path(state_file)
        self.records: List[Dict] = self._load_state()
    
    def _load_state(self) -> List[Dict]:
        if self.state_file.exists():
            try:
                with self.state_file.open('r') as f:
                    return json.load(f).get('records', [])
            except (json.JSONDecodeError, KeyError):
                print("Corrupted state file. Starting fresh.")
        return []
    
    def save_state(self) -> bool:
        try:
            with self.state_file.open('w') as f:
                json.dump({'records': self.records}, f, indent=2)
            return True
        except IOError as e:
            print(f"Save failed: {e}")
            return False
    
    def import_csv(self, csv_path: str) -> bool:
        try:
            with open(csv_path, 'r') as f:
                reader = csv.DictReader(f)
                self.records.extend(list(reader))
            self.save_state()
            print(f"Imported {len(self.records)} records")
            return True
        except FileNotFoundError:
            print("CSV file not found")
        except csv.Error as e:
            print(f"CSV error: {e}")
        return False
    
    def export_report(self, output_file: str) -> bool:
        try:
            report = {
                'total_records': len(self.records),
                'summary': self._generate_summary(),
                'records': self.records
            }
            with open(output_file, 'w') as f:
                json.dump(report, f, indent=2)
            print(f"Report exported to {output_file}")
            return True
        except IOError as e:
            print(f"Export failed: {e}")
        return False
    
    def _generate_summary(self) -> Dict:
        return {'analysis': f'Processed {len(self.records)} records with full persistence'}
    
    def add_record(self, record: Dict):
        self.records.append(record)
        self.save_state()

def main_menu():
    manager = RecordManager()
    while True:
        print("\n=== Information Science Analysis System ===")
        print("1. Import CSV data")
        print("2. Add record")
        print("3. Generate & export report")
        print("4. Show records")
        print("5. Quit")
        
        choice = input("Choose: ").strip()
        if choice == '1':
            manager.import_csv(input("CSV path: "))
        elif choice == '2':
            record = {
                'name': input("Name: "),
                'category': input("Category: "),
                'value': input("Value: ")
            }
            manager.add_record(record)
        elif choice == '3':
            manager.export_report("report.json")
        elif choice == '4':
            print(json.dumps(manager.records, indent=2))
        elif choice == '5':
            break

if __name__ == "__main__":
    main_menu()
