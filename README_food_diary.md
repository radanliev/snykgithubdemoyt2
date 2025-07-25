# Food Diary

A simple, secure food diary application for tracking daily food intake. This application provides both a command-line interface and a web interface for managing food entries.

![Food Diary Web Interface](https://github.com/user-attachments/assets/15ffd9b1-7061-4303-89c5-fbcae8be85ea)

## Features

- ✅ **Command-line interface** for quick food entry management
- 🌐 **Web interface** with a clean, responsive design
- 📊 **Statistics tracking** (total calories, daily averages, etc.)
- 💾 **Persistent storage** using JSON file
- 🔒 **Secure implementation** (no eval, no command injection, proper input validation)
- 📅 **Date-based filtering** for viewing historical entries
- 🍽️ **Meal categorization** (breakfast, lunch, dinner, snack)

## Installation

No additional dependencies required! The food diary uses only Python standard library modules.

```bash
# Clone the repository (if not already done)
git clone https://github.com/radanliev/snykgithubdemoyt2.git
cd snykgithubdemoyt2

# The food diary is ready to use
python food_diary.py help
```

## Usage

### Command Line Interface

#### Add a food entry
```bash
python food_diary.py add "Chicken Salad" 350 lunch "Healthy and filling"
python food_diary.py add "Apple" 95 snack
python food_diary.py add "Oatmeal with berries" 280 breakfast "Great start to the day"
```

#### List today's entries
```bash
python food_diary.py list
```

#### List entries for a specific date
```bash
python food_diary.py list 2024-01-15
```

#### View statistics
```bash
python food_diary.py stats
```

#### Start web server
```bash
python food_diary.py server 8080
# Then visit http://localhost:8080 in your browser
```

### Web Interface

Start the web server and navigate to the provided URL to access the web interface:

1. **Add entries** using the form at the top
2. **View today's entries** with total calorie count
3. **Access API endpoints** for programmatic integration

### API Endpoints

When the web server is running, you can access these REST API endpoints:

- `GET /food/list` - Get all food entries as JSON
- `GET /food/date/YYYY-MM-DD` - Get entries for a specific date
- `GET /food/stats` - Get overall statistics
- `POST /food/add` - Add a new food entry (form data or JSON)

#### API Examples

```bash
# Get all entries
curl http://localhost:8080/food/list

# Get entries for a specific date
curl http://localhost:8080/food/date/2024-01-15

# Get statistics
curl http://localhost:8080/food/stats

# Add an entry via API
curl -X POST http://localhost:8080/food/add \
  -d "food_name=Pasta&calories=400&meal_type=dinner&notes=Italian cuisine"
```

## Data Format

Food entries are stored in `food_diary_data.json` with the following structure:

```json
{
  "id": 1,
  "food_name": "Oatmeal with berries",
  "calories": 280,
  "meal_type": "breakfast",
  "notes": "Healthy start to the day",
  "date": "2025-07-25",
  "timestamp": "2025-07-25 18:02:22"
}
```

## Meal Types

Valid meal types are:
- `breakfast`
- `lunch`
- `dinner`
- `snack`

## Security Features

This food diary implementation follows security best practices:

- ✅ **Input validation** - All user inputs are validated and sanitized
- ✅ **No code execution** - No use of `eval()` or `exec()`
- ✅ **No command injection** - No use of `os.system()` or subprocess with user input
- ✅ **Type safety** - Proper type checking for numeric inputs
- ✅ **Error handling** - Graceful handling of invalid inputs and edge cases

## Examples

### Sample Daily Usage

```bash
# Morning
python food_diary.py add "Greek Yogurt" 150 breakfast "With honey and nuts"

# Lunch
python food_diary.py add "Quinoa Salad" 420 lunch "Lots of vegetables"

# Afternoon snack
python food_diary.py add "Mixed Nuts" 200 snack

# Dinner
python food_diary.py add "Grilled Salmon" 380 dinner "With steamed broccoli"

# Check today's total
python food_diary.py list
```

### Sample Output

```
📅 Food entries for today:
--------------------------------------------------
🍽️  Greek Yogurt (breakfast)
    ⚡ 150 calories at 2025-07-25 08:30:15
    📝 With honey and nuts

🍽️  Quinoa Salad (lunch)
    ⚡ 420 calories at 2025-07-25 12:45:22
    📝 Lots of vegetables

🍽️  Mixed Nuts (snack)
    ⚡ 200 calories at 2025-07-25 15:20:10

🍽️  Grilled Salmon (dinner)
    ⚡ 380 calories at 2025-07-25 19:15:33
    📝 With steamed broccoli

📊 Total calories: 1150
```

## File Structure

- `food_diary.py` - Main application file
- `food_diary_data.json` - Persistent data storage (created automatically)
- `README_food_diary.md` - This documentation file

## Contributing

This food diary is part of the snykgithubdemoyt2 repository. When contributing:

1. Maintain security best practices
2. Add proper input validation for new features
3. Update documentation for any new functionality
4. Test both CLI and web interfaces

## License

This project follows the same license as the parent repository.