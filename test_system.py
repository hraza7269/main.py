import unittest
import json
import os
from main import RecordManager

class TestUnitRecordManager(unittest.TestCase):
    def test_init_empty(self):
        manager = RecordManager("test_state.json")
        self.assertEqual(manager.records, [])
    
    def test_save_load_state(self):
        manager = RecordManager("test1.json")
        manager.records = [{"test": "data"}]
        manager.save_state()
        loaded = RecordManager("test1.json").records
        self.assertEqual(loaded, [{"test": "data"}])

class TestIntegrationRecordManager(unittest.TestCase):
    def setUp(self):
        self.manager = RecordManager("test_int.json")
        self.test_csv = "test.csv"
        with open(self.test_csv, 'w') as f:
            f.write("name,category,value\nAlice,info,100\nBob,data,200\n")
    
    def tearDown(self):
        for file in ["test_int.json", "test.csv"]:
            if os.path.exists(file):
                os.remove(file)
    
    def test_import_save_integration(self):
        self.manager.import_csv(self.test_csv)
        self.assertEqual(len(self.manager.records), 2)
        self.assertTrue(os.path.exists("test_int.json"))
    
    def test_export_integration(self):
        self.manager.records = [{"test": "data"}]
        self.manager.export_report("test_report.json")
        self.assertTrue(os.path.exists("test_report.json"))
    
    def test_add_record_integration(self):
        self.manager.add_record({"name": "Test"})
        self.assertEqual(len(self.manager.records), 1)
        self.assertTrue(os.path.exists("test_int.json"))

class TestSystemWorkflows(unittest.TestCase):
    def setUp(self):
        self.manager = RecordManager("test_sys.json")
    
    def tearDown(self):
        if os.path.exists("test_sys.json"):
            os.remove("test_sys.json")
    
    def test_full_workflow(self):
        with open("sys_test.csv", 'w') as f:
            f.write("name,val\nTest,123\n")
        self.manager.import_csv("sys_test.csv")
        self.assertEqual(len(self.manager.records), 1)
        success = self.manager.export_report("sys_report.json")
        self.assertTrue(success)
        os.remove("sys_test.csv")
        os.remove("sys_report.json")
    
    def test_error_handling(self):
        self.assertFalse(self.manager.import_csv("nonexistent.csv"))
        self.assertEqual(len(self.manager.records), 0)

if __name__ == '__main__':
    unittest.main()
