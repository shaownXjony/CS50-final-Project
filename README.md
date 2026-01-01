# Weekly Budget Planner
#### Video Demo:  <https://youtu.be/uZwrSjlk1z8>

#### Description:

This weekly budget planner helps us manage our weekly spending and save money. It has a command-line program where we can set a weekly budget, track our expenses, and automatically save into a savings account whatever money we don't spend.

I built this because I was terrible at managing my own money and wanted something simple that would actually help me stick to a budget. The weekly format works better for me than monthly budgets because it's easier to course-correct if I'm overspending.

### Main Features

**User System**
- Create your own account with username and password
- Multiple people can use the same program
- Your password gets encrypted for security

**Budget Management**
- Set how much you want to spend each week
- Track expenses in categories like food, transportation, entertainment, rent
- Add your own custom expense categories
- See how much you've spent and how much is left

**Expense Tracking**
- Add expenses for any date
- Edit or delete expenses if you make mistakes
- View weekly reports showing where your money went
- Get a summary on the main screen

**Automatic Savings**
- Whatever you don't spend gets moved to savings
- This happens automatically when you login each week
- You can also manually transfer on Sundays
- Keep track of your growing savings balance

### How to Set It Up

**Requirements**
- Python 3.x (I used Python 3.11)
- The packages in requirements.txt

**Installation Steps**
1. Download all the project files
2. Open terminal/command prompt in the project folder
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the program:
   ```bash
   python project.py
   ```

### Testing

I wrote tests for the important functions to make sure they work correctly:

```bash
pytest test_project.py
```

**What gets tested:**
- Date formatting works properly
- Password hashing is consistent and secure
- Week calculations are correct (Monday to Sunday)
- File saving and loading doesn't break
- Expense math adds up correctly

I focused on testing the behind-the-scenes functions rather than the menu system since those are harder to test automatically.

### Project Files

```
smart-budget-planner/
├── project.py          # Main program
├── test_project.py     # Unit tests
├── requirements.txt    # Dependencies
├── users_data.json     # User data (created automatically)
└── README.md          # This file
```

### How I Built This

**The Weekly System**
I chose weekly budgets instead of monthly because:
- It's easier to remember what you spent this week vs this month
- You get more frequent "wins" when you save money
- If you mess up one week, you can start fresh quickly

**Data Storage**
Everything saves to a JSON file so your data persists between sessions. I hash passwords with SHA-256 so they're not stored in plain text.

**Menu Design**
I kept the interface simple with numbered menus. The main screen shows your current budget status so you always know where you stand.

### Problems I Solved

**Week Calculations**
The trickiest part was getting the weekly math right. I had to make sure:
- Weeks always start on Monday and end on Sunday
- Expenses from different weeks don't get mixed up
- The automatic transfer only happens once per week

**Input Validation**
Since this deals with money, I had to be careful about user input:
- Make sure amounts are valid numbers
- Don't allow negative expenses
- Handle bad date formats gracefully
- Prevent crashes from unexpected input

**User Experience**
I wanted this to be something I'd actually use, so I focused on:
- Clear error messages that tell you what went wrong
- Confirmation prompts before deleting things
- Summary information always visible
- Not too many options on each screen

### Testing Strategy

Writing tests taught me to think about edge cases I hadn't considered:
- What if someone enters an empty password?
- What if the JSON file gets corrupted?
- What if someone tries to edit an expense that doesn't exist?

The tests cover the core logic functions but not the interactive parts. Testing user input/output functions is more complex and wasn't essential for this project's scope.

### Why This Project Matters

Personal finance apps are either too complicated or too simple. This hits a sweet spot where it's easy to use but actually helps build good habits. The automatic savings feature is key - it rewards you for spending less instead of just tracking what you spend.

This project demonstrates several programming concepts I learned in CS50:
- File I/O and JSON handling
- Data validation and error handling
- Working with dates and times
- Password security basics
- Menu-driven program flow
- Unit testing

I'm actually using this program myself now, which I think is the best test of whether it's useful.

### Future Ideas

Some things I might add later:
- Export data to spreadsheet
- Set spending limits per category
- Show spending trends over time
- Budget suggestions based on past spending
- Email reminders about budget status

But for now, it does exactly what I need it to do without being overly complicated.

"README generated with assistance from CLaude and edited by me."
