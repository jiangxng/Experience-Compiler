import unittest
from ec.budget import choose_budget
class BudgetTests(unittest.TestCase):
    def test_high_value_gets_research_budget(self):
        self.assertEqual(choose_budget("normal",2_000_000).mode,"research")
        self.assertEqual(choose_budget("audit").mode,"audit")
if __name__=='__main__': unittest.main()
